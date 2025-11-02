#!/usr/bin/env python3
"""
Production startup script for UniRec Backend
Validates environment and starts the server
"""
import os
import sys

def check_environment():
    """Check if all required files and dependencies are present"""
    print("🔍 Checking environment...")
    
    # Check models directory
    models_dir = os.path.join(os.path.dirname(__file__), '../models')
    required_models = [
        'movie_recommender.pkl',
        'product_recommender.pkl', 
        'music_recommender.pkl',
        'course_recommender.pkl'
    ]
    
    missing_models = []
    for model in required_models:
        model_path = os.path.join(models_dir, model)
        if not os.path.exists(model_path):
            missing_models.append(model)
    
    if missing_models:
        print(f"❌ Missing models: {', '.join(missing_models)}")
        print("Run 'python backend/train_all_models.py' to generate models")
        return False
    
    print("✅ All models present")
    
    # Check data directory
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    if not os.path.exists(os.path.join(data_dir, 'users.json')):
        print("⚠️  users.json not found, will be created on first signup")
    
    return True

def main():
    """Start the production server"""
    if not check_environment():
        sys.exit(1)
    
    print("🚀 Starting UniRec Backend...")
    
    # Import and run uvicorn
    import uvicorn
    
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
