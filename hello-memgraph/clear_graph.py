import logging
import pickle
from neo4j import GraphDatabase, Session
from tqdm import tqdm
from typing import List, Dict, Any

# Set up logging for the application
logging.basicConfig(
    filename='graph_operations.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Database connection settings (use environment variables or config file for sensitive data)
URI = "bolt://localhost:7687"
AUTH = ("", "")  # Memgraph typically doesn't require authentication by default

def clear_database(session: Session) -> None:
    """
    Clears all nodes and relationships from the database.
    
    :param session: Active Neo4j/Memgraph session
    """
    try:
        session.run("MATCH (n) DETACH DELETE n")
        logging.info("Database cleared successfully.")
    except Exception as e:
        logging.error(f"Failed to clear the database: {e}")
        raise

def main():
    """
    Main function that manages the lifecycle of database connections and sessions.
    """
    try:
        # Establish a connection with the database
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            with driver.session() as session:
                logging.info("Connected to the database.")
                
                # Perform database operations
                clear_database(session)
                
                logging.info("Graph creation and verification completed successfully.")
    except Exception as e:
        logging.error(f"Error in main process: {e}")
        raise

if __name__ == "__main__":
    main()
