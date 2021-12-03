from config import Config
from db.Neo4jConnection import Neo4jConnection

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

import time

config = Config()

def authenticate_ner_client():
    key = config.az_text_key
    endpoint = config.az_text_endpoint
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

def authenticate_ocr_client():
    key = config.az_ocr_key
    endpoint = config.az_ocr_endpoint
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))
    return computervision_client

def entity_recognition(ner_client, text):
    try:
        documents = [text]
        result = ner_client.recognize_entities(documents = documents)[0]
        return result.entities

    except Exception as err:
        print("Encountered exception. {}".format(err))

def read_text(computervision_client, doc_url):
    read_image_url = doc_url
    read_response = computervision_client.read(read_image_url,  raw=True)

    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    if read_result.status == OperationStatusCodes.succeeded:
        text = []
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                text.append(line.text)
        return "\n".join(text)

def log(message):
    print(message)

def debug(message):
    # print(message)
    pass

if __name__ == '__main__':
    
    log('Connecting to azure service...')
    ner_client = authenticate_ner_client()
    ocr_client = authenticate_ocr_client()

    doc_url = "<document-url-here>"

    print("Reading file: " + doc_url)
    text = read_text(ocr_client, doc_url)
    debug(text)

    log('Recognizing entities from documents...')
    entities = entity_recognition(ner_client, text)
    debug(entities)

    log('Authenticating Azure services...')
    conn = Neo4jConnection(uri=config.neo4j_uri, user=config.neo4j_username, pwd=config.neo4j_password)

    cypher0 = f"MERGE (:Document {{Url: '{doc_url}'}});"

    log(f'Creating document {doc_url} in neo4j...')
    conn.update(cypher0)
    
    for entity in entities:
        cypher = f"""MATCH (d:Document {{Url: '{doc_url}'}})
                        MERGE (c:Category {{Name: '{entity.category}'}})
                        MERGE (e:Entity {{Name: '{entity.text}', Category: '{entity.category}', Subcategory: '{entity.subcategory}', Score: {entity.confidence_score}}})
                        MERGE (d) - [:HAS_ENTITY] -> (e)
                        MERGE (c) <- [:HAS_CATEGORY] - (e) 
                        MERGE (c) <- [:HAS_CATEGORY] - (d)
                        RETURN d;
                """
        conn.update(cypher)
    
    log(f'Finished updating document from {len(entities)} entities...', )   