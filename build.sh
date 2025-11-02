#!/bin/bash
# Render build script - generates data and trains models

set -e  # Exit on error

echo "🔧 Installing dependencies..."
pip install -r requirements.txt

echo "📊 Generating sample data..."
python backend/generate_comprehensive_data.py

echo "📁 Creating models directory..."
mkdir -p models

echo "🤖 Training models (this may take 5-10 minutes)..."
python backend/train_all_models.py

echo "📦 Checking models directory..."
ls -la models/

echo "✅ Build complete! Models ready."
