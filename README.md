# neo4j-azure-nlp-python
Example of building knowledge graph in neo4j using azure nlp with neo4j python driver.

# Setup Environment
- Install and Run neo4j (http://neo4j.com/download)
- Prepare Azure Cognitive Service key (https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts-sdk/client-library?tabs=visual-studio&pivots=programming-language-python)
- Prepare Azure Computer Vision Service Key (https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/named-entity-recognition/quickstart?pivots=programming-language-python)
- Update config.py with keys (TODO: Refactor)


# Instal Dependencies

```
> python -m venv .venv
> .venv/Scripts/activate
> pip install -r requirements.txt
```


# Running

```
> python app.py
```