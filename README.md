# 🧩 UniRec - Unified AI Recommendation Engine

> A multi-domain AI-based recommendation system capable of learning user preferences across movies, products, music, and courses, generating intelligent cross-domain insights.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Features

- **Multi-Domain Intelligence**: Recommendations across 4 domains (Movies, Products, Music, Courses)
- **Hybrid Recommendation**: Combines Collaborative Filtering + Content-Based + Embedding approaches
- **Cross-Domain Learning**: Unified user profiles that leverage behavior across all domains
- **Advanced Ranking**: LightGBM-based ranking layer for optimal recommendations
- **REST API**: Production-ready FastAPI backend
- **Modern UI**: Beautiful React frontend with real-time recommendations

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interactions                         │
│         (Movies, Products, Music, Courses)                   │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│              Domain-Specific Models                          │
│  ┌────────┐  ┌─────────┐  ┌───────┐  ┌────────┐           │
│  │ Movies │  │Products │  │ Music │  │Courses │           │
│  │  (CF+  │  │   (CF+  │  │(Embed-│  │ (Con-  │           │
│  │Content)│  │Metadata)│  │ ding) │  │ tent)  │           │
│  └────────┘  └─────────┘  └───────┘  └────────┘           │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│            Unified Profile Engine                            │
│         (Aggregate Embeddings + Preferences)                 │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│          LightGBM Ranking Layer (Optional)                   │
│              Cross-Domain Feature Fusion                     │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│               FastAPI + React Frontend                       │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Datasets & Domains

| Domain | Example Dataset | Recommendation Type | Key Features |
|--------|----------------|-------------------|--------------|
| 🎬 Movies | MovieLens | Hybrid (CF + Content) | Genre, actors, ratings |
| 🛒 Products | Amazon Reviews | CF + Metadata | Category, brand, price |
| 🎵 Music | Million Song / Spotify | Embedding-based | Genre, artist, audio features |
| 🎓 Courses | Coursera / Udemy | Content-based | Topics, difficulty, skills |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- pip & npm

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/unirec.git
cd unirec
```

2. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

3. **Generate sample data**

```bash
python generate_data.py
```

This creates synthetic data for all 4 domains in the `data/` directory.

4. **Train all models**

```bash
python train_all_models.py
```

This trains all domain-specific models and creates the unified recommender. Models are saved in `models/` directory.

5. **Start the API server**

```bash
python api.py
```

API will be available at `http://localhost:8000`

6. **Start the React frontend**

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
unirec/
├── backend/
│   ├── movie_recommender.py          # Movie recommendation model
│   ├── product_recommender.py        # Product recommendation model
│   ├── music_recommender.py          # Music recommendation model
│   ├── course_recommender.py         # Course recommendation model
│   ├── unified_engine.py             # Unified cross-domain engine
│   ├── api.py                        # FastAPI backend
│   ├── generate_data.py              # Data generation script
│   └── train_all_models.py           # Training pipeline
├── frontend/
│   └── src/
│       ├── App.jsx                   # React main component
│       └── ...
├── data/                             # Generated datasets
├── models/                           # Trained model files
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## 🔧 API Endpoints

### Get Unified Recommendations
```http
GET /api/recommendations/unified/{user_id}?n_per_domain=5&n_total=20
```

### Get Domain-Specific Recommendations
```http
GET /api/recommendations/{domain}/{user_id}?n_recommendations=10
```
Domains: `movies`, `products`, `music`, `courses`

### Get User Profile
```http
GET /api/profile/{user_id}
```

### Get System Stats
```http
GET /api/stats
```

### Search Items
```http
GET /api/search/{domain}?query=query_text&limit=20
```

### Batch Recommendations
```http
POST /api/recommendations/batch
Body: {"user_ids": [1, 2, 3], "n_recommendations": 10}
```

## 🎨 Frontend Features

- **Domain Switching**: Toggle between unified and domain-specific views
- **User Profiles**: View cross-domain user engagement
- **System Stats**: Monitor dataset sizes and model status
- **Real-time Updates**: Dynamic recommendations with loading states
- **Responsive Design**: Beautiful UI with Tailwind CSS
- **Dark Mode**: Modern gradient design

## 🧪 Model Details

### Movie Recommender
- **Algorithm**: Hybrid (Collaborative Filtering + Content-Based)
- **Features**: TF-IDF on genres, user-item matrix
- **Similarity**: Cosine similarity

### Product Recommender
- **Algorithm**: CF + Metadata-based
- **Features**: Category, brand, price, TF-IDF on descriptions
- **Boosting**: Category preference weighting

### Music Recommender
- **Algorithm**: Embedding-based with audio features
- **Features**: PCA-reduced audio features (tempo, energy, valence, etc.)
- **Personalization**: Genre and artist preference tracking

### Course Recommender
- **Algorithm**: Content-based with skill matching
- **Features**: TF-IDF on topics/description
- **Intelligence**: Difficulty progression tracking

### Unified Engine
- **Algorithm**: Cross-domain profile aggregation + optional LightGBM ranker
- **Features**: Weighted embedding fusion, cross-domain signals
- **Innovation**: Learns user preferences holistically

## 📈 Training Pipeline

1. **Data Preparation**: Load and clean domain datasets
2. **Feature Engineering**: Create TF-IDF, embeddings, user-item matrices
3. **Model Training**: Train each domain model independently
4. **Profile Building**: Create unified user profiles
5. **Ranking (Optional)**: Train LightGBM ranker on interaction data
6. **Evaluation**: Test recommendations across domains

## 🎓 Resume-Worthy Description

> Built **UniRec**, an AI-driven multi-domain recommendation system that learns cross-domain user behavior to personalize content across movies, products, music, and courses. Implemented hybrid modeling (collaborative + content-based + embeddings), unified user profiling with embedding fusion, and deployed via FastAPI with a modern React frontend.

## 🛠️ Technologies Used

**Backend:**
- Python 3.8+
- FastAPI
- scikit-learn
- pandas, numpy
- LightGBM (optional)

**Frontend:**
- React 18
- Tailwind CSS
- Lucide Icons
- Vite

**ML Techniques:**
- Collaborative Filtering
- Content-Based Filtering
- TF-IDF Vectorization
- PCA Dimensionality Reduction
- Cosine Similarity
- Embedding Fusion
- Gradient Boosting (LightGBM)

## 📝 Future Enhancements

- [ ] Deep Learning models (Neural Collaborative Filtering)
- [ ] Real-time streaming recommendations
- [ ] A/B testing framework
- [ ] Explainable AI (recommendation reasoning)
- [ ] User feedback loop
- [ ] Social features (friend recommendations)
- [ ] Mobile app
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/GCP)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- MovieLens dataset by GroupLens Research
- Inspired by multi-domain recommendation research
- Built for educational and portfolio purposes

## 📧 Contact

**Your Name** - your.email@example.com

Project Link: [https://github.com/yourusername/unirec](https://github.com/yourusername/unirec)

---

⭐ If you found this project helpful, please give it a star!