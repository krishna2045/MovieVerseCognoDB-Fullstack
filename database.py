import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()
COGNODB_URI = os.getenv('COGNODB_URI')
COGNODB_USERNAME = os.getenv('COGNODB_USERNAME')
COGNODB_PASSWORD = os.getenv('COGNODB_PASSWORD')
if not (COGNODB_URI and COGNODB_USERNAME and COGNODB_PASSWORD):
    raise RuntimeError('Neo4j credentials not set in environment')
driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(COGNODB_USERNAME, COGNODB_PASSWORD)
)

def execute_query(query, parameters=None):
    try:
        with driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    except Exception as e:
        print("Database Error:", e)
        return []

def close_driver():
    driver.close()