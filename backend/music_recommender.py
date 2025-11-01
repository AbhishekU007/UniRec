"""
UniRec - Music Recommendation Model
Embedding-based with Audio Features
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pickle

class MusicRecommender:
    def __init__(self, n_components=50):
        self.user_item_matrix = None
        self.tracks_df = None
        self.user_profiles = {}
        self.track_embeddings = None
        self.scaler = StandardScaler()
        self.n_components = n_components
        self.pca = None  # Will be initialized in prepare_data
        self.item_similarity = None
        
    def prepare_data(self, listening_history_path, tracks_path):
        """
        Load music data
        listening_history: userId, trackId, playCount, timestamp
        tracks: trackId, title, artist, album, genre, duration, tempo, energy, valence, etc.
        """
        history = pd.read_csv(listening_history_path)
        self.tracks_df = pd.read_csv(tracks_path)
        
        # Create user-item matrix (using play counts)
        self.user_item_matrix = history.pivot_table(
            index='userId',
            columns='trackId',
            values='playCount',
            fill_value=0
        )
        
        # Prepare audio features for embedding
        audio_features = ['tempo', 'energy', 'valence', 'danceability', 
                         'acousticness', 'instrumentalness', 'loudness', 'duration']
        
        # Filter to available features
        available_features = [f for f in audio_features if f in self.tracks_df.columns]
        
        if not available_features:
            # Fallback: create dummy features from genre
            self.tracks_df['genre_encoded'] = pd.Categorical(self.tracks_df['genre']).codes
            feature_matrix = self.tracks_df[['genre_encoded']].values
        else:
            feature_matrix = self.tracks_df[available_features].fillna(0).values
        
        # Scale and reduce dimensionality
        scaled_features = self.scaler.fit_transform(feature_matrix)
        
        # Adjust n_components to be min of n_components and feature dimensions
        n_features = scaled_features.shape[1]
        actual_components = min(self.n_components, n_features)
        self.pca = PCA(n_components=actual_components)
        
        self.track_embeddings = self.pca.fit_transform(scaled_features)
        
        # Calculate track similarity
        self.item_similarity = cosine_similarity(self.track_embeddings)
        
        return self
    
    def train(self):
        """Build user profiles based on listening history"""
        for user_id in self.user_item_matrix.index:
            user_plays = self.user_item_matrix.loc[user_id]
            played_tracks = user_plays[user_plays > 0]
            
            if len(played_tracks) > 0:
                played_track_ids = played_tracks.index.tolist()
                track_indices = [
                    self.tracks_df[self.tracks_df['trackId'] == tid].index[0]
                    for tid in played_track_ids
                    if tid in self.tracks_df['trackId'].values
                ]
                
                if track_indices:
                    # Weighted average based on play counts
                    weights = np.array([played_tracks[tid] for tid in played_track_ids])
                    weights = weights / weights.sum()
                    
                    user_embedding = np.average(
                        self.track_embeddings[track_indices],
                        axis=0,
                        weights=weights
                    )
                    
                    # Genre preferences
                    genre_prefs = {}
                    for tid in played_track_ids:
                        track = self.tracks_df[self.tracks_df['trackId'] == tid]
                        if not track.empty:
                            genre = track.iloc[0]['genre']
                            plays = user_plays[tid]
                            if genre in genre_prefs:
                                genre_prefs[genre] += plays
                            else:
                                genre_prefs[genre] = plays
                    
                    # Artist preferences
                    artist_prefs = {}
                    for tid in played_track_ids:
                        track = self.tracks_df[self.tracks_df['trackId'] == tid]
                        if not track.empty:
                            artist = track.iloc[0]['artist']
                            plays = user_plays[tid]
                            if artist in artist_prefs:
                                artist_prefs[artist] += plays
                            else:
                                artist_prefs[artist] = plays
                    
                    self.user_profiles[user_id] = {
                        'embedding': user_embedding,
                        'played_tracks': played_track_ids,
                        'total_plays': played_tracks.sum(),
                        'genre_preferences': genre_prefs,
                        'artist_preferences': artist_prefs,
                        'top_genres': sorted(genre_prefs.items(), 
                                           key=lambda x: x[1], 
                                           reverse=True)[:5]
                    }
        
        return self
    
    def get_collaborative_scores(self, user_id):
        """Collaborative filtering based on play counts"""
        if user_id not in self.user_item_matrix.index:
            return {}
        
        user_vector = self.user_item_matrix.loc[user_id].values.reshape(1, -1)
        
        # Use cosine similarity with play counts
        user_similarities = cosine_similarity(user_vector, self.user_item_matrix.values)[0]
        
        # Get similar users
        similar_users_idx = np.argsort(user_similarities)[-11:-1][::-1]
        similar_users = self.user_item_matrix.index[similar_users_idx]
        
        cf_scores = {}
        user_played = set(self.user_item_matrix.loc[user_id][self.user_item_matrix.loc[user_id] > 0].index)
        
        for similar_user in similar_users:
            sim_score = user_similarities[self.user_item_matrix.index.get_loc(similar_user)]
            similar_user_plays = self.user_item_matrix.loc[similar_user]
            
            for track_id, plays in similar_user_plays[similar_user_plays > 0].items():
                if track_id not in user_played:
                    if track_id not in cf_scores:
                        cf_scores[track_id] = []
                    # Weight by both similarity and play count
                    cf_scores[track_id].append(np.log1p(plays) * sim_score)
        
        cf_scores = {tid: np.mean(scores) for tid, scores in cf_scores.items()}
        return cf_scores
    
    def get_embedding_scores(self, user_id):
        """Content-based using audio feature embeddings"""
        if user_id not in self.user_profiles:
            return {}
        
        user_profile = self.user_profiles[user_id]
        user_embedding = user_profile['embedding']
        played_tracks = set(user_profile['played_tracks'])
        
        # Calculate similarity with all tracks
        embedding_scores = {}
        for idx, row in self.tracks_df.iterrows():
            track_id = row['trackId']
            if track_id not in played_tracks:
                track_embedding = self.track_embeddings[idx]
                similarity = cosine_similarity(
                    user_embedding.reshape(1, -1),
                    track_embedding.reshape(1, -1)
                )[0][0]
                
                # Boost by genre preference
                genre = row['genre']
                genre_boost = user_profile['genre_preferences'].get(genre, 0)
                genre_boost = np.log1p(genre_boost) / 10  # Normalize
                
                # Boost by artist preference
                artist = row['artist']
                artist_boost = user_profile['artist_preferences'].get(artist, 0)
                artist_boost = np.log1p(artist_boost) / 10
                
                embedding_scores[track_id] = similarity + 0.2 * genre_boost + 0.1 * artist_boost
        
        return embedding_scores
    
    def recommend(self, user_id, n_recommendations=10, alpha=0.4):
        """
        Hybrid recommendation
        alpha: weight for collaborative filtering
        """
        cf_scores = self.get_collaborative_scores(user_id)
        embedding_scores = self.get_embedding_scores(user_id)
        
        # Normalize
        if cf_scores:
            max_cf = max(cf_scores.values())
            if max_cf > 0:
                cf_scores = {k: v/max_cf for k, v in cf_scores.items()}
        
        if embedding_scores:
            max_emb = max(embedding_scores.values())
            if max_emb > 0:
                embedding_scores = {k: v/max_emb for k, v in embedding_scores.items()}
        
        # Combine
        all_items = set(cf_scores.keys()) | set(embedding_scores.keys())
        hybrid_scores = {}
        
        for item in all_items:
            cf_score = cf_scores.get(item, 0)
            emb_score = embedding_scores.get(item, 0)
            hybrid_scores[item] = alpha * cf_score + (1 - alpha) * emb_score
        
        # Get top recommendations
        top_items = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
        
        recommendations = []
        for track_id, score in top_items:
            track = self.tracks_df[self.tracks_df['trackId'] == track_id]
            if not track.empty:
                t = track.iloc[0]
                recommendations.append({
                    'item_id': int(track_id),
                    'title': t['title'],
                    'artist': t['artist'],
                    'album': t.get('album', 'N/A'),
                    'genre': t['genre'],
                    'duration': int(t.get('duration', 0)),
                    'score': float(score),
                    'domain': 'music'
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


if __name__ == "__main__":
    recommender = MusicRecommender(n_components=50)
    recommender.prepare_data('listening_history.csv', 'tracks.csv')
    recommender.train()
    recommender.save_model('music_recommender.pkl')
    
    user_id = 1
    recommendations = recommender.recommend(user_id, n_recommendations=10)
    
    print(f"Top 10 music recommendations for User {user_id}:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} by {rec['artist']} - {rec['genre']} (Score: {rec['score']:.3f})")