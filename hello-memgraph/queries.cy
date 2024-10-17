
// MATCH (c:CHUNK)-[r:HAS_ENTITY]->(e:ENTITY)
// RETURN c, e, r LIMIT 10;


// MATCH (e:Entity)
// RETURN DISTINCT e.label

// MATCH (c:Chunk)-[r:HAS_ENTITY]->(e:Entity)
// RETURN c.id AS ChunkID, e.id AS EntityID, e.label AS EntityLabel, COUNT(r) AS RelationshipCount
// ORDER BY RelationshipCount DESC

MATCH (n) DETACH DELETE n;

// MATCH (n) RETURN n;