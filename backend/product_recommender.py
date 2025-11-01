"""
UniRec - Product Recommendation Model
Collaborative Filtering + Metadata-based
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

class ProductRecommender:
    def __init__(self):
        self.user_item_matrix = None
        self.products_df = None
        self.user_profiles = {}
        self.tfidf_vectorizer = None
        self.item_similarity = None
        self.category_embeddings = None
        
    def prepare_data(self, reviews_path, products_path):
        """Load and prepare product data"""
        # Load reviews and product metadata
        reviews = pd.read_csv(reviews_path)
        self.products_df = pd.read_csv(products_path)
        
        # Ensure we have required columns
        # Expected: userId, productId, rating, timestamp
        # Products: productId, title, category, brand, price
        
        # Create user-item matrix
        self.user_item_matrix = reviews.pivot_table(
            index='userId',
            columns='productId',
            values='rating'
        ).fillna(0)
        
        # Prepare product features
        self.products_df['features'] = (
            self.products_df['category'].fillna('') + ' ' +
            self.products_df['brand'].fillna('') + ' ' +
            self.products_df['title'].fillna('')
        )
        
        # Create TF-IDF features
        self.tfidf_vectorizer = TfidfVectorizer(max_features=150, stop_words='english')
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.products_df['features'])
        
        # Calculate item-item similarity
        self.item_similarity = cosine_similarity(tfidf_matrix)
        
        # Create category embeddings
        unique_categories = self.products_df['category'].unique()
        self.category_embeddings = {cat: idx for idx, cat in enumerate(unique_categories)}
        
        return self
    
    def train(self):
        """Train the model and create user profiles"""
        for user_id in self.user_item_matrix.index:
            user_ratings = self.user_item_matrix.loc[user_id]
            rated_items = user_ratings[user_ratings > 0]
            
            if len(rated_items) > 0:
                rated_product_ids = rated_items.index.tolist()
                product_indices = [
                    self.products_df[self.products_df['productId'] == pid].index[0]
                    for pid in rated_product_ids 
                    if pid in self.products_df['productId'].values
                ]
                
                if product_indices:
                    # User embedding from purchased/rated products
                    user_embedding = np.mean(self.item_similarity[product_indices], axis=0)
                    
                    # Calculate category preferences
                    category_prefs = {}
                    for pid in rated_product_ids:
                        product = self.products_df[self.products_df['productId'] == pid]
                        if not product.empty:
                            category = product.iloc[0]['category']
                            rating = user_ratings[pid]
                            if category in category_prefs:
                                category_prefs[category].append(rating)
                            else:
                                category_prefs[category] = [rating]
                    
                    category_prefs = {k: np.mean(v) for k, v in category_prefs.items()}
                    
                    self.user_profiles[user_id] = {
                        'embedding': user_embedding,
                        'rated_items': rated_product_ids,
                        'avg_rating': rated_items.mean(),
                        'category_preferences': category_prefs,
                        'preferred_categories': sorted(category_prefs.items(), 
                                                      key=lambda x: x[1], 
                                                      reverse=True)[:3]
                    }
        
        return self
    
    def get_collaborative_scores(self, user_id):
        """Collaborative filtering scores"""
        if user_id not in self.user_item_matrix.index:
            return {}
        
        user_vector = self.user_item_matrix.loc[user_id].values.reshape(1, -1)
        user_similarities = cosine_similarity(user_vector, self.user_item_matrix.values)[0]
        
        # Get similar users
        similar_users_idx = np.argsort(user_similarities)[-11:-1][::-1]
        similar_users = self.user_item_matrix.index[similar_users_idx]
        
        cf_scores = {}
        user_rated = set(self.user_item_matrix.loc[user_id][self.user_item_matrix.loc[user_id] > 0].index)
        
        for similar_user in similar_users:
            sim_score = user_similarities[self.user_item_matrix.index.get_loc(similar_user)]
            similar_user_ratings = self.user_item_matrix.loc[similar_user]
            
            for product_id, rating in similar_user_ratings[similar_user_ratings > 0].items():
                if product_id not in user_rated:
                    if product_id not in cf_scores:
                        cf_scores[product_id] = []
                    cf_scores[product_id].append(rating * sim_score)
        
        cf_scores = {pid: np.mean(scores) for pid, scores in cf_scores.items()}
        return cf_scores
    
    def get_content_scores(self, user_id):
        """Content-based filtering scores"""
        if user_id not in self.user_profiles:
            return {}
        
        user_profile = self.user_profiles[user_id]
        user_embedding = user_profile['embedding']
        rated_items = set(user_profile['rated_items'])
        category_prefs = user_profile['category_preferences']
        
        content_scores = {}
        for idx, row in self.products_df.iterrows():
            product_id = row['productId']
            if product_id not in rated_items:
                # Base similarity score
                similarity = user_embedding[idx]
                
                # Boost by category preference
                category = row['category']
                category_boost = category_prefs.get(category, 0) / 5.0  # Normalize by max rating
                
                content_scores[product_id] = similarity + 0.3 * category_boost
        
        return content_scores
    
    def recommend(self, user_id, n_recommendations=10, alpha=0.5):
        """
        Hybrid recommendation
        alpha: weight for collaborative filtering
        """
        cf_scores = self.get_collaborative_scores(user_id)
        content_scores = self.get_content_scores(user_id)
        
        # Normalize
        if cf_scores:
            max_cf = max(cf_scores.values())
            cf_scores = {k: v/max_cf for k, v in cf_scores.items()}
        
        if content_scores:
            max_content = max(content_scores.values())
            content_scores = {k: v/max_content for k, v in content_scores.items()}
        
        # Combine
        all_items = set(cf_scores.keys()) | set(content_scores.keys())
        hybrid_scores = {}
        
        for item in all_items:
            cf_score = cf_scores.get(item, 0)
            content_score = content_scores.get(item, 0)
            hybrid_scores[item] = alpha * cf_score + (1 - alpha) * content_score
        
        # Get top recommendations
        top_items = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
        
        recommendations = []
        for product_id, score in top_items:
            product = self.products_df[self.products_df['productId'] == product_id]
            if not product.empty:
                p = product.iloc[0]
                recommendations.append({
                    'item_id': int(product_id),
                    'title': p['title'],
                    'category': p['category'],
                    'brand': p.get('brand', 'N/A'),
                    'price': float(p.get('price', 0)),
                    'score': float(score),
                    'domain': 'products'
                })
        
        return recommendations
    
    def get_user_embedding(self, user_id):
        """Get user embedding for unified profile"""
        if user_id in self.user_profiles:
            profile = self.user_profiles[user_id]
            return {
                'embedding': profile['embedding'],
                'preferences': profile['category_preferences']
            }
        return None
    
    def save_model(self, path):
        """Save trained model"""
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load_model(path):
        """Load trained model"""
        with open(path, 'rb') as f:
            return pickle.load(f)


if __name__ == "__main__":
    # Initialize and train
    recommender = ProductRecommender()
    recommender.prepare_data('product_reviews.csv', 'products.csv')
    recommender.train()
    recommender.save_model('product_recommender.pkl')
    
    # Test
    user_id = 1
    recommendations = recommender.recommend(user_id, n_recommendations=10)
    
    print(f"Top 10 product recommendations for User {user_id}:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} - {rec['category']} (${rec['price']:.2f}) - Score: {rec['score']:.3f}")