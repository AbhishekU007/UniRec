#!/bin/bash
# Render build script - generates data and trains models

echo "🔧 Installing dependencies..."
pip install -r requirements.txt

echo "📊 Generating sample data..."
python backend/generate_data.py

echo "🤖 Training models..."
python backend/train_all_models.py

echo "✅ Build complete!"
