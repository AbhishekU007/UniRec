# **UniRec – Unified AI Recommendation Engine**

Lightweight showcase of a multi-domain recommender that learns as you interact. UniRec serves four domains (movies, products, music, courses) through a FastAPI backend, React frontend, and a reinforcement-learning layer that personalises results in real time.

---

## **Highlights**
- **Hybrid modelling** – collaborative filtering + content signals per domain, fused inside a unified engine.
- **Instant feedback loop** – likes/dislikes, passes, and ratings trigger preference updates and RL score boosts.
- **Exploration vs exploitation** – epsilon-greedy sampling keeps recommendations fresh while protecting favourites.
- **Cross-domain profile** – quiz answers, behavioural history, and domain embeddings combine into a single user vector.
- **User experience** – React SPA with domain tabs, inline feedback buttons, “Learn from actions” shortcut, and toast status.

---

## **System Overview**
```
           +----------------------------+
           |  React Frontend (Vite)     |
           |  - Auth, domain tabs       |
           |  - Interaction logging     |
           +-------------+--------------+
                    |
           +-------------v--------------+
           | FastAPI Backend            |
           |  Authentication + API      |
           |  UnifiedEngine + RL boost  |
           +------+------+--------------+
                |    |
      +--------------+    +---------------------+
      |                                     |
  +----v----+  +-----------+  +---------+  +---v----+
  | Movies  |  | Products  |  | Music   |  | Courses|
  | CF/CB   |  | CF/Meta   |  | Embed   |  | Content|
  +---------+  +-----------+  +---------+  +--------+
```

---

## **Key Mechanics**

**Domain models**
- *Movies*: hybrid CF + TF-IDF on genres/crew metadata.
- *Products*: purchases + text embeddings, category weighting.
- *Music*: listening matrix + PCA-reduced audio descriptors.
- *Courses*: topic TF-IDF, difficulty progression, RL-aware topic rebalance.

**Unified engine**
- Builds user embeddings per domain, aggregates into a cross-domain profile, optionally re-ranks with LightGBM.

**Reinforcement Learning**
- Interaction tracker stores all events in `data/interactions.json`.
- Weighted scores: like (+0.8), dislike (-0.8), purchase/enrol (+1.0), pass (-0.3), etc.
- `InteractionTracker.apply_reinforcement_boost` shifts ranking immediately; recent likes also adjust the topic quotas inside the course recommender so loved topics replace lower-interest ones next refresh.

---

## **Running the Project**
1. **Install deps**
  ```bash
  pip install -r requirements.txt
  cd frontend && npm install && cd ..
  ```
2. **Generate sample data & train models**
  ```bash
  python backend/generate_data.py
  python backend/train_all_models.py
  ```
3. **Serve backend**
  ```bash
  cd backend
  python api.py  # http://localhost:8000
  ```
4. **Serve frontend**
  ```bash
  cd frontend
  npm run dev    # http://localhost:3000
  ```

Credentials and seed users live in `data/users.json`. All models are persisted under `models/`.

---

## **APIs to Know**
- `GET /api/recommendations/unified?n_per_domain=10` – default endpoint used by the UI.
- `GET /api/recommendations/courses/{user}?n_recommendations=15` – course recommender with RL topic balancing.
- `POST /api/interactions/log` – capture like/dislike/pass/ratings events.
- `POST /api/preferences/update-from-interactions` – “Learn from Actions” button triggers this.
- `GET /api/interactions/stats` – quick dashboards for presentations.

Swagger/OpenAPI docs: `http://localhost:8000/docs`.

---

## **Frontend Walkthrough**
- **Unified tab** bundles all domains, annotated with RL boosts when applicable.
- **Domain tabs** (movies/products/music/courses) call their respective APIs; the course tab now shows all Programming + Data Science items, heavily reordered by recent feedback.
- **Cards** expose like/dislike/pass actions, star ratings, and a detail modal.
- **Learn from Actions** replays interactions for the tracker, updates stored preferences, and calls `fetchRecommendations` so the new order is visible immediately.

---

## **Testing & Demo Tips**
- `python backend/check_status.py` sanity-checks models, data, and API ports.
- To demonstrate RL: like the three Data Science courses, hit “Learn from Actions”, and reload – the course list should alternate Data Science and Programming entries with visible score boosts.
- Sample cURL for logs:
  ```bash
  curl -X POST http://localhost:8000/api/interactions/log \
     -H "Content-Type: application/json" \
     -d '{"user_id":4,"item_id":66,"domain":"courses","action_type":"like"}'
  ```

---

## **Tech Stack**
- **Backend**: FastAPI, pandas/numpy, scikit-learn, LightGBM (optional).
- **Frontend**: React 18, Vite, Tailwind, Lucide icons.
- **Tooling**: Python 3.11 virtualenv, Node 18, GitHub-style project layout.

---

## **License & Attribution**
MIT License. Generated datasets are synthetic; swap in your own CSVs via `backend/generate_data.py` if needed.

Enjoy the project, and feel free to tailor it for demos or coursework submissions! ⭐