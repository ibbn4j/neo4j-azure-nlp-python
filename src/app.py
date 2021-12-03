from config import Config
from db.Neo4jConnection import Neo4jConnection

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

config = Config()
key = config.az_text_key
endpoint = config.az_text_endpoint

def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

def entity_recognition(client):

    try:
        documents = ["""
            We Help the World Make Sense of Data. 
            Neo4j enables organizations to unlock the business value of connections, influences and
            relationships in data: through new applications that adapt to changing business needs, and by
            enabling existing applications to scale with the business. Headquartered in San Mateo,
            California, Neo4j has offices in Sweden, Germany, Singapore, and the UK.
            Our vision is to help the world make sense of data.
        """]
        result = client.recognize_entities(documents = documents)[0]

        return result.entities

    except Exception as err:
        print("Encountered exception. {}".format(err))

def log(message):
    print(message)

if __name__ == '__main__':
    
    log('Connecting to azure service...')
    client = authenticate_client()

    log('Recognizing entities from documents...')
    entities = entity_recognition(client)

    log('Authenticating Azure services...')
    conn = Neo4jConnection(uri=config.neo4j_uri, user=config.neo4j_username, pwd=config.neo4j_password)

    docUrl = 'Document Title'
    cypher0 = f"MERGE (:Document {{Url: '{docUrl}'}});"

    log(f'Creating document {docUrl} in neo4j...')
    conn.update(cypher0)
    
    for entity in entities:
        cypher = f"""MATCH (d:Document {{Url: '{docUrl}'}})
                        MERGE (c:Category {{Name: '{entity.category}'}})
                        MERGE (e:Entity {{Name: '{entity.text}', Category: '{entity.category}', Subcategory: '{entity.subcategory}', Score: {entity.confidence_score}}})
                        MERGE (d) - [:HAS_ENTITY] -> (e)
                        MERGE (c) <- [:HAS_CATEGORY] - (e) 
                        MERGE (c) <- [:HAS_CATEGORY] - (d)
                        RETURN d;
                """
        conn.update(cypher)
    
    log(f'Finished updating document from {len(entities)} entities...', )   