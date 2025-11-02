"""
UniRec - Course Recommendation Model
Content-Based with Skill Matching
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

from interaction_tracker import InteractionTracker

class CourseRecommender:
    def __init__(self):
        self.user_item_matrix = None
        self.courses_df = None
        self.course_category_map = None
        self.enrollments_df = None  # Store enrollments for sparse data detection
        self.user_profiles = {}
        self.tfidf_vectorizer = None
        self.item_similarity = None
        self.difficulty_map = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
        
    def prepare_data(self, enrollments_path, courses_path):
        """
        Load course data
        enrollments: user_id, course_id, progress, rating, enrollment_date
        courses: course_id, title, category, skill, level, platform, duration_hours, rating, num_students, price
        """
        enrollments = pd.read_csv(enrollments_path)
        self.enrollments_df = enrollments  # Store for later use
        self.courses_df = pd.read_csv(courses_path)

        # Cache category lookups for faster preference weighting
        self.course_category_map = {
            int(row['course_id']): str(row['category']).lower().strip()
            for _, row in self.courses_df.iterrows()
        }
        
        # Map skill to subcategory and level to difficulty for compatibility
        if 'skill' in self.courses_df.columns:
            self.courses_df['subcategory'] = self.courses_df['skill']
        else:
            self.courses_df['subcategory'] = ''
            
        if 'level' in self.courses_df.columns:
            self.courses_df['difficulty'] = self.courses_df['level']
        else:
            self.courses_df['difficulty'] = 'Beginner'
        
        # Create user-item matrix (using progress + rating)
        # Weight: 1 for enrolled, +progress/100 for completion, +rating/5 for quality
        enrollments['interaction_score'] = (
            1 + 
            enrollments['progress'].fillna(0) / 100.0 + 
            enrollments['rating'].fillna(0) / 5.0
        )
        
        self.user_item_matrix = enrollments.pivot_table(
            index='user_id',
            columns='course_id',
            values='interaction_score',
            fill_value=0
        )
        
        # Prepare course features
        topics = self.courses_df['topics'].fillna('') if 'topics' in self.courses_df.columns else ''
        description = self.courses_df['description'].fillna('') if 'description' in self.courses_df.columns else ''
        
        self.courses_df['combined_features'] = (
            self.courses_df['title'].fillna('') + ' ' +
            self.courses_df['category'].fillna('') + ' ' +
            self.courses_df['subcategory'].fillna('') + ' ' +
            (topics if isinstance(topics, str) else topics) + ' ' +
            (description if isinstance(description, str) else description)
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
        # Create course_id to index lookup for faster access
        course_id_to_idx = {cid: idx for idx, cid in enumerate(self.courses_df['course_id'])}
        
        for user_id in self.user_item_matrix.index:
            user_interactions = self.user_item_matrix.loc[user_id]
            enrolled_courses = user_interactions[user_interactions > 0]
            
            if len(enrolled_courses) > 0:
                enrolled_course_ids = enrolled_courses.index.tolist()
                course_indices = [course_id_to_idx[cid] for cid in enrolled_course_ids if cid in course_id_to_idx]
                
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
                        if cid in course_id_to_idx:
                            c = self.courses_df.iloc[course_id_to_idx[cid]]
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
            course_id = row['course_id']
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
    
    def recommend(self, user_id, n_recommendations=10, alpha=0.3, preferred_topics=None):
        """
        Hybrid recommendation with topic filtering
        alpha: weight for collaborative filtering (content is more important for courses)
        preferred_topics: list of learning topics to filter by (if provided)
        """
        cf_scores = self.get_collaborative_scores(user_id)
        content_scores = self.get_content_scores(user_id)

        # Ensure category map exists after loading from pickle
        if getattr(self, 'course_category_map', None) is None and self.courses_df is not None:
            self.course_category_map = {
                int(row['course_id']): str(row['category']).lower().strip()
                for _, row in self.courses_df.iterrows()
            }

        preferred_topics_lower = []
        topic_weights = {}

        interactions_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'data', 'interactions.json')
        )
        tracker = None
        try:
            tracker = InteractionTracker(interactions_file=interactions_path)
        except Exception:
            tracker = None

        behavior_priorities = []
        if tracker is not None:
            try:
                behavior_updates = tracker.get_preference_updates(user_id)
                for topic in behavior_updates.get('learning_interests', []) or []:
                    lt = topic.lower().strip()
                    if lt and lt not in behavior_priorities:
                        behavior_priorities.append(lt)
            except Exception:
                behavior_priorities = []

        if preferred_topics:
            preferred_topics_lower = [t.lower().strip() for t in preferred_topics]
        else:
            preferred_topics_lower = []

        if behavior_priorities:
            merged_topics = []
            for topic in behavior_priorities + preferred_topics_lower:
                if topic and topic not in merged_topics:
                    merged_topics.append(topic)
            preferred_topics_lower = merged_topics

        if preferred_topics_lower:
            total_topics = len(preferred_topics_lower)
            if total_topics:
                # Highest-ranked topic gets weight 1.0, descending afterwards
                for index, topic in enumerate(preferred_topics_lower):
                    topic_weights[topic] = (total_topics - index) / total_topics
        
        # Check if user has sparse data in this topic
        # If filtered topics are specified, check enrollment count in those topics
        user_has_sparse_data = False
        if preferred_topics_lower and user_id in self.user_profiles and self.enrollments_df is not None:
            # Count how many enrollments the user has in the preferred topics
            user_enrollments = self.enrollments_df[self.enrollments_df['user_id'] == user_id]
            enrolled_course_ids = user_enrollments['course_id'].tolist()
            enrolled_courses = self.courses_df[self.courses_df['course_id'].isin(enrolled_course_ids)]
            
            # Normalize topics for comparison
            # Count enrollments in preferred topics
            topic_enrollment_count = 0
            for _, course in enrolled_courses.iterrows():
                if str(course['category']).lower().strip() in preferred_topics_lower:
                    topic_enrollment_count += 1
            
            # If user has less than 3 enrollments in this topic, favor content-based
            if topic_enrollment_count < 3:
                user_has_sparse_data = True
                alpha = 0.1  # Heavily favor content-based (90% content, 10% collaborative)
        
        # Normalize
        if cf_scores:
            max_cf = max(cf_scores.values())
            if max_cf > 0:
                cf_scores = {k: v/max_cf for k, v in cf_scores.items()}
        
        if content_scores:
            max_content = max(content_scores.values())
            if max_content > 0:
                content_scores = {k: v/max_content for k, v in content_scores.items()}
        
        # Combine (favor content for courses, even more so for sparse data)
        all_items = set(cf_scores.keys()) | set(content_scores.keys())
        hybrid_scores = {}
        
        for item in all_items:
            cf_score = cf_scores.get(item, 0)
            content_score = content_scores.get(item, 0)
            base_score = alpha * cf_score + (1 - alpha) * content_score

            # Apply topic weighting so the most-preferred topics surface first
            topic_weight = 0
            if self.course_category_map and item in self.course_category_map:
                topic_weight = topic_weights.get(self.course_category_map[item], 0)

            # Up to 60% boost based on topic rank
            hybrid_scores[item] = base_score * (1 + 0.6 * topic_weight)
        
        # Filter by topic if preferred topics specified
        if preferred_topics_lower:
            filtered_scores = {}
            for course_id, score in hybrid_scores.items():
                course = self.courses_df[self.courses_df['course_id'] == course_id]
                if not course.empty:
                    course_category = str(course.iloc[0]['category']).lower().strip()
                    # EXACT MATCH: Check if course category exactly matches any preferred topic
                    if course_category in preferred_topics_lower:
                        filtered_scores[course_id] = score
            
            # If filtering left us with very few results, add ALL courses from preferred topics
            if len(filtered_scores) < n_recommendations:
                # Get all courses matching preferred topics
                for _, course in self.courses_df.iterrows():
                    course_id = course['course_id']
                    course_category = str(course['category']).lower().strip()
                    if course_category in preferred_topics_lower and course_id not in filtered_scores:
                        # Give it a base score if not already scored
                        filtered_scores[int(course_id)] = 0.5
            
            hybrid_scores = filtered_scores if filtered_scores else hybrid_scores
        
        # Get top recommendations (get MORE to ensure we have enough variety)
        top_items = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)[:n_recommendations * 3]
        
        # Normalize scores to 0-1 range before creating recommendations
        if top_items:
            max_score = max(score for _, score in top_items)
            if max_score > 0:
                top_items = [(course_id, score / max_score) for course_id, score in top_items]
        
        recommendation_dicts = []
        for course_id, score in top_items:
            course = self.courses_df[self.courses_df['course_id'] == course_id]
            if not course.empty:
                c = course.iloc[0]
                recommendation_dicts.append({
                    'course_id': int(course_id),
                    'item_id': int(course_id),
                    'title': c['title'],
                    'instructor': c.get('instructor', 'N/A'),
                    'category': c['category'],
                    'subcategory': c.get('subcategory', 'N/A'),
                    'difficulty': c.get('difficulty', 'Beginner'),
                    'duration': int(c.get('duration', 0)),
                    'score': float(score),  # Now properly normalized to 0-1
                    'domain': 'courses'
                })

        # Apply reinforcement-learning boost so recent likes surface instantly
        if tracker is not None:
            try:
                recommendation_dicts = tracker.apply_reinforcement_boost(
                    user_id,
                    recommendation_dicts,
                    domain='courses',
                    boost_factor=0.5
                )
                
                # Re-normalize scores after RL boost to keep them 0-1
                if recommendation_dicts:
                    max_score = max(rec.get('score', 0) for rec in recommendation_dicts)
                    if max_score > 1.0:
                        for rec in recommendation_dicts:
                            rec['score'] = rec.get('score', 0) / max_score
            except Exception:
                pass

        # Rebalance to honor topic weights so behavior/preference shifts replace other topics
        if preferred_topics_lower:
            topic_buckets = {topic: [] for topic in preferred_topics_lower}
            other_items = []
            topic_reinforcement = {}
            for rec in recommendation_dicts:
                category = str(rec.get('category', '')).lower().strip()
                if category in topic_buckets:
                    topic_buckets[category].append(rec)
                    topic_reinforcement[category] = max(
                        topic_reinforcement.get(category, 0),
                        rec.get('rl_boost', 0)
                    )
                else:
                    other_items.append(rec)

            dynamic_weights = {}
            for topic in preferred_topics_lower:
                base_weight = topic_weights.get(topic, 1.0)
                reinforcement = topic_reinforcement.get(topic, 0) * 2  # amplify immediate likes
                dynamic_weights[topic] = base_weight + reinforcement

            total_weight = sum(dynamic_weights.values()) or len(preferred_topics_lower)
            quotas = {}
            for topic in preferred_topics_lower:
                weight = dynamic_weights.get(topic, 1.0)
                quotas[topic] = max(1, round((weight / total_weight) * n_recommendations))

            current_total = sum(quotas.values())
            if current_total > n_recommendations:
                for topic in reversed(preferred_topics_lower):
                    if current_total <= n_recommendations:
                        break
                    if quotas[topic] > 1:
                        quotas[topic] -= 1
                        current_total -= 1

            topic_index = 0
            while current_total < n_recommendations and preferred_topics_lower:
                topic = preferred_topics_lower[topic_index % len(preferred_topics_lower)]
                quotas[topic] += 1
                current_total += 1
                topic_index += 1

            max_quota_total = sum(quotas.values())
            round_robin_total = min(max_quota_total, n_recommendations)
            topic_positions = {topic: 0 for topic in preferred_topics_lower}
            rebalanced = []

            while len(rebalanced) < round_robin_total:
                for topic in preferred_topics_lower:
                    if len(rebalanced) >= round_robin_total:
                        break
                    quota = quotas.get(topic, 0)
                    bucket = topic_buckets.get(topic, [])
                    index = topic_positions[topic]
                    if index < quota and index < len(bucket):
                        rebalanced.append(bucket[index])
                    topic_positions[topic] = index + 1

            remainder = []
            for topic in preferred_topics_lower:
                bucket = topic_buckets.get(topic, [])
                index = topic_positions.get(topic, 0)
                remainder.extend(bucket[index:])
            remainder.extend(other_items)

            rebalanced.extend(remainder)
            recommendation_dicts = rebalanced

        # Trim after reinforcement adjustments
        return recommendation_dicts[:n_recommendations]
    
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