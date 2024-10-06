from neo4j import GraphDatabase
from neo4j import GraphDatabase
 
URI = "bolt://localhost:7687"
AUTH = ("", "")
 
with GraphDatabase.driver(URI, auth=AUTH) as client:
    client.verify_connectivity()
 
    # Find a user John in the database
    records, summary, keys = client.execute_query(
        "MATCH (u:User {name: $name}) RETURN u.name AS name",
        name="John",
        database_="memgraph",
    )
    # Run a create query
    node = "CREATE (n:Technology {name:'Memgraph'});"
    client.execute_query(node)
    # -----------------------

    # # Run a read query
    # node = "MATCH (n:Technology) RETURN n;"
    # result = client.execute_query(node)
 
    # for record in records:
    #     node = record["n"]
    #     print(node)
    # # -----------------------

    # # Running queries with property map
    # query = "CREATE (n:Technology {id:$id, name: $name, description: $description});"
    # client.execute_query(query,
    #     id=1,
    #     name="MemgraphDB",
    #     description="Fastest graph database")
    
    # # -----------------------

    # # Process the Node result
    # query = "MATCH (n:Technology) RETURN n;"
    # records, summary, keys = client.execute_query(query)
    # for record in records:
    #     node = record["n"]
    #     print(node)
    # '''To process the results, you can iterate over the records and access the fields you need.'''
    # # -----------------------
    # print(node)             # <Node element_id='47' labels=frozenset({'Technology'}) properties={'description': 'Fastest graph database', 'id': 1, 'name': 'MemgraphDB'}>
    # print(node.labels)      # frozenset({'Technology'})
    # print(node.element_id)  # 48
    # print(node["id"])       # 1
    # print(node["name"])     # MemgraphDB

    # # Process the Relationship result
    # query = "CREATE (u:User {name: 'John'})-[r:LOVES {id:99}]->(t:Technology {name: 'Memgraph'})"
    # client.execute_query(query)
 
    # query = "MATCH (u:User)-[r:LOVES]->(t:Technology) RETURN r"
    # records, summary, keys = client.execute_query(query)
    # for record in records:
    #     relationship = record["r"]
    #     print(relationship)
    #     print(relationship.element_id)
    #     print(relationship["id"])
    #     print(relationship.type)
    #     print(relationship.nodes)
    # # -----------------------

    # # Process the Path result
    # query = "MATCH p=(d:User)-[r:LOVES]->(t:Technology) RETURN p"
    # records, summary, keys = client.execute_query(query)
    # for record in records:
    #     path = record["p"]
    #     print(path)
    #     print(path.nodes)
    #     print(path.relationships)
    #     print(path.start_node)
    #     print(path.end_node)
    # # -----------------------


    # Get the result
    for record in records:
        print(record["name"])
 
    # Print the query
    print(summary.query)