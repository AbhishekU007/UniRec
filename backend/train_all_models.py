"""
UniRec - Training Script
Train all domain models and create unified recommender
"""

import os
import sys
from pathlib import Path
import importlib

# Import all recommender models
from movie_recommender import MovieRecommender
from product_recommender import ProductRecommender
from music_recommender import MusicRecommender
from course_recommender import CourseRecommender
from unified_engine import UnifiedRecommender

def train_all_models():
    """Train all domain models"""
    print("=" * 80)
    print("UniRec - Model Training Pipeline")
    print("=" * 80)
    
    # Determine project root and models directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_dir = os.path.join(project_root, 'data')
    models_dir = os.path.join(project_root, 'models')
    
    # Create models directory
    os.makedirs(models_dir, exist_ok=True)
    print(f"📁 Models will be saved to: {models_dir}")
    
    # Resolve canonical data paths
    path = lambda *parts: os.path.join(project_root, *parts)

    movies_csv = path('data', 'movies.csv')
    ratings_csv = path('data', 'ratings.csv')
    products_csv = path('data', 'products.csv')
    # Support both reviews.csv (new) and product_reviews.csv (legacy)
    reviews_csv_new = path('data', 'reviews.csv')
    reviews_csv_legacy = path('data', 'product_reviews.csv')
    reviews_csv = reviews_csv_new if os.path.exists(reviews_csv_new) else reviews_csv_legacy
    tracks_csv = path('data', 'tracks.csv')
    listening_csv = path('data', 'listening_history.csv')
    courses_csv = path('data', 'courses.csv')
    enrollments_csv = path('data', 'enrollments.csv')

    # Ensure data exists; if not, try to generate minimal fallbacks (movies only)
    def ensure_data():
        nonlocal reviews_csv
        missing = []
        # Movies
        if not os.path.exists(movies_csv) or not os.path.exists(ratings_csv):
            missing += [p for p in [movies_csv, ratings_csv] if not os.path.exists(p)]
        # Products (support either reviews filename)
        if not os.path.exists(products_csv):
            missing.append(products_csv)
        if not (os.path.exists(reviews_csv_new) or os.path.exists(reviews_csv_legacy)):
            missing.append(reviews_csv_new)
        # Music
        if not os.path.exists(tracks_csv):
            missing.append(tracks_csv)
        if not os.path.exists(listening_csv):
            missing.append(listening_csv)
        # Courses
        if not os.path.exists(courses_csv):
            missing.append(courses_csv)
        if not os.path.exists(enrollments_csv):
            missing.append(enrollments_csv)

        if missing:
            print("\n⚠️  Missing data files detected:")
            for f in missing:
                print(f"   - {f}")

            # If anything other than movies/ratings is missing, don't auto-regenerate to avoid overwriting
            non_movie_missing = [p for p in missing if p not in [movies_csv, ratings_csv]]
            if non_movie_missing:
                print("\n❌ Required dataset(s) missing (non-movie). Please add these files or run your data generator:")
                for f in non_movie_missing:
                    print(f"   - {f}")
                return False

            # Only movies/ratings missing: synthesize a small fallback
            try:
                print("\n🎬 MovieLens files missing — creating synthetic movies/ratings fallback...")
                import pandas as pd
                genres = ['Action', 'Comedy', 'Drama', 'Thriller', 'Romance', 'Sci-Fi']
                movies = pd.DataFrame({
                    'movie_id': range(1, 201),
                    'title': [f"Movie {i}" for i in range(1, 201)],
                    'genres': [random_choice(genres) for _ in range(200)]
                })
                import random
                random.seed(42)
                ratings = pd.DataFrame([
                    {
                        'user_id': random.randint(1, 100),
                        'movie_id': random.randint(1, 200),
                        'rating': random.randint(1, 5)
                    }
                    for _ in range(20000)
                ])
                os.makedirs(data_dir, exist_ok=True)
                movies.to_csv(movies_csv, index=False)
                ratings.to_csv(ratings_csv, index=False)
                print("✓ Synthetic movie data created.")
            except Exception as e:
                print(f"❌ Failed to create synthetic movie data: {e}")
                return False

        return True

    # helper: random choice without numpy to avoid extra import here
    def random_choice(seq):
        import random as _r
        return _r.choice(seq)

    if not ensure_data():
        return False

    print("\nAll required data available. Starting training...\n")
    
    # Train Movie Recommender
    print("-" * 80)
    print("1. Training Movie Recommender")
    print("-" * 80)
    try:
        movie_model = MovieRecommender()
        movie_model.prepare_data(ratings_csv, movies_csv)
        movie_model.train()
        movie_model.save_model(os.path.join(models_dir, 'movie_recommender.pkl'))
        print("✓ Movie recommender trained and saved\n")
    except Exception as e:
        print(f"❌ Error training movie recommender: {e}\n")
        return False
    
    # Train Product Recommender
    print("-" * 80)
    print("2. Training Product Recommender")
    print("-" * 80)
    try:
        product_model = ProductRecommender()
        product_model.prepare_data(reviews_csv, products_csv)
        product_model.train()
        product_model.save_model(os.path.join(models_dir, 'product_recommender.pkl'))
        print("✓ Product recommender trained and saved\n")
    except Exception as e:
        print(f"❌ Error training product recommender: {e}\n")
        return False
    
    # Train Music Recommender
    print("-" * 80)
    print("3. Training Music Recommender")
    print("-" * 80)
    try:
        music_model = MusicRecommender(n_components=50)
        music_model.prepare_data(listening_csv, tracks_csv)
        music_model.train()
        music_model.save_model(os.path.join(models_dir, 'music_recommender.pkl'))
        print("✓ Music recommender trained and saved\n")
    except Exception as e:
        print(f"❌ Error training music recommender: {e}\n")
        return False
    
    # Train Course Recommender
    print("-" * 80)
    print("4. Training Course Recommender")
    print("-" * 80)
    try:
        course_model = CourseRecommender()
        course_model.prepare_data(enrollments_csv, courses_csv)
        course_model.train()
        course_model.save_model(os.path.join(models_dir, 'course_recommender.pkl'))
        print("✓ Course recommender trained and saved\n")
    except Exception as e:
        print(f"❌ Error training course recommender: {e}\n")
        return False
    
    # Create Unified Recommender
    print("-" * 80)
    print("5. Creating Unified Recommender")
    print("-" * 80)
    try:
        unified_model = UnifiedRecommender(
            movie_model, product_model, music_model, course_model
        )
        print("✓ Unified recommender created\n")
    except Exception as e:
        print(f"❌ Error creating unified recommender: {e}\n")
        return False
    
    # Test recommendations
    print("-" * 80)
    print("6. Testing Recommendations")
    print("-" * 80)
    try:
        test_user_id = 1
        
        print(f"\nTesting for User {test_user_id}:\n")
        
        # Test movie recommendations
        print("📽️  Movie Recommendations:")
        movie_recs = movie_model.recommend(test_user_id, n_recommendations=3)
        for i, rec in enumerate(movie_recs, 1):
            print(f"   {i}. {rec['title']} - {rec['genres']} (Score: {rec['score']:.3f})")
        
        # Test product recommendations
        print("\n🛍️  Product Recommendations:")
        product_recs = product_model.recommend(test_user_id, n_recommendations=3)
        for i, rec in enumerate(product_recs, 1):
            print(f"   {i}. {rec['title']} - ${rec['price']:.2f} (Score: {rec['score']:.3f})")
        
        # Test music recommendations
        print("\n🎵  Music Recommendations:")
        music_recs = music_model.recommend(test_user_id, n_recommendations=3)
        for i, rec in enumerate(music_recs, 1):
            print(f"   {i}. {rec['title']} by {rec['artist']} (Score: {rec['score']:.3f})")
        
        # Test course recommendations
        print("\n🎓  Course Recommendations:")
        course_recs = course_model.recommend(test_user_id, n_recommendations=3)
        for i, rec in enumerate(course_recs, 1):
            print(f"   {i}. {rec['title']} - {rec['difficulty']} (Score: {rec['score']:.3f})")
        
        # Test unified recommendations
        print("\n✨  Unified Cross-Domain Recommendations:")
        unified_recs = unified_model.get_unified_recommendations(
            test_user_id, n_per_domain=2, n_total=8
        )
        for i, rec in enumerate(unified_recs['recommendations'], 1):
            domain_emoji = {'movies': '📽️', 'products': '🛍️', 'music': '🎵', 'courses': '🎓'}
            emoji = domain_emoji.get(rec['domain'], '⭐')
            print(f"   {i}. {emoji} [{rec['domain'].upper()}] {rec['title']} (Score: {rec['score']:.3f})")
        
        print("\n✓ All tests passed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}\n")
        return False
    
    # Summary
    print("\n" + "=" * 80)
    print("✓ Training Complete!")
    print("=" * 80)
    print("\nTrained Models:")
    print("  ✓ models/movie_recommender.pkl")
    print("  ✓ models/product_recommender.pkl")
    print("  ✓ models/music_recommender.pkl")
    print("  ✓ models/course_recommender.pkl")
    print("\nNext Steps:")
    print("  1. Start the API server: python api.py")
    print("  2. Start the React frontend: cd frontend && npm run dev")
    print("  3. Access the app at: http://localhost:3000")
    print("=" * 80)
    
    return True


def quick_test():
    """Quick test of a single model"""
    print("Running quick test...\n")
    
    try:
        # Test movie recommender with sample data
        print("Testing Movie Recommender:")
        movie_model = MovieRecommender.load_model('models/movie_recommender.pkl')
        recs = movie_model.recommend(1, n_recommendations=5)
        
        for i, rec in enumerate(recs, 1):
            print(f"{i}. {rec['title']} - {rec['genres']}")
        
        print("\n✓ Quick test passed!")
        
    except FileNotFoundError:
        print("❌ Models not found. Please train models first using: python train_all_models.py")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train UniRec models')
    parser.add_argument('--test', action='store_true', help='Run quick test only')
    args = parser.parse_args()
    
    if args.test:
        quick_test()
    else:
        success = train_all_models()
        sys.exit(0 if success else 1)