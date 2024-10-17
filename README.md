# graph


# running docker for memgraph
## Run Memgraph Lab image
More information here https://memgraph.com/docs/getting-started/install-memgraph/docker#run-memgraph-lab-image
-  First run this
    - docker run -d -p 3000:3000 -e QUICK_CONNECT_MG_HOST=host.docker.internal --name lab memgraph/lab
- Now, run this:    
    - docker run -p 7687:7687 -p 7444:7444 memgraph/memgraph-mage

# DELETE data from graph
MATCH (n) DETACH DELETE n;

# QUERY all from graph
MATCH (n) RETURN n;

# QUERY to see nodes, entities and edges
MATCH (c:CHUNK)-[r:HAS_ENTITY]->(e:ENTITY)
RETURN c, e, r LIMIT 10;