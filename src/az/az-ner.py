key =  "<az_text_key>"
endpoint = "<az_text_endpoint>>"

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

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

        print("Named Entities:\n")
        for entity in result.entities:
            print("\tText: \t", entity.text, "\tCategory: \t", entity.category, "\tSubCategory: \t", entity.subcategory,
                    "\n\tConfidence Score: \t", round(entity.confidence_score, 2), "\tLength: \t", entity.length, "\tOffset: \t", entity.offset, "\n")

    except Exception as err:
        print("Encountered exception. {}".format(err))


if __name__ == '__main__':
    client = authenticate_client()
    entity_recognition(client)