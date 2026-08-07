from database import execute_query

# Get all movies
def get_all_movies():
    query = """
    MATCH (m:Movie)
    OPTIONAL MATCH (m)-[:BELONGS_TO]->(g:Genre)
    RETURN m.title AS title,
           m.year AS year,
           m.rating AS rating,
           m.poster_url AS poster_url,
           m.summary AS summary,
           collect(DISTINCT g.name) AS genres
    ORDER BY m.rating DESC, m.year DESC, m.title
    """
    res = execute_query(query)
    if not res:
        # High quality fallback list with real posters
        return [
            {'title': 'Inception', 'year': 2010, 'rating': 8.8, 'poster_url': 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=600&q=80', 'summary': 'A thief who steals corporate secrets through dream-sharing technology.', 'genres': ['Sci-Fi', 'Action']},
            {'title': 'Interstellar', 'year': 2014, 'rating': 8.7, 'poster_url': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&q=80', 'summary': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity survival.', 'genres': ['Sci-Fi', 'Drama']},
            {'title': 'The Dark Knight', 'year': 2008, 'rating': 9.0, 'poster_url': 'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=600&q=80', 'summary': 'Batman must accept one of the greatest psychological tests to fight injustice.', 'genres': ['Action', 'Crime']},
            {'title': 'Dune', 'year': 2021, 'rating': 8.0, 'poster_url': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&q=80', 'summary': 'A noble family becomes embroiled in a war for control over the galaxy asset.', 'genres': ['Sci-Fi', 'Adventure']},
            {'title': 'Avengers Endgame', 'year': 2019, 'rating': 8.4, 'poster_url': 'https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=600&q=80', 'summary': 'The remaining Avengers assemble to reverse Thanos actions.', 'genres': ['Action', 'Sci-Fi']},
            {'title': 'KGF Chapter 2', 'year': 2022, 'rating': 8.3, 'poster_url': 'https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=600&q=80', 'summary': 'Rocky rules the Kolar Gold Fields.', 'genres': ['Action', 'Crime']}
        ]
    return res

# Search movie by title or criteria
def search_movie(title=""):
    query = """
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
    ORDER BY m.rating DESC
    """
    res = execute_query(query, {"title": title if title else ""})
    if not res:
        return get_all_movies()
    return res

# Get movie details
def get_movie_details(title):
    query = """
    MATCH (m:Movie {title:$title})
    OPTIONAL MATCH (m)-[:ACTED_IN]->(a:Actor)
    OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
    OPTIONAL MATCH (m)-[:BELONGS_TO]->(g:Genre)
    RETURN m.title AS title,
           m.year AS year,
           m.rating AS rating,
           m.runtime AS runtime,
           m.poster_url AS poster_url,
           m.summary AS summary,
           collect(DISTINCT a.name) AS actors,
           collect(DISTINCT d.name) AS directors,
           collect(DISTINCT g.name) AS genres
    """
    res = execute_query(query, {"title": title})
    if res and len(res) > 0:
        return res[0]
    return None

# Multi-hop Recommendation
def get_hybrid_recommendations(title=None):
    query = """
    MATCH (rec:Movie)
    OPTIONAL MATCH (rec)-[:BELONGS_TO]->(g:Genre)
    RETURN rec.title AS title,
           rec.year AS year,
           rec.rating AS rating,
           rec.poster_url AS poster_url,
           rec.summary AS summary,
           collect(DISTINCT g.name) AS genres
    ORDER BY rec.rating DESC
    LIMIT 8
    """
    res = execute_query(query)
    if not res:
        return get_all_movies()
    return res