"""
UniRec - Unified Recommendation Engine
Cross-Domain User Profiling and Ranking
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import lightgbm as lgb
import pickle
import json

class UnifiedRecommender:
    def __init__(self, movie_model, product_model, music_model, course_model):
        """
        Initialize with trained domain-specific models
        """
        self.movie_model = movie_model
        self.product_model = product_model
        self.music_model = music_model
        self.course_model = course_model
        
        self.unified_profiles = {}
        self.ranker = None
        self.scaler = StandardScaler()
        
    def build_unified_profile(self, user_id):
        """
        Create a unified user profile across all domains
        """
        profile = {
            'user_id': user_id,
            'domains': {},
            'unified_embedding': None,
            'preferences': {}
        }
        
        # Collect embeddings from each domain
        embeddings = []
        weights = []
        
        # Movies
        movie_emb = self.movie_model.get_user_embedding(user_id)
        if movie_emb is not None:
            embeddings.append(movie_emb)
            weights.append(1.0)
            profile['domains']['movies'] = True
            profile['preferences']['movies'] = {
                'engaged': True,
                'embedding_size': len(movie_emb)
            }
        else:
            profile['domains']['movies'] = False
        
        # Products
        product_data = self.product_model.get_user_embedding(user_id)
        if product_data is not None:
            embeddings.append(product_data['embedding'])
            weights.append(1.2)  # Slightly higher weight for purchase behavior
            profile['domains']['products'] = True
            profile['preferences']['products'] = {
                'engaged': True,
                'categories': product_data['preferences']
            }
        else:
            profile['domains']['products'] = False
        
        # Music
        music_emb = self.music_model.get_user_embedding(user_id)
        if music_emb is not None:
            embeddings.append(music_emb)
            weights.append(0.8)  # Slightly lower weight (more casual)
            profile['domains']['music'] = True
            profile['preferences']['music'] = {
                'engaged': True
            }
        else:
            profile['domains']['music'] = False
        
        # Courses
        course_data = self.course_model.get_user_embedding(user_id)
        if course_data is not None:
            embeddings.append(course_data['embedding'])
            weights.append(1.1)
            profile['domains']['courses'] = True
            profile['preferences']['courses'] = {
                'engaged': True,
                'skill_level': course_data['skill_level'],
                'interests': course_data['interests']
            }
        else:
            profile['domains']['courses'] = False
        
        # Create unified embedding
        if embeddings:
            # Pad embeddings to same length
            max_len = max(len(emb) for emb in embeddings)
            padded_embeddings = []
            for emb in embeddings:
                if len(emb) < max_len:
                    padded = np.pad(emb, (0, max_len - len(emb)), mode='constant')
                else:
                    padded = emb[:max_len]
                padded_embeddings.append(padded)
            
            # Weighted average
            weights = np.array(weights)
            weights = weights / weights.sum()
            profile['unified_embedding'] = np.average(padded_embeddings, axis=0, weights=weights)
        
        self.unified_profiles[user_id] = profile
        return profile
    
    def extract_cross_domain_features(self, user_id, item, domain):
        """
        Extract features for ranking that consider cross-domain behavior
        """
        if user_id not in self.unified_profiles:
            self.build_unified_profile(user_id)
        
        profile = self.unified_profiles[user_id]
        
        features = {
            # Domain engagement features
            'movies_engaged': 1 if profile['domains']['movies'] else 0,
            'products_engaged': 1 if profile['domains']['products'] else 0,
            'music_engaged': 1 if profile['domains']['music'] else 0,
            'courses_engaged': 1 if profile['domains']['courses'] else 0,
            'total_domains_engaged': sum(profile['domains'].values()),
            
            # Item features
            'item_score': item['score'],
            'domain': ['movies', 'products', 'music', 'courses'].index(domain),
        }
        
        # Cross-domain signals
        if domain == 'movies' and profile['domains']['courses']:
            # If user takes courses, might prefer educational/documentary content
            features['cross_domain_boost_education'] = 1
        else:
            features['cross_domain_boost_education'] = 0
        
        if domain == 'products' and profile['domains']['music']:
            # If user listens to music, might be interested in audio gear
            features['cross_domain_boost_audio'] = 1
        else:
            features['cross_domain_boost_audio'] = 0
        
        if domain == 'courses' and profile['domains']['products']:
            # If user buys products, might want practical/skill courses
            features['cross_domain_boost_practical'] = 1
        else:
            features['cross_domain_boost_practical'] = 0
        
        return features
    
    def train_ranker(self, training_data):
        """
        Train a LightGBM ranker to optimize final recommendations
        training_data: list of dicts with features and labels
        """
        df = pd.DataFrame(training_data)
        X = df.drop(['label', 'user_id'], axis=1)
        y = df['label']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train LightGBM ranker
        train_data = lgb.Dataset(X_scaled, label=y)
        
        params = {
            'objective': 'lambdarank',
            'metric': 'ndcg',
            'boosting_type': 'gbdt',
            'num_leaves': 31,
            'learning_rate': 0.05,
            'feature_fraction': 0.9
        }
        
        self.ranker = lgb.train(params, train_data, num_boost_round=100)
        return self
    
    def get_unified_recommendations(self, user_id, n_per_domain=5, n_total=20, user_preferences=None):
        """
        Get unified recommendations across all domains
        user_preferences: dict containing user's quiz preferences (favorite_music_genres, favorite_genres, etc.)
        """
        # Build unified profile
        profile = self.build_unified_profile(user_id)
        
        # Get recommendations from each domain
        all_recommendations = []
        
        if profile['domains']['movies']:
            # Pass favorite movie genres if available
            preferred_movie_genres = None
            if user_preferences and 'favorite_genres' in user_preferences:
                preferred_movie_genres = user_preferences['favorite_genres']
            
            movie_recs = self.movie_model.recommend(
                user_id, 
                n_recommendations=n_per_domain,
                preferred_genres=preferred_movie_genres
            )
            all_recommendations.extend(movie_recs)
        
        if profile['domains']['products']:
            # Pass shopping categories if available
            preferred_categories = None
            if user_preferences and 'shopping_categories' in user_preferences:
                preferred_categories = user_preferences['shopping_categories']
            
            product_recs = self.product_model.recommend(
                user_id, 
                n_recommendations=n_per_domain,
                preferred_categories=preferred_categories
            )
            all_recommendations.extend(product_recs)
        
        if profile['domains']['music']:
            # Pass favorite music genres if available
            preferred_music_genres = None
            if user_preferences and 'favorite_music_genres' in user_preferences:
                preferred_music_genres = user_preferences['favorite_music_genres']
            
            music_recs = self.music_model.recommend(
                user_id, 
                n_recommendations=n_per_domain,
                preferred_genres=preferred_music_genres
            )
            all_recommendations.extend(music_recs)
        
        if profile['domains']['courses']:
            # Pass learning interests if available
            learning_interests = None
            if user_preferences and 'learning_interests' in user_preferences:
                learning_interests = user_preferences['learning_interests']
            
            course_recs = self.course_model.recommend(
                user_id, 
                n_recommendations=n_per_domain,
                preferred_topics=learning_interests
            )
            all_recommendations.extend(course_recs)
        
        # If ranker is trained, use it to re-rank
        if self.ranker is not None and all_recommendations:
            features_list = []
            for rec in all_recommendations:
                features = self.extract_cross_domain_features(user_id, rec, rec['domain'])
                features_list.append(features)
            
            X = pd.DataFrame(features_list)
            X_scaled = self.scaler.transform(X)
            
            # Get ranking scores
            ranking_scores = self.ranker.predict(X_scaled)
            
            # Add ranking scores to recommendations
            for i, rec in enumerate(all_recommendations):
                rec['unified_score'] = float(ranking_scores[i])
            
            # Sort by unified score
            all_recommendations = sorted(all_recommendations, 
                                       key=lambda x: x['unified_score'], 
                                       reverse=True)[:n_total]
        else:
            # Without ranker, use simple score-based sorting
            all_recommendations = sorted(all_recommendations,
                                       key=lambda x: x['score'],
                                       reverse=True)[:n_total]
        
        return {
            'user_id': user_id,
            'recommendations': all_recommendations,
            'profile_summary': {
                'domains_engaged': sum(profile['domains'].values()),
                'has_unified_embedding': profile['unified_embedding'] is not None
            }
        }
    
    def get_domain_specific_recommendations(self, user_id, domain, n_recommendations=10):
        """
        Get recommendations for a specific domain
        """
        if domain == 'movies':
            return self.movie_model.recommend(user_id, n_recommendations)
        elif domain == 'products':
            return self.product_model.recommend(user_id, n_recommendations)
        elif domain == 'music':
            return self.music_model.recommend(user_id, n_recommendations)
        elif domain == 'courses':
            return self.course_model.recommend(user_id, n_recommendations)
        else:
            return []
    
    def save_unified_model(self, path):
        """Save the unified model"""
        model_data = {
            'unified_profiles': self.unified_profiles,
            'ranker': self.ranker,
            'scaler': self.scaler
        }
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_unified_model(self, path):
        """Load the unified model"""
        with open(path, 'rb') as f:
            model_data = pickle.load(f)
        self.unified_profiles = model_data['unified_profiles']
        self.ranker = model_data['ranker']
        self.scaler = model_data['scaler']
        return self


# Example usage
if __name__ == "__main__":
    from movie_recommender import MovieRecommender
    from product_recommender import ProductRecommender
    from music_recommender import MusicRecommender
    from course_recommender import CourseRecommender
    
    # Load trained domain models
    movie_model = MovieRecommender.load_model('movie_recommender.pkl')
    product_model = ProductRecommender.load_model('product_recommender.pkl')
    music_model = MusicRecommender.load_model('music_recommender.pkl')
    course_model = CourseRecommender.load_model('course_recommender.pkl')
    
    # Create unified recommender
    unified = UnifiedRecommender(movie_model, product_model, music_model, course_model)
    
    # Get unified recommendations
    user_id = 1
    results = unified.get_unified_recommendations(user_id, n_per_domain=5, n_total=20)
    
    print(f"\nTop 20 Unified Recommendations for User {user_id}:")
    print(f"User engaged with {results['profile_summary']['domains_engaged']} domains\n")
    
    for i, rec in enumerate(results['recommendations'], 1):
        domain = rec['domain'].upper()
        title = rec['title']
        score = rec.get('unified_score', rec['score'])
        print(f"{i}. [{domain}] {title} (Score: {score:.3f})")