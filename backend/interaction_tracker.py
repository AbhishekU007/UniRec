"""
Interaction Tracker for Reinforcement Learning
Tracks user interactions and uses them to improve recommendations
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
import numpy as np


class InteractionTracker:
    """Tracks and analyzes user interactions for reinforcement learning"""
    
    def __init__(self, interactions_file='../data/interactions.json'):
        self.interactions_file = interactions_file
        self.interactions = self._load_interactions()
        
    def _load_interactions(self) -> List[Dict]:
        """Load interactions from file"""
        if os.path.exists(self.interactions_file):
            try:
                with open(self.interactions_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_interactions(self):
        """Save interactions to file"""
        os.makedirs(os.path.dirname(self.interactions_file), exist_ok=True)
        with open(self.interactions_file, 'w') as f:
            json.dump(self.interactions, f, indent=2)
    
    def log_interaction(self, user_id: int, item_id: int, domain: str, 
                       action_type: str, metadata: Optional[Dict] = None):
        """
        Log a user interaction
        
        Args:
            user_id: User identifier
            item_id: Item identifier (track_id, movie_id, product_id, course_id)
            domain: Domain (music, movies, products, courses)
            action_type: Type of interaction (view, click, like, dislike, rate, purchase, enroll, complete)
            metadata: Additional metadata (rating, time_spent, etc.)
        """
        interaction = {
            'user_id': user_id,
            'item_id': item_id,
            'domain': domain,
            'action_type': action_type,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.interactions.append(interaction)
        self._save_interactions()
        
        return interaction
    
    def get_user_interactions(self, user_id: int, domain: Optional[str] = None,
                             days: Optional[int] = None) -> List[Dict]:
        """Get interactions for a specific user"""
        user_interactions = [i for i in self.interactions if i['user_id'] == user_id]
        
        if domain:
            user_interactions = [i for i in user_interactions if i['domain'] == domain]
        
        if days:
            cutoff = datetime.now() - timedelta(days=days)
            user_interactions = [
                i for i in user_interactions 
                if datetime.fromisoformat(i['timestamp']) > cutoff
            ]
        
        return user_interactions
    
    def calculate_item_score(self, user_id: int, item_id: int, domain: str) -> float:
        """
        Calculate reinforcement learning score for an item based on past interactions
        
        Returns a score between -1 and 1:
        - Positive: User has shown interest
        - Negative: User has shown disinterest
        - Zero: No interaction history
        """
        interactions = [
            i for i in self.interactions 
            if i['user_id'] == user_id and i['item_id'] == item_id and i['domain'] == domain
        ]
        
        if not interactions:
            return 0.0
        
        # Weight different actions
        action_weights = {
            'view': 0.1,
            'click': 0.3,
            'like': 0.8,
            'dislike': -0.8,
            'rate': 0.0,  # Will use actual rating
            'purchase': 1.0,
            'enroll': 0.7,
            'complete': 1.0,
            'skip': -0.3,
            'time_spent': 0.0  # Will calculate based on duration
        }
        
        total_score = 0.0
        for interaction in interactions:
            action = interaction['action_type']
            metadata = interaction.get('metadata', {})
            
            if action == 'rate' and 'rating' in metadata:
                # Normalize rating (assume 1-5 scale) to -1 to 1
                rating = metadata['rating']
                total_score += (rating - 3) / 2  # 5->1, 4->0.5, 3->0, 2->-0.5, 1->-1
            elif action == 'time_spent' and 'duration' in metadata:
                # More time = more interest (cap at 5 minutes)
                duration = min(metadata['duration'], 300)
                total_score += duration / 300 * 0.5
            else:
                total_score += action_weights.get(action, 0.0)
        
        # Normalize to -1 to 1
        return max(-1.0, min(1.0, total_score))
    
    def get_preference_updates(self, user_id: int, days: int = 30) -> Dict[str, Dict]:
        """
        Analyze recent interactions to suggest preference updates
        
        Returns updated preferences based on actual behavior
        """
        recent_interactions = self.get_user_interactions(user_id, days=days)
        
        if not recent_interactions:
            return {}
        
        updates = {
            'favorite_music_genres': {},
            'favorite_genres': {},  # Movie genres
            'shopping_categories': {},
            'learning_interests': {}
        }
        
        # Count positive interactions by category
        for interaction in recent_interactions:
            if interaction['action_type'] in ['like', 'purchase', 'enroll', 'complete', 'rate']:
                domain = interaction['domain']
                metadata = interaction.get('metadata', {})
                
                # Extract category/genre from metadata
                if domain == 'music' and 'genre' in metadata:
                    genre = metadata['genre']
                    updates['favorite_music_genres'][genre] = \
                        updates['favorite_music_genres'].get(genre, 0) + 1
                
                elif domain == 'movies' and 'genres' in metadata:
                    # Handle pipe-separated genres
                    genres = metadata['genres'].split('|')
                    for genre in genres:
                        genre = genre.strip()
                        updates['favorite_genres'][genre] = \
                            updates['favorite_genres'].get(genre, 0) + 1
                
                elif domain == 'products' and 'category' in metadata:
                    category = metadata['category']
                    updates['shopping_categories'][category] = \
                        updates['shopping_categories'].get(category, 0) + 1
                
                elif domain == 'courses' and 'category' in metadata:
                    category = metadata['category']
                    updates['learning_interests'][category] = \
                        updates['learning_interests'].get(category, 0) + 1
        
        # Convert counts to lists of preferences (top categories)
        for key in updates:
            if updates[key]:
                # Sort by count and take top items
                sorted_prefs = sorted(updates[key].items(), key=lambda x: x[1], reverse=True)
                updates[key] = [pref[0] for pref in sorted_prefs[:5]]  # Top 5
            else:
                updates[key] = None
        
        # Remove empty updates
        return {k: v for k, v in updates.items() if v}
    
    def get_exploration_candidates(self, user_id: int, domain: str, 
                                   all_items: List[int], n: int = 5) -> List[int]:
        """
        Select items for exploration (items user hasn't interacted with much)
        Uses epsilon-greedy strategy
        """
        user_interactions = self.get_user_interactions(user_id, domain=domain)
        interacted_items = set(i['item_id'] for i in user_interactions)
        
        # Find items not yet explored
        unexplored = [item for item in all_items if item not in interacted_items]
        
        if len(unexplored) >= n:
            return np.random.choice(unexplored, size=n, replace=False).tolist()
        else:
            # If not enough unexplored, add some less-interacted items
            item_counts = {}
            for interaction in user_interactions:
                item_id = interaction['item_id']
                item_counts[item_id] = item_counts.get(item_id, 0) + 1
            
            # Sort by interaction count (ascending)
            less_explored = sorted(interacted_items, key=lambda x: item_counts[x])[:n-len(unexplored)]
            
            return unexplored + less_explored
    
    def calculate_diversity_score(self, recommendations: List[Dict]) -> float:
        """
        Calculate diversity score for a set of recommendations
        Higher is more diverse
        """
        if not recommendations:
            return 0.0
        
        # Check genre/category diversity
        categories = set()
        for rec in recommendations:
            metadata = rec.get('metadata', {})
            if 'genre' in metadata:
                categories.add(metadata['genre'])
            elif 'genres' in metadata:
                categories.update(metadata['genres'].split('|'))
            elif 'category' in metadata:
                categories.add(metadata['category'])
        
        # Diversity = number of unique categories / total recommendations
        return len(categories) / len(recommendations)
    
    def apply_reinforcement_boost(self, user_id: int, recommendations: List[Dict],
                                  domain: str, boost_factor: float = 0.3) -> List[Dict]:
        """
        Apply reinforcement learning boost to recommendation scores
        
        Args:
            user_id: User ID
            recommendations: List of recommendations with scores
            domain: Domain
            boost_factor: How much to boost/penalize based on interactions (0-1)
        
        Returns:
            Updated recommendations with adjusted scores
        """
        for rec in recommendations:
            item_id = rec.get('id') or rec.get('track_id') or rec.get('movie_id') or \
                     rec.get('product_id') or rec.get('course_id')
            
            if item_id:
                rl_score = self.calculate_item_score(user_id, item_id, domain)
                
                # Adjust the recommendation score
                if 'score' in rec:
                    original_score = rec['score']
                    # Boost or penalize based on interaction history
                    rec['score'] = original_score + (rl_score * boost_factor)
                    rec['rl_boost'] = rl_score * boost_factor
        
        # Re-sort by updated scores
        recommendations.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return recommendations
    
    def get_interaction_stats(self, user_id: int) -> Dict:
        """Get statistics about user interactions"""
        interactions = self.get_user_interactions(user_id)
        
        if not interactions:
            return {
                'total_interactions': 0,
                'by_domain': {},
                'by_action': {},
                'engagement_score': 0.0
            }
        
        by_domain = {}
        by_action = {}
        
        for interaction in interactions:
            domain = interaction['domain']
            action = interaction['action_type']
            
            by_domain[domain] = by_domain.get(domain, 0) + 1
            by_action[action] = by_action.get(action, 0) + 1
        
        # Calculate engagement score (more interactions = higher engagement)
        engagement_score = min(1.0, len(interactions) / 100)
        
        return {
            'total_interactions': len(interactions),
            'by_domain': by_domain,
            'by_action': by_action,
            'engagement_score': engagement_score,
            'days_active': self._calculate_days_active(interactions)
        }
    
    def _calculate_days_active(self, interactions: List[Dict]) -> int:
        """Calculate number of unique days user was active"""
        if not interactions:
            return 0
        
        dates = set()
        for interaction in interactions:
            timestamp = datetime.fromisoformat(interaction['timestamp'])
            dates.add(timestamp.date())
        
        return len(dates)
