"""
UniRec - Course Recommendation Model
Content-Based with Skill Matching
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

class CourseRecommender:
    def __init__(self):
        self.user_item_matrix = None
        self.courses_df = None
        self.user_profiles = {}
        self.tfidf_vectorizer = None
        self.item_similarity = None
        self.difficulty_map = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
        
    def prepare_data(self, enrollments_path, courses_path):
        """
        Load course data
        enrollments: userId, courseId, completed, rating, progress
        courses: courseId, title, instructor, category, subcategory, difficulty, duration, topics, description
        """
        enrollments = pd.read_csv(enrollments_path)
        self.courses_df = pd.read_csv(courses_path)
        
        # Create user-item matrix (using completion + rating)
        # Weight: 1 for enrolled, +1 for completed, +rating/5 for quality
        enrollments['interaction_score'] = (
            1 + 
            enrollments['completed'].fillna(0) + 
            enrollments['rating'].fillna(0) / 5.0
        )
        
        self.user_item_matrix = enrollments.pivot_table(
            index='userId',
            columns='courseId',
            values='interaction_score',
            fill_value=0
        )
        
        # Prepare course features
        self.courses_df['combined_features'] = (
            self.courses_df['title'].fillna('') + ' ' +
            self.courses_df['category'].fillna('') + ' ' +
            self.courses_df['subcategory'].fillna('') + ' ' +
            self.courses_df['topics'].fillna('') + ' ' +
            self.courses_df['description'].fillna('')
        )
        
        # Create TF-IDF features
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=200,
            stop_words='english',
            ngram_range=(1, 2)
        )
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.courses_df['combined_features'])
        
        # Calculate course similarity
        self.item_similarity = cosine_similarity(tfidf_matrix)
        
        return self
    
    def train(self):
        """Build user skill profiles"""
        for user_id in self.user_item_matrix.index:
            user_interactions = self.user_item_matrix.loc[user_id]
            enrolled_courses = user_interactions[user_interactions > 0]
            
            if len(enrolled_courses) > 0:
                enrolled_course_ids = enrolled_courses.index.tolist()
                course_indices = [
                    self.courses_df[self.courses_df['courseId'] == cid].index[0]
                    for cid in enrolled_course_ids
                    if cid in self.courses_df['courseId'].values
                ]
                
                if course_indices:
                    # Weighted user embedding based on interaction strength
                    weights = enrolled_courses.values
                    weights = weights / weights.sum()
                    
                    user_embedding = np.average(
                        self.item_similarity[course_indices],
                        axis=0,
                        weights=weights
                    )
                    
                    # Extract skill interests
                    category_interests = {}
                    subcategory_interests = {}
                    difficulty_levels = []
                    
                    for cid in enrolled_course_ids:
                        course = self.courses_df[self.courses_df['courseId'] == cid]
                        if not course.empty:
                            c = course.iloc[0]
                            interaction = user_interactions[cid]
                            
                            # Category interests
                            category = c['category']
                            if category in category_interests:
                                category_interests[category] += interaction
                            else:
                                category_interests[category] = interaction
                            
                            # Subcategory interests
                            subcategory = c.get('subcategory', 'N/A')
                            if subcategory in subcategory_interests:
                                subcategory_interests[subcategory] += interaction
                            else:
                                subcategory_interests[subcategory] = interaction
                            
                            # Track difficulty progression
                            difficulty = c.get('difficulty', 'Beginner')
                            difficulty_levels.append(self.difficulty_map.get(difficulty, 1))
                    
                    # Infer user's current skill level
                    avg_difficulty = np.mean(difficulty_levels) if difficulty_levels else 1
                    
                    self.user_profiles[user_id] = {
                        'embedding': user_embedding,
                        'enrolled_courses': enrolled_course_ids,
                        'category_interests': category_interests,
                        'subcategory_interests': subcategory_interests,
                        'skill_level': avg_difficulty,
                        'top_categories': sorted(category_interests.items(),
                                                key=lambda x: x[1],
                                                reverse=True)[:3]
                    }
        
        return self
    
    def get_collaborative_scores(self, user_id):
        """Collaborative filtering"""
        if user_id not in self.user_item_matrix.index:
            return {}
        
        user_vector = self.user_item_matrix.loc[user_id].values.reshape(1, -1)
        user_similarities = cosine_similarity(user_vector, self.user_item_matrix.values)[0]
        
        similar_users_idx = np.argsort(user_similarities)[-11:-1][::-1]
        similar_users = self.user_item_matrix.index[similar_users_idx]
        
        cf_scores = {}
        user_enrolled = set(self.user_item_matrix.loc[user_id][self.user_item_matrix.loc[user_id] > 0].index)
        
        for similar_user in similar_users:
            sim_score = user_similarities[self.user_item_matrix.index.get_loc(similar_user)]
            similar_user_courses = self.user_item_matrix.loc[similar_user]
            
            for course_id, score in similar_user_courses[similar_user_courses > 0].items():
                if course_id not in user_enrolled:
                    if course_id not in cf_scores:
                        cf_scores[course_id] = []
                    cf_scores[course_id].append(score * sim_score)
        
        cf_scores = {cid: np.mean(scores) for cid, scores in cf_scores.items()}
        return cf_scores
    
    def get_content_scores(self, user_id):
        """Content-based filtering with skill matching"""
        if user_id not in self.user_profiles:
            return {}
        
        user_profile = self.user_profiles[user_id]
        user_embedding = user_profile['embedding']
        enrolled_courses = set(user_profile['enrolled_courses'])
        user_skill_level = user_profile['skill_level']
        
        content_scores = {}
        for idx, row in self.courses_df.iterrows():
            course_id = row['courseId']
            if course_id not in enrolled_courses:
                # Content similarity
                similarity = user_embedding[idx]
                
                # Category boost
                category = row['category']
                category_boost = user_profile['category_interests'].get(category, 0) / 10
                
                # Subcategory boost
                subcategory = row.get('subcategory', 'N/A')
                subcategory_boost = user_profile['subcategory_interests'].get(subcategory, 0) / 10
                
                # Difficulty matching (prefer appropriate challenge)
                course_difficulty = self.difficulty_map.get(row.get('difficulty', 'Beginner'), 1)
                difficulty_diff = abs(course_difficulty - user_skill_level)
                
                # Penalize if too easy or too hard
                if difficulty_diff > 1:
                    difficulty_penalty = 0.3
                elif difficulty_diff == 1:
                    difficulty_penalty = 0  # Perfect progression
                else:
                    difficulty_penalty = 0.1  # Slight penalty for same level
                
                score = (
                    similarity +
                    0.3 * category_boost +
                    0.2 * subcategory_boost -
                    difficulty_penalty
                )
                
                content_scores[course_id] = max(0, score)  # Ensure non-negative
        
        return content_scores
    
    def recommend(self, user_id, n_recommendations=10, alpha=0.3):
        """
        Hybrid recommendation
        alpha: weight for collaborative filtering (content is more important for courses)
        """
        cf_scores = self.get_collaborative_scores(user_id)
        content_scores = self.get_content_scores(user_id)
        
        # Normalize
        if cf_scores:
            max_cf = max(cf_scores.values())
            if max_cf > 0:
                cf_scores = {k: v/max_cf for k, v in cf_scores.items()}
        
        if content_scores:
            max_content = max(content_scores.values())
            if max_content > 0:
                content_scores = {k: v/max_content for k, v in content_scores.items()}
        
        # Combine (favor content for courses)
        all_items = set(cf_scores.keys()) | set(content_scores.keys())
        hybrid_scores = {}
        
        for item in all_items:
            cf_score = cf_scores.get(item, 0)
            content_score = content_scores.get(item, 0)
            hybrid_scores[item] = alpha * cf_score + (1 - alpha) * content_score
        
        # Get top recommendations
        top_items = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
        
        recommendations = []
        for course_id, score in top_items:
            course = self.courses_df[self.courses_df['courseId'] == course_id]
            if not course.empty:
                c = course.iloc[0]
                recommendations.append({
                    'item_id': int(course_id),
                    'title': c['title'],
                    'instructor': c.get('instructor', 'N/A'),
                    'category': c['category'],
                    'subcategory': c.get('subcategory', 'N/A'),
                    'difficulty': c.get('difficulty', 'Beginner'),
                    'duration': int(c.get('duration', 0)),
                    'score': float(score),
                    'domain': 'courses'
                })
        
        return recommendations
    
    def get_user_embedding(self, user_id):
        """Get user embedding for unified profile"""
        if user_id in self.user_profiles:
            profile = self.user_profiles[user_id]
            return {
                'embedding': profile['embedding'],
                'skill_level': profile['skill_level'],
                'interests': profile['category_interests']
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
    recommender = CourseRecommender()
    recommender.prepare_data('enrollments.csv', 'courses.csv')
    recommender.train()
    recommender.save_model('course_recommender.pkl')
    
    user_id = 1
    recommendations = recommender.recommend(user_id, n_recommendations=10)
    
    print(f"Top 10 course recommendations for User {user_id}:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} - {rec['category']} ({rec['difficulty']}) - Score: {rec['score']:.3f}")