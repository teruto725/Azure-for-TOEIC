from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

from models.azure import Azure

subscription_key = "08c68d3f93b34867a35a91cf41aebb53"
endpoint = "https://terutocomputervison.cognitiveservices.azure.com/"
"""
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

image_path = "static/images/cafe.jpg"
f = open(image_path, "rb")
result = computervision_client.describe_image_in_stream(f)
print(result)
print(result.tags)
f.close()

"""
"""
Azure.setup()
print(Azure.trans_word("shark","en","ja"))
"""
