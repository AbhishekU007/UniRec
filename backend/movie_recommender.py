"""
UniRec - Movie Recommendation Model
Hybrid Collaborative Filtering + Content-Based
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
import pickle
import json

class MovieRecommender:
    def __init__(self):
        self.user_item_matrix = None
        self.item_features = None
        self.movies_df = None
        self.user_profiles = {}
        self.tfidf_vectorizer = None
        self.item_similarity = None
        
    def prepare_data(self, ratings_path, movies_path):
        """Load and prepare MovieLens data"""
        # Load data
        ratings = pd.read_csv(ratings_path)
        self.movies_df = pd.read_csv(movies_path)
        
        # Create user-item matrix for collaborative filtering
        self.user_item_matrix = ratings.pivot_table(
            index='userId', 
            columns='movieId', 
            values='rating'
        ).fillna(0)
        
        # Prepare content features (genres)
        self.movies_df['genres_clean'] = self.movies_df['genres'].str.replace('|', ' ')
        
        # Create TF-IDF features for content-based filtering
        self.tfidf_vectorizer = TfidfVectorizer(max_features=100)
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.movies_df['genres_clean'])
        
        # Calculate item-item similarity
        self.item_similarity = cosine_similarity(tfidf_matrix)
        
        return self
    
    def train(self):
        """Train the hybrid model"""
        # For each user, create a profile based on their interactions
        for user_id in self.user_item_matrix.index:
            user_ratings = self.user_item_matrix.loc[user_id]
            rated_items = user_ratings[user_ratings > 0]
            
            if len(rated_items) > 0:
                # Create user embedding (average of rated item features)
                rated_movie_ids = rated_items.index.tolist()
                movie_indices = [self.movies_df[self.movies_df['movieId'] == mid].index[0] 
                               for mid in rated_movie_ids if mid in self.movies_df['movieId'].values]
                
                if movie_indices:
                    user_embedding = np.mean(self.item_similarity[movie_indices], axis=0)
                    self.user_profiles[user_id] = {
                        'embedding': user_embedding,
                        'rated_items': rated_movie_ids,
                        'avg_rating': rated_items.mean()
                    }
        
        return self
    
    def get_collaborative_scores(self, user_id, n_items=20):
        """Get scores using collaborative filtering"""
        if user_id not in self.user_item_matrix.index:
            return {}
        
        # Find similar users
        user_vector = self.user_item_matrix.loc[user_id].values.reshape(1, -1)
        user_similarities = cosine_similarity(user_vector, self.user_item_matrix.values)[0]
        
        # Get top similar users (excluding self)
        similar_users_idx = np.argsort(user_similarities)[-11:-1][::-1]
        similar_users = self.user_item_matrix.index[similar_users_idx]
        
        # Aggregate ratings from similar users
        cf_scores = {}
        user_rated = set(self.user_item_matrix.loc[user_id][self.user_item_matrix.loc[user_id] > 0].index)
        
        for similar_user in similar_users:
            sim_score = user_similarities[self.user_item_matrix.index.get_loc(similar_user)]
            similar_user_ratings = self.user_item_matrix.loc[similar_user]
            
            for movie_id, rating in similar_user_ratings[similar_user_ratings > 0].items():
                if movie_id not in user_rated:
                    if movie_id not in cf_scores:
                        cf_scores[movie_id] = []
                    cf_scores[movie_id].append(rating * sim_score)
        
        # Average the scores
        cf_scores = {mid: np.mean(scores) for mid, scores in cf_scores.items()}
        return cf_scores
    
    def get_content_scores(self, user_id, n_items=20):
        """Get scores using content-based filtering"""
        if user_id not in self.user_profiles:
            return {}
        
        user_profile = self.user_profiles[user_id]
        user_embedding = user_profile['embedding']
        rated_items = set(user_profile['rated_items'])
        
        # Calculate similarity with all items
        content_scores = {}
        for idx, row in self.movies_df.iterrows():
            movie_id = row['movieId']
            if movie_id not in rated_items:
                similarity = user_embedding[idx]
                content_scores[movie_id] = similarity
        
        return content_scores
    
    def get_popular_items(self, n_recommendations=10):
        """Get popular items for cold start (fallback)"""
        if self.user_item_matrix is None:
            return []
        
        # Calculate popularity based on ratings
        item_popularity = self.user_item_matrix.sum(axis=0).sort_values(ascending=False)
        top_items = item_popularity.head(n_recommendations * 2)  # Get more to filter
        
        recommendations = []
        for movie_id, popularity in top_items.items():
            movie_info = self.movies_df[self.movies_df['movieId'] == movie_id]
            if not movie_info.empty:
                recommendations.append({
                    'item_id': int(movie_id),
                    'title': movie_info.iloc[0]['title'],
                    'genres': movie_info.iloc[0]['genres'],
                    'score': float(popularity / item_popularity.max()),
                    'domain': 'movies'
                })
            if len(recommendations) >= n_recommendations:
                break
        
        return recommendations
    
    def recommend(self, user_id, n_recommendations=10, alpha=0.6):
        """
        Hybrid recommendation with cold start handling
        alpha: weight for collaborative filtering (1-alpha for content-based)
        """
        cf_scores = self.get_collaborative_scores(user_id)
        content_scores = self.get_content_scores(user_id)
        
        # Cold start handling: if user has no history
        if not cf_scores and not content_scores:
            return self.get_popular_items(n_recommendations)
        
        # Normalize scores
        if cf_scores:
            max_cf = max(cf_scores.values())
            cf_scores = {k: v/max_cf for k, v in cf_scores.items()}
        
        if content_scores:
            max_content = max(content_scores.values())
            content_scores = {k: v/max_content for k, v in content_scores.items()}
        
        # Combine scores
        all_items = set(cf_scores.keys()) | set(content_scores.keys())
        hybrid_scores = {}
        
        for item in all_items:
            cf_score = cf_scores.get(item, 0)
            content_score = content_scores.get(item, 0)
            hybrid_scores[item] = alpha * cf_score + (1 - alpha) * content_score
        
        # Get top recommendations
        top_items = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
        
        # Format recommendations
        recommendations = []
        for movie_id, score in top_items:
            movie_info = self.movies_df[self.movies_df['movieId'] == movie_id]
            if not movie_info.empty:
                recommendations.append({
                    'item_id': int(movie_id),
                    'title': movie_info.iloc[0]['title'],
                    'genres': movie_info.iloc[0]['genres'],
                    'score': float(score),
                    'domain': 'movies'
                })
        
        return recommendations
    
    def get_user_embedding(self, user_id):
        """Get user embedding for unified profile"""
        if user_id in self.user_profiles:
            return self.user_profiles[user_id]['embedding']
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


# Example usage and training script
if __name__ == "__main__":
    # Initialize recommender
    recommender = MovieRecommender()
    
    # Prepare data (you'll need to download MovieLens dataset)
    # Download from: https://grouplens.org/datasets/movielens/
    recommender.prepare_data('ratings.csv', 'movies.csv')
    
    # Train
    recommender.train()
    
    # Save model
    recommender.save_model('movie_recommender.pkl')
    
    # Test recommendation
    user_id = 1
    recommendations = recommender.recommend(user_id, n_recommendations=10)
    
    print(f"Top 10 movie recommendations for User {user_id}:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} - {rec['genres']} (Score: {rec['score']:.3f})")