# 🎬 MovieVerse - Premium AI Movie Recommendation & Knowledge Graph Platform

## Overview

MovieVerse is a premium Netflix & IMDb-inspired Flask web application powered by **CognoDB Graph Database** and **Flask-Login**. The platform features a complete protected authentication flow, a full-screen loading animation, interactive knowledge graph visualization, AI recommendation engine, smart search filters, and user profile management.

Developed by **G. Krishna**.

---

## 🌟 Key Features

* **Complete Protected Authentication Flow**:
  * Mandatory login wall for unauthenticated users redirecting all protected routes (`/`, `/search`, `/recommendations`, `/graph`, `/about`, `/profile`).
  * Full-screen 1.5s loading animation overlay ("MovieVerse Logo", purple glowing spinner, "Loading your cinematic experience...").
  * Dual user storage supporting **CognoDB / Neo4j** graph backend with **SQLite (mqlslite)** fallback.
* **Netflix & IMDb Inspired Aesthetic**:
  * Glassmorphism layout with purple neon accents, blue glows, and pink highlights.
  * Poppins typography, rounded cards, smooth hover lift & glow transitions.
* **Knowledge Graph Visualization**:
  * Interactive 2D graph network using Vis.js to explore connections between movies, actors, directors, and genres.
  * Interactive controls: Zoom In, Zoom Out, Reset, Fullscreen, and color-coded node legend.
* **AI-Powered Recommendation Engine**:
  * Multi-hop Cypher queries calculating hybrid content similarity scores based on shared genres, directors, actors, and user viewing history.
* **Smart Search & Discovery**:
  * Parameterized search with dynamic filters for Movie, Actor, Director, Genre, Release Year, and IMDb Ratings.

---

## 🛠️ Technology Stack

* **Backend**: Python 3.12, Flask, Flask-Login, Werkzeug
* **Database**: CognoDB (Graph Database), Neo4j Python Driver, SQLite (`movieverse.db`)
* **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript (ES6+), Vis.js Network
* **Design & Theme**: Glassmorphism, Dark Cinematic Theme, Font Awesome 6

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/krishna2045/MovieVerseCognoDB-Fullstack.git
cd MovieVerseCognoDB-Fullstack
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
COGNODB_URI=bolt+s://db-1a2b405d.databases.cognodb.com
COGNODB_USERNAME=cognodb
COGNODB_PASSWORD=89e493ff5757030289694ee34b67486f
SECRET_KEY=super-secret-movieverse-key
```

### 5. Seed Database Data & Demo User
```bash
python seed_db.py
```

### 6. Run the Application
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 🔑 Demo Credentials

* **Username**: `demo`
* **Password**: `password123`

---

## 📄 License
Licensed under the MIT License.
