"""
UniRec - Training Script
Train all domain models and create unified recommender
"""

import os
import sys
from pathlib import Path

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
    models_dir = os.path.join(project_root, 'models')
    
    # Create models directory
    os.makedirs(models_dir, exist_ok=True)
    print(f"📁 Models will be saved to: {models_dir}")
    
    # Check if data exists
    data_files = [
        '../data/movies.csv', '../data/ratings.csv',
        '../data/products.csv', '../data/product_reviews.csv',
        '../data/tracks.csv', '../data/listening_history.csv',
        '../data/courses.csv', '../data/enrollments.csv'
    ]
    
    missing_files = [f for f in data_files if not os.path.exists(f)]
    if missing_files:
        print("\nERROR: Missing data files:")
        for f in missing_files:
            print(f"   - {f}")
        print("\nPlease run 'python generate_data.py' first to generate sample data.")
        sys.exit(1)
    
    print("\nAll data files found. Starting training...\n")
    
    # Train Movie Recommender
    print("-" * 80)
    print("1. Training Movie Recommender")
    print("-" * 80)
    try:
        movie_model = MovieRecommender()
        movie_model.prepare_data('../data/ratings.csv', '../data/movies.csv')
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
        product_model.prepare_data('../data/product_reviews.csv', '../data/products.csv')
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
        music_model.prepare_data('../data/listening_history.csv', '../data/tracks.csv')
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
        course_model.prepare_data('../data/enrollments.csv', '../data/courses.csv')
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