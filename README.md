# 🎬 MovieVerse - Full-Stack AI Movie Recommendation & Knowledge Graph Platform

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![CognoDB](https://img.shields.io/badge/CognoDB-Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white)](https://neo4j.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

MovieVerse is a premium, full-stack movie recommendation website built with **Flask**, **CognoDB / Neo4j Graph Database**, **Flask-Login**, and **Bootstrap 5**. Designed with a modern **Netflix & IMDb-inspired glassmorphism dark aesthetic**, the application seamlessly combines graph database traversals, personalized AI recommendation algorithms, interactive 2D Knowledge Graph visualizers, and a secure authentication flow with custom loading animations.

---

## 📌 Table of Contents

- [User Flow Architecture](#-user-flow-architecture)
- [Step-by-Step Feature Walkthrough](#-step-by-step-feature-walkthrough)
  - [Step 1: Unauthenticated Flow & Login Wall](#step-1-unauthenticated-flow--login-wall)
  - [Step 2: Credential Verification & 1.5s Loading Animation](#step-2-credential-verification--15s-loading-animation)
  - [Step 3: Dashboard Navigation & Profile Dropdown](#step-3-dashboard-navigation--profile-dropdown)
  - [Step 4: Netflix Hero & Popular Movies](#step-4-netflix-hero--popular-movies)
  - [Step 5: Smart Search & Multi-Attribute Filters](#step-5-smart-search--multi-attribute-filters)
  - [Step 6: CognoDB AI Recommendations](#step-6-cognodb-ai-recommendations)
  - [Step 7: Interactive Vis.js Knowledge Graph](#step-7-interactive-visjs-knowledge-graph)
  - [Step 8: User Profile & Recommendation History](#step-8-user-profile--recommendation-history)
  - [Step 9: Secure Logout & Cache-Control](#step-9-secure-logout--cache-control)
- [System Architecture & Technology Stack](#-system-architecture--technology-stack)
- [CognoDB Graph Data Model](#-cognodb-graph-data-model)
- [Cypher Graph Queries](#-cypher-graph-queries)
- [Project Directory Structure](#-project-directory-structure)
- [Installation & Setup Guide](#-installation--setup-guide)
- [Database Seeding & Dual Persistence](#-database-seeding--dual-persistence)
- [Automated Testing](#-automated-testing)
- [GitHub Repositories](#-github-repositories)
- [Author & License](#-author--license)

---

## 🔄 User Flow Architecture

```mermaid
flowchart TD
    A[User Opens Website] --> B{Is Authenticated?}
    B -- No --> C[Redirect to /auth/login]
    C --> D[MovieVerse Login Page]
    D -->|Click Register| E[Register Account /auth/register]
    E -->|Account Created| C
    D -->|Enter Username + Password| F[Validate with Flask-Login & CognoDB/SQLite]
    F -- Invalid --> D
    F -- Valid --> G[Show 1.5s Cinematic Loading Overlay]
    G -->|Purple Glow + MovieVerse Logo| H[Redirect to Main Dashboard /]
    B -- Yes --> H
    H --> I[Netflix Hero + Popular Movie Cards]
    H --> J[Navbar: Home | Search | Recommendations | Graph | About | Profile | Logout]
    J --> K[Search Page /search]
    J --> L[Recommendations Page /recommendations]
    J --> M[Knowledge Graph Page /graph]
    J --> N[About Page /about]
    J --> O[Profile Page /profile]
    J --> P[Logout /auth/logout]
    P -->|Destroy Session + Clear Cache| C
```

---

## 🚀 Step-by-Step Feature Walkthrough

### Step 1: Unauthenticated Flow & Login Wall
- **Route Security**: All main application routes (`/`, `/search`, `/recommendations`, `/graph`, `/about`, `/profile`) are protected by `@login_required` and a blueprint filter.
- **Redirect behavior**: Any attempt to access protected pages without logging in immediately redirects to `/auth/login`.
- **Standalone Auth UI**: The main dashboard navbar is hidden when unauthenticated. Only the glassmorphism authentication container is displayed.

### Step 2: Credential Verification & 1.5s Loading Animation
- **Supported Login Identifiers**: Accepts Username (e.g., `demo`) or Email (e.g., `demo@movieverse.com`) with hashed password comparison.
- **Cinematic Loading Overlay**:
  - Full-screen glassmorphism overlay (`#loading-overlay`).
  - **MovieVerse Logo** with animated text gradient.
  - **Purple glowing ring loader** (`.purple-ring-loader`) with a pulsing clapperboard center icon.
  - Subtitle: *"Loading your cinematic experience... Connecting to CognoDB Knowledge Graph Engine"*.
  - Duration: 1.5 seconds before navigating to the Main Dashboard (`/`).

### Step 3: Dashboard Navigation & Profile Dropdown
- **Navbar Layout**:
  - Brand Logo: **MovieVerse** with pink text and blue gradient.
  - Links: `Home`, `Search`, `Recommendations`, `Graph`, `About`.
- **User Profile Area**:
  - Circular gradient avatar with user icon.
  - Username displayed next to avatar.
  - Bootstrap dropdown containing:
    - **My Profile** (`/profile`)
    - **Settings** (interactive modal for theme & recommendation preferences)
    - **Logout** (`/auth/logout`)

### Step 4: Netflix Hero & Popular Movies
- **Hero Section**:
  - Heading: **Welcome to MovieVerse**
  - Description: *"Explore movies, discover insights, and receive AI-powered recommendations using Knowledge Graph technology."*
  - Large Search Bar + Search Button.
  - **Right-side Cinematic Illustration**: CSS glowing stage containing 3D floating film reel, popcorn bucket, movie clapperboard, camera, purple glowing smoke aura, and blue lighting effects.
- **Popular Movies Grid**:
  - Responsive cards (6-columns on desktop, 3 on tablet, 2 on mobile).
  - High-resolution cinematic poster images.
  - Movie Title, Release Year, IMDb Rating badge, Genre.
  - Hover animation (card rises up with a neon purple glow border).
  - **View Details** button & interactive **Favorite Heart** toggle.

### Step 5: Smart Search & Multi-Attribute Filters
- **Interactive Search Engine**:
  - Real-time searching across titles, actors, directors, and genres.
- **Advanced Filter Bar**:
  - Filter by Media Type (Movie, TV Series, Documentary).
  - Filter by Genre (Sci-Fi, Action, Drama, Thriller, Adventure).
  - Actor & Director text filters.
  - Min IMDb Rating selector (8.0+, 7.0+).
  - Sort by Relevance, IMDb Rating, or Release Year.

### Step 6: CognoDB AI Recommendations
- Multi-hop graph similarity algorithm calculating content affinity based on shared directors, actors, and genres.
- Displays recommendation cards with **Match Percentage Badges** (e.g., `98% Match`), IMDb ratings, overview, and quick links to details or graph view.

### Step 7: Interactive Vis.js Knowledge Graph
- **Interactive 2D Canvas**: Vis.js network graph renderer showing nodes and relationship edges.
- **Interactive Node Controls**:
  - **Zoom In**: Magnifies graph view.
  - **Zoom Out**: Zooms out camera.
  - **Reset**: Fits network to canvas.
  - **Fullscreen**: Expands graph wrapper to full screen.
- **Color-Coded Legend**:
  - 🟣 **Movies** (`#8B5CF6`)
  - 🔵 **Actors** (`#3B82F6`)
  - 💗 **Directors** (`#EC4899`)
  - 🟢 **Genres** (`#10B981`)
  - 🟡 **Relationships** (`#F59E0B`)

### Step 8: User Profile & Recommendation History
- **Profile Header**: Avatar, Username, Email, Registration Date, Member status badge (`Cinephile Pro`), and quick stats (Movies Watched, Favorite Films, Graph Connections).
- **Tabbed Interface**:
  - **Favorite Movies**: Grid of user's favorited films.
  - **Recently Viewed**: List of recently watched movies and explored graphs.
  - **Recommendation History**: Log table showing past target movies, recommended titles, similarity scores, and graph algorithms used.

### Step 9: Secure Logout & Cache-Control
- Invokes `logout_user()` to destroy Flask session.
- Redirects user to `/auth/login`.
- Serves HTTP headers: `Cache-Control: no-cache, no-store, must-revalidate, max-age=0` to prevent browser back button caching.

---

## 🛠️ System Architecture & Technology Stack

```text
┌─────────────────────────────────────────────────────────────┐
│                    MovieVerse Frontend                      │
│   HTML5 | CSS3 | Bootstrap 5 | JavaScript ES6+ | Vis.js     │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP / JSON API
┌──────────────────────────────▼──────────────────────────────┐
│                    Flask Backend (Python)                   │
│    App Blueprints | Flask-Login Auth | Werkzeug Security    │
└──────────────┬──────────────────────────────┬───────────────┘
               │ Cypher Driver                │ SQL Queries
┌──────────────▼──────────────┐┌──────────────▼──────────────┐
│   CognoDB Graph Database    ││      SQLite (mqlslite)       │
│  (Nodes & Relationships)    ││     (Dual Fallback Store)    │
└─────────────────────────────┘└──────────────────────────────┘
```

---

## 📊 CognoDB Graph Data Model

### Node Labels
- `(m:Movie {title, year, rating, runtime, poster_url, summary})`
- `(a:Actor {name})`
- `(d:Director {name})`
- `(g:Genre {name})`
- `(u:User {username, email, password_hash, created_at})`

### Relationships
- `(u:User)-[:WATCHED]->(m:Movie)`
- `(m:Movie)-[:BELONGS_TO]->(g:Genre)`
- `(m:Movie)-[:ACTED_IN]->(a:Actor)`
- `(m:Movie)-[:DIRECTED_BY]->(d:Director)`

---

## 🔍 Cypher Graph Queries

### 1. Retrieve All Movies & Genres
```cypher
MATCH (m:Movie)
OPTIONAL MATCH (m)-[:BELONGS_TO]->(g:Genre)
RETURN m.title AS title,
       m.year AS year,
       m.rating AS rating,
       m.poster_url AS poster_url,
       m.summary AS summary,
       collect(DISTINCT g.name) AS genres
ORDER BY m.rating DESC, m.title
```

### 2. Search Movie by Title / Actor / Director
```cypher
MATCH (m:Movie)
WHERE toLower(m.title) CONTAINS toLower($title)
OPTIONAL MATCH (m)-[:ACTED_IN]->(a:Actor)
OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
OPTIONAL MATCH (m)-[:BELONGS_TO]->(g:Genre)
RETURN m.title AS title,
       m.year AS year,
       m.rating AS rating,
       m.runtime AS runtime,
       m.poster_url AS poster_url,
       m.summary AS overview,
       collect(DISTINCT a.name) AS cast,
       collect(DISTINCT d.name) AS director,
       collect(DISTINCT g.name) AS genres
```

### 3. Multi-Hop Hybrid Recommendation Traversal
```cypher
MATCH (m:Movie {title:$title})
OPTIONAL MATCH (m)-[:BELONGS_TO]->(g:Genre)
OPTIONAL MATCH (m)-[:ACTED_IN]->(a:Actor)
WITH m, collect(DISTINCT g) AS genres, collect(DISTINCT a) AS actors
MATCH (rec:Movie)
WHERE rec <> m
OPTIONAL MATCH (rec)-[:BELONGS_TO]->(rg:Genre)
OPTIONAL MATCH (rec)-[:ACTED_IN]->(ra:Actor)
WITH rec,
     size(apoc.coll.intersection(genres, collect(DISTINCT rg))) AS genre_sim,
     size(apoc.coll.intersection(actors, collect(DISTINCT ra))) AS actor_sim,
     (genre_sim * 0.5 + actor_sim * 0.5) AS contentScore
RETURN rec.title AS title, rec.poster_url AS poster_url, contentScore
ORDER BY contentScore DESC
LIMIT 8
```

---

## 📁 Project Directory Structure

```text
MovieVerse/
├── app/
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py              # Login, register, logout, & loading endpoints
│   ├── __init__.py                # Flask app factory & blueprint registration
│   ├── config.py                  # Base, Dev, & Prod configurations
│   ├── extensions.py              # Neo4j driver & Flask-Login manager setup
│   ├── models.py                  # Dual User model (CognoDB + SQLite fallback)
│   └── routes.py                  # Main routes (Home, Search, Recs, Graph, Profile)
├── static/
│   ├── css/
│   │   ├── login.css              # Glassmorphism auth styles & loading overlay
│   │   ├── main.css               # Dark theme, glow effects, & hero illustration stage
│   │   └── responsive.css         # Mobile, tablet, & desktop breakpoints
│   └── js/
│       ├── graph.js               # Vis.js network initialization
│       └── main.js                # UI helpers & interactive toggles
├── templates/
│   ├── auth/
│   │   ├── login.html             # Login page with 1.5s loading animation modal
│   │   └── register.html          # Registration page
│   ├── about.html                 # Platform overview & feature cards
│   ├── base.html                  # Global layout with conditional navbar & footer
│   ├── case_study.html            # UI/UX Showcase presentation
│   ├── graph.html                 # Interactive Knowledge Graph page
│   ├── index.html                 # Netflix hero & popular movies dashboard
│   ├── profile.html               # User profile & recommendation history
│   ├── recommendation.html        # Movie details page
│   ├── recommendations.html       # Recommended for you page
│   └── search.html                # Search page with filter sidebar
├── app.py                         # Application entry point
├── config.py                      # Dotenv configuration loader
├── database.py                    # Cypher query execution helper
├── movieverse.db                  # SQLite dual persistence database
├── queries.py                     # Cypher query definitions & fallback data
├── requirements.txt               # Python package dependencies
├── seed_data.py                   # CognoDB graph graph seeder
├── seed_db.py                     # Full dual database seeder script
├── test_app.py                    # Automated test suite
└── README.md                      # Documentation
```

---

## ⚙️ Installation & Setup Guide

### 1. Prerequisites
- Python 3.10+ installed.
- Git installed.

### 2. Clone the Repository
```bash
git clone https://github.com/krishna2045/MovieVerseCognoDB-Fullstack.git
cd MovieVerseCognoDB-Fullstack
```

### 3. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Required Packages
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the project root:
```env
COGNODB_URI=bolt+s://db-1a2b405d.databases.cognodb.com
COGNODB_USERNAME=cognodb
COGNODB_PASSWORD=89e493ff5757030289694ee34b67486f
SECRET_KEY=super-secret-movieverse-key
```

---

## 🗄️ Database Seeding & Dual Persistence

Run `seed_db.py` to populate both CognoDB (Neo4j) and SQLite with rich movie properties, high-res posters, genres, and default demo user accounts:

```bash
python seed_db.py
```

### 🔑 Demo Login Credentials
- **Username**: `demo`
- **Password**: `password123`

---

## 🧪 Automated Testing

To run the unit test suite verifying route protection, authentication flow, and session security:

```bash
python test_app.py
```

Expected Output:
```text
...
----------------------------------------------------------------------
Ran 3 tests in 7.313s

OK
```

---

## 🌐 Running Locally

Start the local server:
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 📦 GitHub Repositories

This codebase is published and mirrored at:
1. [https://github.com/krishna2045/MovieVerseCognoDB-Fullstack](https://github.com/krishna2045/MovieVerseCognoDB-Fullstack)
2. [https://github.com/krishna2045/krishna2045](https://github.com/krishna2045/krishna2045)

---

## 👤 Author & License

Developed by **G. Krishna**.

Licensed under the **MIT License**.
