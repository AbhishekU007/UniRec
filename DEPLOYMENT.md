# 🚀 Deployment Guide

## Step 1: Deploy Backend to Render

1. **Create a new Web Service** on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: `unirec-backend` (or your choice)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r ../requirements.txt`
   - **Start Command**: `cd backend && uvicorn api:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables** (optional):
   - `SECRET_KEY`: Generate a secure random key for JWT
5. Click **Create Web Service**
6. Wait for deployment and **copy the service URL** (e.g., `https://unirec-backend.onrender.com`)

## Step 2: Deploy Frontend to Vercel

### Add Backend URL to Vercel

1. Go to your Vercel project → **Settings** → **Environment Variables**
2. Add variable:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://unirec-backend.onrender.com` (your Render backend URL)
   - **Environment**: Production (or All)
3. Save

### Deploy to Vercel

```bash
cd frontend
npm run build
vercel --prod
```

Or use Vercel's GitHub integration for automatic deployments.

## Step 3: Update Backend CORS

After deploying to Vercel, update `backend/api.py`:

```python
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173", 
    "http://localhost:5174",
    "https://your-app.vercel.app",  # Add your Vercel URL here
]
```

Commit and push changes to trigger Render redeployment.

## Step 4: Test Production

1. Visit your Vercel URL
2. Try signing up with the quiz
3. Check that recommendations load correctly

## Environment Variables Summary

### Frontend (Vercel)
- `VITE_API_URL`: Backend URL (e.g., `https://unirec-backend.onrender.com`)

### Backend (Render)
- `SECRET_KEY` (optional): JWT secret key for production

## Troubleshooting

### CORS Errors
- Make sure Vercel URL is added to `allowed_origins` in `backend/api.py`
- Redeploy backend after updating CORS settings

### Auth Not Working
- Check browser console for actual error messages
- Verify `VITE_API_URL` is set correctly in Vercel
- Test API directly: `curl https://your-backend.onrender.com/`

### Backend Cold Start
- Render free tier sleeps after inactivity
- First request may take 30-60 seconds to wake up
- Consider upgrading to paid tier for always-on service

## Alternative: Railway Backend

If you prefer Railway over Render:

1. Create new project on Railway
2. Connect GitHub repo
3. Railway auto-detects Python and runs from root
4. Add environment variable if needed
5. Use the generated Railway URL as `VITE_API_URL`
