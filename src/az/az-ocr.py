from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

import time

subscription_key = "<az_ocr_key>"
endpoint = "<az_ocr_endpoint>"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

read_image_url = "<doc-url>"
print("Reading File: " + read_image_url)
print('---')

read_response = computervision_client.read(read_image_url,  raw=True)

read_operation_location = read_response.headers["Operation-Location"]
operation_id = read_operation_location.split("/")[-1]

while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            # print(line.bounding_box)
print('---')
