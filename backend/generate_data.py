"""
UniRec - Synthetic Data Generator
Generates sample data for all domains for testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

class DataGenerator:
    def __init__(self, n_users=1000):
        self.n_users = n_users
        
    def generate_movie_data(self, n_movies=5000, n_ratings=50000):
        """Generate MovieLens-style data"""
        print("Generating movie data...")
        
        # Movie genres
        genres = ['Action', 'Comedy', 'Drama', 'Thriller', 'Sci-Fi', 'Romance', 
                 'Horror', 'Documentary', 'Animation', 'Adventure']
        
        # Generate movies
        movies_data = []
        for i in range(1, n_movies + 1):
            year = random.randint(1980, 2024)
            selected_genres = random.sample(genres, random.randint(1, 3))
            movies_data.append({
                'movieId': i,
                'title': f'Movie {i} ({year})',
                'genres': '|'.join(selected_genres)
            })
        
        movies_df = pd.DataFrame(movies_data)
        
        # Generate ratings
        ratings_data = []
        for _ in range(n_ratings):
            user_id = random.randint(1, self.n_users)
            movie_id = random.randint(1, n_movies)
            rating = random.choice([1, 2, 3, 4, 5])
            timestamp = int((datetime.now() - timedelta(days=random.randint(0, 730))).timestamp())
            
            ratings_data.append({
                'userId': user_id,
                'movieId': movie_id,
                'rating': rating,
                'timestamp': timestamp
            })
        
        ratings_df = pd.DataFrame(ratings_data)
        
        # Save
        movies_df.to_csv('data/movies.csv', index=False)
        ratings_df.to_csv('data/ratings.csv', index=False)
        
        print(f"✓ Generated {len(movies_df)} movies and {len(ratings_df)} ratings")
        return movies_df, ratings_df
    
    def generate_product_data(self, n_products=3000, n_reviews=30000):
        """Generate e-commerce product data"""
        print("Generating product data...")
        
        categories = ['Electronics', 'Clothing', 'Books', 'Home & Kitchen', 
                     'Sports', 'Beauty', 'Toys', 'Health', 'Automotive']
        brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE', 'Generic']
        
        # Generate products
        products_data = []
        for i in range(1, n_products + 1):
            category = random.choice(categories)
            brand = random.choice(brands)
            price = round(random.uniform(10, 500), 2)
            
            products_data.append({
                'productId': i,
                'title': f'{category} Product {i}',
                'category': category,
                'brand': brand,
                'price': price
            })
        
        products_df = pd.DataFrame(products_data)
        
        # Generate reviews
        reviews_data = []
        for _ in range(n_reviews):
            user_id = random.randint(1, self.n_users)
            product_id = random.randint(1, n_products)
            rating = random.choice([1, 2, 3, 4, 5])
            timestamp = int((datetime.now() - timedelta(days=random.randint(0, 365))).timestamp())
            
            reviews_data.append({
                'userId': user_id,
                'productId': product_id,
                'rating': rating,
                'timestamp': timestamp
            })
        
        reviews_df = pd.DataFrame(reviews_data)
        
        # Save
        products_df.to_csv('data/products.csv', index=False)
        reviews_df.to_csv('data/product_reviews.csv', index=False)
        
        print(f"✓ Generated {len(products_df)} products and {len(reviews_df)} reviews")
        return products_df, reviews_df
    
    def generate_music_data(self, n_tracks=8000, n_listens=60000):
        """Generate music streaming data"""
        print("Generating music data...")
        
        genres = ['Pop', 'Rock', 'Hip Hop', 'Electronic', 'Jazz', 'Classical', 
                 'Country', 'R&B', 'Metal', 'Folk']
        artists = [f'Artist {i}' for i in range(1, 201)]
        
        # Generate tracks
        tracks_data = []
        for i in range(1, n_tracks + 1):
            genre = random.choice(genres)
            artist = random.choice(artists)
            album = f'Album {random.randint(1, 500)}'
            duration = random.randint(120, 360)  # 2-6 minutes
            tempo = random.uniform(60, 180)
            energy = random.uniform(0, 1)
            valence = random.uniform(0, 1)
            danceability = random.uniform(0, 1)
            acousticness = random.uniform(0, 1)
            instrumentalness = random.uniform(0, 1)
            loudness = random.uniform(-60, 0)
            
            tracks_data.append({
                'trackId': i,
                'title': f'Song {i}',
                'artist': artist,
                'album': album,
                'genre': genre,
                'duration': duration,
                'tempo': tempo,
                'energy': energy,
                'valence': valence,
                'danceability': danceability,
                'acousticness': acousticness,
                'instrumentalness': instrumentalness,
                'loudness': loudness
            })
        
        tracks_df = pd.DataFrame(tracks_data)
        
        # Generate listening history
        history_data = []
        for _ in range(n_listens):
            user_id = random.randint(1, self.n_users)
            track_id = random.randint(1, n_tracks)
            play_count = random.randint(1, 50)
            timestamp = int((datetime.now() - timedelta(days=random.randint(0, 365))).timestamp())
            
            history_data.append({
                'userId': user_id,
                'trackId': track_id,
                'playCount': play_count,
                'timestamp': timestamp
            })
        
        history_df = pd.DataFrame(history_data)
        
        # Save
        tracks_df.to_csv('data/tracks.csv', index=False)
        history_df.to_csv('data/listening_history.csv', index=False)
        
        print(f"✓ Generated {len(tracks_df)} tracks and {len(history_df)} listening records")
        return tracks_df, history_df
    
    def generate_course_data(self, n_courses=1500, n_enrollments=20000):
        """Generate online course data"""
        print("Generating course data...")
        
        categories = ['Programming', 'Data Science', 'Business', 'Design', 
                     'Marketing', 'Photography', 'Music', 'Health', 'Language']
        subcategories = {
            'Programming': ['Python', 'JavaScript', 'Java', 'Web Development'],
            'Data Science': ['Machine Learning', 'Data Analysis', 'Statistics'],
            'Business': ['Management', 'Finance', 'Entrepreneurship'],
            'Design': ['Graphic Design', 'UI/UX', '3D Modeling'],
            'Marketing': ['Digital Marketing', 'SEO', 'Social Media'],
        }
        difficulties = ['Beginner', 'Intermediate', 'Advanced']
        
        # Generate courses
        courses_data = []
        for i in range(1, n_courses + 1):
            category = random.choice(categories)
            subcategory = random.choice(subcategories.get(category, ['General']))
            difficulty = random.choice(difficulties)
            duration = random.randint(5, 100)  # hours
            instructor = f'Instructor {random.randint(1, 100)}'
            
            topics = f'{category}, {subcategory}, {difficulty}'
            description = f'Learn {subcategory} in this comprehensive {difficulty.lower()} course.'
            
            courses_data.append({
                'courseId': i,
                'title': f'{subcategory} {difficulty} Course {i}',
                'instructor': instructor,
                'category': category,
                'subcategory': subcategory,
                'difficulty': difficulty,
                'duration': duration,
                'topics': topics,
                'description': description
            })
        
        courses_df = pd.DataFrame(courses_data)
        
        # Generate enrollments
        enrollments_data = []
        for _ in range(n_enrollments):
            user_id = random.randint(1, self.n_users)
            course_id = random.randint(1, n_courses)
            completed = random.choice([0, 1])
            rating = random.choice([3, 4, 5]) if completed else None
            progress = random.randint(0, 100) if not completed else 100
            
            enrollments_data.append({
                'userId': user_id,
                'courseId': course_id,
                'completed': completed,
                'rating': rating,
                'progress': progress
            })
        
        enrollments_df = pd.DataFrame(enrollments_data)
        
        # Save
        courses_df.to_csv('data/courses.csv', index=False)
        enrollments_df.to_csv('data/enrollments.csv', index=False)
        
        print(f"✓ Generated {len(courses_df)} courses and {len(enrollments_df)} enrollments")
        return courses_df, enrollments_df
    
    def generate_all(self):
        """Generate all domain data"""
        print("=" * 60)
        print("UniRec Data Generator")
        print("=" * 60)
        print(f"Generating data for {self.n_users} users across all domains...\n")
        
        # Create data directory if it doesn't exist
        import os
        os.makedirs('data', exist_ok=True)
        
        # Generate all domains
        self.generate_movie_data()
        self.generate_product_data()
        self.generate_music_data()
        self.generate_course_data()
        
        print("\n" + "=" * 60)
        print("✓ All data generated successfully!")
        print("=" * 60)
        print("\nFiles created in 'data/' directory:")
        print("  - movies.csv")
        print("  - ratings.csv")
        print("  - products.csv")
        print("  - product_reviews.csv")
        print("  - tracks.csv")
        print("  - listening_history.csv")
        print("  - courses.csv")
        print("  - enrollments.csv")
        print("\nYou can now train the models using train_all_models.py")


if __name__ == "__main__":
    generator = DataGenerator(n_users=1000)
    generator.generate_all()