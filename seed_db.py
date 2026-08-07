import os
import sqlite3
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from database import execute_query

load_dotenv()

print("--- Seeding Database for MovieVerse ---")

# 1. Setup SQLite Database Table
def setup_sqlite():
    conn = sqlite3.connect("movieverse.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE NOT NULL,
        year INTEGER,
        rating REAL,
        poster_url TEXT,
        summary TEXT,
        genres TEXT
    )
    """)
    
    # Seed default user into SQLite if not existing
    demo_pwd = generate_password_hash("password123")
    cursor.execute("""
    INSERT OR IGNORE INTO users (username, email, password_hash)
    VALUES ('demo', 'demo@movieverse.com', ?)
    """, (demo_pwd,))
    
    demo_krishna = generate_password_hash("krishna123")
    cursor.execute("""
    INSERT OR IGNORE INTO users (username, email, password_hash)
    VALUES ('Krishna', 'krishna@movieverse.com', ?)
    """, (demo_krishna,))
    
    conn.commit()
    conn.close()
    print("SQLite database setup complete.")

# 2. Enrich Neo4j Movies & Users
def setup_neo4j():
    demo_pwd = generate_password_hash("password123")
    demo_krishna = generate_password_hash("krishna123")
    
    # Seed Demo Users in Neo4j
    execute_query("""
    MERGE (u:User {username: 'demo'})
    SET u.email = 'demo@movieverse.com', u.password_hash = $pwd, u.created_at = datetime()
    """, {"pwd": demo_pwd})

    execute_query("""
    MERGE (u:User {username: 'Krishna'})
    SET u.email = 'krishna@movieverse.com', u.password_hash = $pwd, u.created_at = datetime()
    """, {"pwd": demo_krishna})
    
    movies_data = [
        {
            "title": "Inception", "year": 2010, "rating": 8.8, "runtime": "148 min",
            "poster_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=600&q=80",
            "summary": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
        },
        {
            "title": "Interstellar", "year": 2014, "rating": 8.7, "runtime": "169 min",
            "poster_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&q=80",
            "summary": "When Earth becomes uninhabitable, a team of ex-NASA pilots travels through a wormhole in search of a new home for humanity."
        },
        {
            "title": "The Dark Knight", "year": 2008, "rating": 9.0, "runtime": "152 min",
            "poster_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=600&q=80",
            "summary": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological tests of his ability to fight injustice."
        },
        {
            "title": "Dune", "year": 2021, "rating": 8.0, "runtime": "155 min",
            "poster_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&q=80",
            "summary": "A noble family becomes embroiled in a war for control over the galaxy's most valuable asset while its heir is haunted by visions of a dark future."
        },
        {
            "title": "KGF", "year": 2018, "rating": 8.2, "runtime": "156 min",
            "poster_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728?w=600&q=80",
            "summary": "In the 1970s, a fierce rebel named Rocky rises against oppression in the Kolar Gold Fields, embarking on a quest for power and wealth."
        },
        {
            "title": "KGF Chapter 2", "year": 2022, "rating": 8.3, "runtime": "168 min",
            "poster_url": "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=600&q=80",
            "summary": "In the blood-soaked Kolar Gold Fields, Rocky's name strikes fear into his foes while government forces view him as a threat to law and order."
        },
        {
            "title": "Pushpa", "year": 2021, "rating": 7.6, "runtime": "179 min",
            "poster_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&q=80",
            "summary": "Pushpa Raj, a coolie, rises through the ranks of a red sandalwood smuggling syndicate in the forests of Andhra Pradesh."
        },
        {
            "title": "Pushpa 2", "year": 2024, "rating": 8.1, "runtime": "180 min",
            "poster_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&q=80",
            "summary": "The clash between Pushpa Raj and SP Bhanwar Singh Shekhawat continues as Pushpa expands his empire across global borders."
        },
        {
            "title": "RRR", "year": 2022, "rating": 7.8, "runtime": "187 min",
            "poster_url": "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=600&q=80",
            "summary": "A fictitious story about two legendary revolutionaries and their journey away from home before they started fighting for their country in the 1920s."
        },
        {
            "title": "Salaar", "year": 2023, "rating": 6.5, "runtime": "175 min",
            "poster_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&q=80",
            "summary": "A gang leader makes a promise to a dying friend and takes on other criminal gangs in the dystopian city-state of Khansaar."
        },
        {
            "title": "Baahubali", "year": 2015, "rating": 8.0, "runtime": "159 min",
            "poster_url": "https://images.unsplash.com/photo-1568876694728-451bbf694b83?w=600&q=80",
            "summary": "A adventurous young man uncovers his royal lineage and fights to reclaim his rightful throne from a cruel tyrant."
        },
        {
            "title": "Baahubali 2", "year": 2017, "rating": 8.2, "runtime": "167 min",
            "poster_url": "https://images.unsplash.com/photo-1533929736458-ca58856e62bd?w=600&q=80",
            "summary": "Amarendra Baahubali, heir to Mahishmati, faces betrayal and tragedy before his son returns to avenge his father's legacy."
        },
        {
            "title": "Iron Man", "year": 2008, "rating": 7.9, "runtime": "126 min",
            "poster_url": "https://images.unsplash.com/photo-1635863138275-d9b33299680b?w=600&q=80",
            "summary": "After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique armored suit to fight evil."
        },
        {
            "title": "Captain America", "year": 2011, "rating": 6.9, "runtime": "124 min",
            "poster_url": "https://images.unsplash.com/photo-1569003339405-ea396a5a8a90?w=600&q=80",
            "summary": "Steve Rogers, a rejected military soldier, transforms into Captain America after taking a dose of a Super-Soldier serum."
        },
        {
            "title": "Avengers", "year": 2012, "rating": 8.0, "runtime": "143 min",
            "poster_url": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=600&q=80",
            "summary": "Earth's mightiest heroes must come together and learn to fight as a team if they are to stop Loki and his alien army."
        },
        {
            "title": "Avengers Endgame", "year": 2019, "rating": 8.4, "runtime": "181 min",
            "poster_url": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=600&q=80",
            "summary": "After devastating events, the universe is in ruins. With the help of remaining allies, the Avengers assemble to reverse Thanos' actions."
        },
        {
            "title": "Spider-Man Homecoming", "year": 2017, "rating": 7.4, "runtime": "133 min",
            "poster_url": "https://images.unsplash.com/photo-1635805737707-575885ab0820?w=600&q=80",
            "summary": "Peter Parker balances his life as an ordinary high school student in Queens with his superhero alter-ego Spider-Man."
        },
        {
            "title": "Spider-Man No Way Home", "year": 2021, "rating": 8.2, "runtime": "148 min",
            "poster_url": "https://images.unsplash.com/photo-1635805737707-575885ab0820?w=600&q=80",
            "summary": "With Spider-Man's identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds appear."
        },
        {
            "title": "Thor Ragnarok", "year": 2017, "rating": 7.9, "runtime": "130 min",
            "poster_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&q=80",
            "summary": "Imprisoned on the planet Sakaar, Thor must race against time to return to Asgard and stop Ragnarok."
        }
    ]

    for m in movies_data:
        execute_query("""
        MERGE (mov:Movie {title: $title})
        SET mov.year = $year,
            mov.rating = $rating,
            mov.runtime = $runtime,
            mov.poster_url = $poster_url,
            mov.summary = $summary
        """, m)

    print("Neo4j database seeded with full movie properties and demo user.")

if __name__ == "__main__":
    setup_sqlite()
    setup_neo4j()
