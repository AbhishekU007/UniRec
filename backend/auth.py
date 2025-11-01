"""
UniRec - User Authentication & Profile Management
Handles user registration, login, and preference collection
"""

import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
import json
import os

SECRET_KEY = "your-secret-key-change-in-production"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

class UserManager:
    def __init__(self, users_file='../data/users.json'):
        self.users_file = users_file
        self.users = self._load_users()
    
    def _load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_users(self):
        """Save users to JSON file"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def create_user(self, email: str, password: str, name: str, quiz_responses: dict):
        """Create a new user"""
        if email in self.users:
            return None, "Email already registered"
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Assign internal user ID (for recommendations)
        internal_user_id = len(self.users) + 1
        
        # Create user profile
        user = {
            'email': email,
            'password': hashed_password,
            'name': name,
            'internal_user_id': internal_user_id,
            'quiz_responses': quiz_responses,
            'preferences': self._extract_preferences(quiz_responses),
            'created_at': datetime.now().isoformat(),
            'last_login': datetime.now().isoformat()
        }
        
        self.users[email] = user
        self._save_users()
        
        return user, None
    
    def authenticate_user(self, email: str, password: str):
        """Authenticate user and return user data"""
        if email not in self.users:
            return None, "User not found"
        
        user = self.users[email]
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return None, "Incorrect password"
        
        # Update last login
        user['last_login'] = datetime.now().isoformat()
        self._save_users()
        
        return user, None
    
    def create_access_token(self, user_email: str):
        """Create JWT access token"""
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            'sub': user_email,
            'exp': expire
        }
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str):
        """Verify JWT token and return user email"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get('sub')
            if email is None:
                return None
            return email
        except jwt.PyJWTError:
            return None
    
    def get_user(self, email: str):
        """Get user by email"""
        return self.users.get(email)
    
    def _extract_preferences(self, quiz_responses: dict):
        """Extract preferences from quiz responses"""
        preferences = {
            'favorite_genres': quiz_responses.get('favorite_movie_genres', []),
            'favorite_music_genres': quiz_responses.get('favorite_music_genres', []),
            'shopping_categories': quiz_responses.get('shopping_interests', []),
            'learning_interests': quiz_responses.get('learning_topics', []),
            'experience_level': quiz_responses.get('experience_level', 'beginner'),
            'budget_range': quiz_responses.get('budget_range', 'medium')
        }
        return preferences
    
    def get_user_recommendations_id(self, email: str):
        """Get the internal user ID for recommendations"""
        user = self.users.get(email)
        if user:
            return user.get('internal_user_id')
        return None
    
    def update_preferences(self, email: str, new_preferences: dict):
        """Update user preferences"""
        if email in self.users:
            self.users[email]['preferences'].update(new_preferences)
            self._save_users()
            return True
        return False
