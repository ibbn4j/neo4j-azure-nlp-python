from neo4j import GraphDatabase
from config import Config

config = Config()
uri = config.neo4j_uri
driver = GraphDatabase.driver(uri, auth=(config.neo4j_username, config.neo4j_password))

def get_entities_of(tx, name):
    entities = []
    result = tx.run("MATCH (e:Entity)-[:HAS_CATEGORY]->(c:Category) "
                         "WHERE c.Name = $name "
                         "RETURN e.Name AS entity", name=name)
    for record in result:
        entities.append(record["entity"])
    return entities

with driver.session() as session:
    category = "Location"
    entities = session.read_transaction(get_entities_of, category)
    print(category + ':')
    
    for entity in entities:
        print('- ' + entity)

driver.close()

