"""
UniRec - FastAPI Backend
REST API for Multi-Domain Recommendations
"""

from fastapi import FastAPI, HTTPException, Query, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
import uvicorn
import pickle
import os

# Import models
from unified_engine import UnifiedRecommender
from movie_recommender import MovieRecommender
from product_recommender import ProductRecommender
from music_recommender import MusicRecommender
from course_recommender import CourseRecommender
from auth import UserManager

app = FastAPI(
    title="UniRec API",
    description="Multi-Domain AI Recommendation Engine",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instances
models = {
    'movie': None,
    'product': None,
    'music': None,
    'course': None,
    'unified': None
}

# Initialize UserManager
user_manager = UserManager()

# Request/Response models
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    quiz_responses: Dict

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    user: Dict

class RecommendationItem(BaseModel):
    item_id: int
    title: str
    domain: str
    score: float
    metadata: Dict

class RecommendationsResponse(BaseModel):
    user_id: int
    recommendations: List[RecommendationItem]
    profile_summary: Optional[Dict] = None

class UserProfileResponse(BaseModel):
    user_id: int
    domains_engaged: List[str]
    preferences: Dict

class HealthResponse(BaseModel):
    status: str
    models_loaded: Dict[str, bool]

# Startup: Load models
@app.on_event("startup")
async def load_models():
    """Load all trained models on startup"""
    try:
        # Check both backend/models and ../models paths
        model_paths = ['models/', '../models/']
        models_dir = None
        
        for path in model_paths:
            if os.path.exists(os.path.join(path, 'movie_recommender.pkl')):
                models_dir = path
                break
        
        if not models_dir:
            print("❌ Models directory not found!")
            return
            
        print(f"\n📂 Loading models from: {os.path.abspath(models_dir)}\n")
        
        if os.path.exists(os.path.join(models_dir, 'movie_recommender.pkl')):
            models['movie'] = MovieRecommender.load_model(os.path.join(models_dir, 'movie_recommender.pkl'))
            print("✓ Movie model loaded")
        
        if os.path.exists(os.path.join(models_dir, 'product_recommender.pkl')):
            models['product'] = ProductRecommender.load_model(os.path.join(models_dir, 'product_recommender.pkl'))
            print("✓ Product model loaded")
        
        if os.path.exists(os.path.join(models_dir, 'music_recommender.pkl')):
            models['music'] = MusicRecommender.load_model(os.path.join(models_dir, 'music_recommender.pkl'))
            print("✓ Music model loaded")
        
        if os.path.exists(os.path.join(models_dir, 'course_recommender.pkl')):
            models['course'] = CourseRecommender.load_model(os.path.join(models_dir, 'course_recommender.pkl'))
            print("✓ Course model loaded")
        
        # Create unified model if all domain models are loaded
        if all(models[k] is not None for k in ['movie', 'product', 'music', 'course']):
            models['unified'] = UnifiedRecommender(
                models['movie'],
                models['product'],
                models['music'],
                models['course']
            )
            print("✓ Unified model created")
            print("\n🎉 All models loaded successfully! API is ready.\n")
        else:
            print(f"\n⚠️ Some models failed to load")
        
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        import traceback
        traceback.print_exc()

# Authentication dependency
async def get_current_user(authorization: Optional[str] = Header(None)):
    """Get current authenticated user from JWT token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    email = user_manager.verify_token(token)
    
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = user_manager.get_user(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# Health check endpoint
@app.get("/", response_model=HealthResponse)
async def health_check():
    """Check API health and model status"""
    return {
        "status": "healthy",
        "models_loaded": {
            "movies": models['movie'] is not None,
            "products": models['product'] is not None,
            "music": models['music'] is not None,
            "courses": models['course'] is not None,
            "unified": models['unified'] is not None
        }
    }

# Authentication endpoints
@app.post("/api/auth/signup", response_model=AuthResponse)
async def signup(request: SignupRequest):
    """Register a new user with quiz responses"""
    user, error = user_manager.create_user(
        email=request.email,
        password=request.password,
        name=request.name,
        quiz_responses=request.quiz_responses
    )
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # Create access token
    access_token = user_manager.create_access_token(user['email'])
    
    # Remove password from response
    user_response = {k: v for k, v in user.items() if k != 'password'}
    
    return AuthResponse(
        access_token=access_token,
        user=user_response
    )

@app.post("/api/auth/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Authenticate user and return token"""
    user, error = user_manager.authenticate_user(
        email=request.email,
        password=request.password
    )
    
    if error:
        raise HTTPException(status_code=401, detail=error)
    
    # Create access token
    access_token = user_manager.create_access_token(user['email'])
    
    # Remove password from response
    user_response = {k: v for k, v in user.items() if k != 'password'}
    
    return AuthResponse(
        access_token=access_token,
        user=user_response
    )

@app.get("/api/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user info"""
    user_response = {k: v for k, v in current_user.items() if k != 'password'}
    return user_response

# Unified recommendations endpoint (authenticated)
@app.get("/api/recommendations/unified", response_model=RecommendationsResponse)
async def get_unified_recommendations(
    n_per_domain: int = Query(5, ge=1, le=20),
    n_total: int = Query(20, ge=1, le=50),
    current_user: dict = Depends(get_current_user)
):
    """
    Get unified recommendations across all domains for authenticated user
    """
    if models['unified'] is None:
        raise HTTPException(status_code=503, detail="Unified model not available")
    
    # Get user's internal recommendation ID
    user_id = current_user['internal_user_id']
    
    try:
        results = models['unified'].get_unified_recommendations(
            user_id,
            n_per_domain=n_per_domain,
            n_total=n_total
        )
        
        # Format response
        recommendations = []
        for rec in results['recommendations']:
            metadata = {k: v for k, v in rec.items() 
                       if k not in ['item_id', 'title', 'domain', 'score', 'unified_score']}
            
            recommendations.append(RecommendationItem(
                item_id=rec['item_id'],
                title=rec['title'],
                domain=rec['domain'],
                score=rec.get('unified_score', rec['score']),
                metadata=metadata
            ))
        
        return RecommendationsResponse(
            user_id=user_id,
            recommendations=recommendations,
            profile_summary=results['profile_summary']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

# Domain-specific recommendations
@app.get("/api/recommendations/{domain}/{user_id}", response_model=RecommendationsResponse)
async def get_domain_recommendations(
    domain: str,
    user_id: int,
    n_recommendations: int = Query(10, ge=1, le=50)
):
    """
    Get recommendations for a specific domain
    Domains: movies, products, music, courses
    """
    if domain not in ['movies', 'products', 'music', 'courses']:
        raise HTTPException(status_code=400, detail="Invalid domain")
    
    model_key = domain.rstrip('s')  # movies -> movie
    if models[model_key] is None:
        raise HTTPException(status_code=503, detail=f"{domain.capitalize()} model not available")
    
    try:
        if models['unified']:
            recs = models['unified'].get_domain_specific_recommendations(
                user_id, domain, n_recommendations
            )
        else:
            # Fallback to direct model call
            recs = models[model_key].recommend(user_id, n_recommendations)
        
        recommendations = []
        for rec in recs:
            metadata = {k: v for k, v in rec.items() 
                       if k not in ['item_id', 'title', 'domain', 'score']}
            
            recommendations.append(RecommendationItem(
                item_id=rec['item_id'],
                title=rec['title'],
                domain=rec['domain'],
                score=rec['score'],
                metadata=metadata
            ))
        
        return RecommendationsResponse(
            user_id=user_id,
            recommendations=recommendations
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

# User profile endpoint
@app.get("/api/profile/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(user_id: int):
    """
    Get user's cross-domain profile
    """
    if models['unified'] is None:
        raise HTTPException(status_code=503, detail="Unified model not available")
    
    try:
        profile = models['unified'].build_unified_profile(user_id)
        
        domains_engaged = [domain for domain, engaged in profile['domains'].items() if engaged]
        
        return UserProfileResponse(
            user_id=user_id,
            domains_engaged=domains_engaged,
            preferences=profile['preferences']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching profile: {str(e)}")

# Search/filter endpoint (optional - for future enhancement)
@app.get("/api/search/{domain}")
async def search_items(
    domain: str,
    query: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Search for items in a specific domain
    """
    if domain not in ['movies', 'products', 'music', 'courses']:
        raise HTTPException(status_code=400, detail="Invalid domain")
    
    model_key = domain.rstrip('s')
    if models[model_key] is None:
        raise HTTPException(status_code=503, detail=f"{domain.capitalize()} model not available")
    
    try:
        # Get the dataframe from the model
        if domain == 'movies':
            df = models[model_key].movies_df
            search_col = 'title'
        elif domain == 'products':
            df = models[model_key].products_df
            search_col = 'title'
        elif domain == 'music':
            df = models[model_key].tracks_df
            search_col = 'title'
        else:  # courses
            df = models[model_key].courses_df
            search_col = 'title'
        
        # Simple text search
        results = df[df[search_col].str.contains(query, case=False, na=False)].head(limit)
        
        return {
            "domain": domain,
            "query": query,
            "results": results.to_dict('records')
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching: {str(e)}")

# Stats endpoint
@app.get("/api/stats")
async def get_stats():
    """
    Get system statistics
    """
    stats = {
        "models_loaded": sum(1 for m in models.values() if m is not None),
        "domains": []
    }
    
    try:
        if models['movie']:
            stats['domains'].append({
                "name": "movies",
                "total_items": len(models['movie'].movies_df),
                "total_users": len(models['movie'].user_item_matrix)
            })
        
        if models['product']:
            stats['domains'].append({
                "name": "products",
                "total_items": len(models['product'].products_df),
                "total_users": len(models['product'].user_item_matrix)
            })
        
        if models['music']:
            stats['domains'].append({
                "name": "music",
                "total_items": len(models['music'].tracks_df),
                "total_users": len(models['music'].user_item_matrix)
            })
        
        if models['course']:
            stats['domains'].append({
                "name": "courses",
                "total_items": len(models['course'].courses_df),
                "total_users": len(models['course'].user_item_matrix)
            })
        
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

# Batch recommendations (for multiple users)
@app.post("/api/recommendations/batch")
async def get_batch_recommendations(
    user_ids: List[int],
    domain: Optional[str] = None,
    n_recommendations: int = Query(10, ge=1, le=50)
):
    """
    Get recommendations for multiple users at once
    """
    if len(user_ids) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 users per batch")
    
    results = []
    for user_id in user_ids:
        try:
            if domain:
                recs = await get_domain_recommendations(domain, user_id, n_recommendations)
            else:
                recs = await get_unified_recommendations(user_id, n_per_domain=5, n_total=n_recommendations)
            results.append(recs)
        except Exception as e:
            results.append({
                "user_id": user_id,
                "error": str(e),
                "recommendations": []
            })
    
    return {"batch_results": results}

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )