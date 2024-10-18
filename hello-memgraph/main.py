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

# Type aliases for better readability
ChunkNode = Dict[str, Any]
EntityNode = Dict[str, Any]

# Load chunk nodes and entity nodes from pickle files
try:
    with open("./graph_data/chunk_nodes_sample.pkl", "rb") as f:
        chunk_nodes: List[ChunkNode] = pickle.load(f)
    with open("./graph_data/entity_nodes_sample.pkl", "rb") as f:
        entity_nodes: List[EntityNode] = pickle.load(f)
    logging.info("Successfully loaded chunk and entity node data.")
except Exception as e:
    logging.error(f"Error loading pickle files: {e}")
    raise

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

def create_nodes(session: Session, chunk_nodes: List[ChunkNode]) -> None:
    """
    Creates CHUNK nodes in the database.
    
    :param session: Active Neo4j/Memgraph session
    :param chunk_nodes: List of chunk nodes to be created
    """
    try:
        for chunk in tqdm(chunk_nodes, desc="Creating CHUNK nodes"):
            cypher_query = """
            CREATE (c:CHUNK {
                id: $id,
                doc_id: $doc_id,
                content: $content
            })
            """
            session.run(cypher_query, id=chunk['id'], doc_id=chunk['doc_id'], content=chunk['text'])
        logging.info("CHUNK nodes created successfully.")
    except Exception as e:
        logging.error(f"Error creating CHUNK nodes: {e}")
        raise

def create_entities(session: Session, entity_nodes: List[EntityNode]) -> None:
    """
    Creates ENTITY nodes in the database.
    
    :param session: Active Neo4j/Memgraph session
    :param entity_nodes: List of entity nodes to be created
    """
    try:
        for entity in tqdm(entity_nodes, desc="Creating ENTITY nodes"):
            cypher_query = """
            CREATE (e:ENTITY {
                id: $id,
                content: $content,
                category: $category,
                chunk_id: $chunk_id
            })
            """
            session.run(cypher_query, id=entity['id'], content=entity['text'], category=entity['label'], chunk_id=entity['chunk_id'])
        logging.info("ENTITY nodes created successfully.")
    except Exception as e:
        logging.error(f"Error creating ENTITY nodes: {e}")
        raise

def create_relationships(session: Session, entity_nodes: List[EntityNode]) -> None:
    """
    Creates relationships between CHUNK and ENTITY nodes.
    
    :param session: Active Neo4j/Memgraph session
    :param entity_nodes: List of entity nodes used to match and create relationships
    """
    try:
        for entity in tqdm(entity_nodes, desc="Creating relationships"):
            cypher_query = """
            MATCH (c:CHUNK {id: $chunk_id})
            MATCH (e:ENTITY {id: $entity_id})
            MERGE (c)-[:HAS_ENTITY]->(e)
            """
            # Execute the query to create a relationship between CHUNK and ENTITY
            session.run(cypher_query, chunk_id=entity['chunk_id'], entity_id=entity['id'])
        logging.info("Relationships created successfully.")
    except Exception as e:
        logging.error(f"Error creating relationships: {e}")
        raise


def verify_data(session: Session) -> None:
    """
    Verifies that nodes and relationships have been created successfully.
    
    :param session: Active Neo4j/Memgraph session
    """
    try:
        chunk_count = session.run("MATCH (c:CHUNK) RETURN count(c) AS count").single()["count"]
        entity_count = session.run("MATCH (e:ENTITY) RETURN count(e) AS count").single()["count"]
        rel_count = session.run("MATCH ()-[r:HAS_ENTITY]->() RETURN count(r) AS count").single()["count"]
        logging.info(f"Verification: Chunks: {chunk_count}, Entities: {entity_count}, Relationships: {rel_count}")
    except Exception as e:
        logging.error(f"Error verifying data: {e}")
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
                create_nodes(session, chunk_nodes)
                create_entities(session, entity_nodes)
                create_relationships(session, entity_nodes)
                # verify_data(session)
                
                logging.info("Graph creation and verification completed successfully.")
    except Exception as e:
        logging.error(f"Error in main process: {e}")
        raise

if __name__ == "__main__":
    main()
