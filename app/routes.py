from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for, make_response
from flask_login import login_required, current_user
from queries import (
    get_all_movies,
    search_movie,
    get_movie_details,
    get_hybrid_recommendations
)

bp = Blueprint('main', __name__)

@bp.before_request
def check_authentication():
    # If user is not authenticated and trying to access any route in main blueprint, redirect to login
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

@bp.after_request
def add_cache_control_headers(response):
    # Prevent browser back button caching on protected pages after logout
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@bp.route('/')
@login_required
def home():
    movies = get_all_movies()
    return render_template('index.html', movies=movies, current_year=2026)

@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    query_text = request.args.get('movie') or request.form.get('movie') or ''
    results = search_movie(query_text)
    return render_template('search.html', movies=results, query=query_text, current_year=2026)

@bp.route('/movie/<title>')
@login_required
def movie_details(title):
    details = get_movie_details(title)
    recommendations = get_hybrid_recommendations(title)
    return render_template(
        'recommendation.html',
        details=details,
        recommendations=recommendations,
        current_year=2026
    )

@bp.route('/recommendations')
@login_required
def recommendations():
    recs = get_hybrid_recommendations()
    return render_template('recommendations.html', recommendations=recs, current_year=2026)

@bp.route('/about')
@login_required
def about():
    return render_template('about.html', current_year=2026)

@bp.route('/graph')
@login_required
def graph_view():
    movie_title = request.args.get('title') or 'Inception'
    return render_template('graph.html', focused_title=movie_title, current_year=2026)

@bp.route('/showcase')
@login_required
def case_study():
    return render_template('case_study.html', current_year=2026)

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', current_year=2026)

@bp.route('/movies')
@login_required
def movies():
    all_movies = get_all_movies()
    return render_template('movies.html', movies=all_movies, current_year=2026)

# ---------- API Endpoints ----------
@bp.route('/api/search')
@login_required
def api_search():
    query_text = request.args.get('q', '') or request.args.get('movie', '')
    results = search_movie(query_text)
    return jsonify(results)

@bp.route('/api/stats')
@login_required
def api_stats():
    movies_list = get_all_movies()
    return jsonify({
        'total_movies': len(movies_list) if movies_list else 0,
        'status': 'online'
    })

@bp.route('/api/recommendations/<title>')
@login_required
def api_recommendations(title):
    recs = get_hybrid_recommendations(title)
    return jsonify(recs)

@bp.route('/api/graph/recommendations/<title>')
@login_required
def api_graph_recommendations(title):
    query = """
    MATCH (m:Movie {title:$title})
    OPTIONAL MATCH (m)-[:BELONGS_TO]->(g:Genre)
    OPTIONAL MATCH (m)-[:ACTED_IN]->(a:Actor)
    WITH m, collect(g) AS genres, collect(a) AS actors
    MATCH (rec:Movie)
    WHERE rec <> m AND (
        (rec)-[:BELONGS_TO]->(g2) WHERE g2 IN genres OR
        (rec)-[:ACTED_IN]->(a2) WHERE a2 IN actors
    )
    RETURN m.title AS source, rec.title AS target, 'RECOMMEND' AS type
    LIMIT 10
    """
    try:
        driver = current_app.extensions.get('neo4j')
        if driver:
            with driver.session() as session:
                rows = session.run(query, {'title': title})
                nodes = set()
                edges = []
                for r in rows:
                    src = r['source']
                    tgt = r['target']
                    nodes.update([src, tgt])
                    edges.append({'from': src, 'to': tgt, 'label': r['type']})
                return jsonify({'nodes': list(nodes), 'edges': edges})
    except Exception as e:
        print("API graph error:", e)

    return jsonify({
        'nodes': [title, 'Inception', 'Interstellar', 'Christopher Nolan', 'Sci-Fi'],
        'edges': [
            {'from': title, 'to': 'Christopher Nolan', 'label': 'DIRECTED_BY'},
            {'from': title, 'to': 'Sci-Fi', 'label': 'BELONGS_TO'},
            {'from': title, 'to': 'Inception', 'label': 'RECOMMENDED'},
            {'from': title, 'to': 'Interstellar', 'label': 'RECOMMENDED'}
        ]
    })

@bp.route('/health')
def health():
    return jsonify({'status': 'ok', 'environment': current_app.config.get('ENV', 'unknown')})
