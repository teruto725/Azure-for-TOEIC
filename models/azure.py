from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import requests, uuid, json

from array import array
import os
from PIL import Image
import sys
import time

c_key = "ComputerVision's key"
c_end = "https://terutocomputervison.cognitiveservices.azure.com/"
#
t_key = "Transformer's key"
t_end = "https://api.cognitive.microsofttranslator.com/"

class Azure():
    @staticmethod
    #clientをセットする
    def setup():
        Azure.cvc_client = ComputerVisionClient(c_end, CognitiveServicesCredentials(c_key))

    @staticmethod
    #ファイルを受け取って写真の中の物質を検出し名前のリストを返す。
    def detect_objects(f):
        Azure.setup()
        #f = open(image_path, "rb")
        result = Azure.cvc_client.describe_image_in_stream(f)
        #f.close()
        return result

    @staticmethod
    #単語を翻訳し、意味を３つlistで返す
    def trans_word(word,from_lan,to_lan):
        location = "japaneast"
        path = '/dictionary/lookup'
        constructed_url = t_end + path
        params = {'api-version': '3.0','from': from_lan,'to': to_lan}
        headers = {'Ocp-Apim-Subscription-Key': t_key,'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json','X-ClientTraceId': str(uuid.uuid4())
        }
        body = [{
            'text': word
        }]
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        trans_jsons = request.json()[0]["translations"]
        ans_li = list()
        for trans in trans_jsons[0:3]:
            ans_li.append(trans["displayTarget"])
        return ans_li


    @staticmethod
    #写真内の印刷文字を読取る
    def read(image):
        Azure.setup()
        ocr_result_local = Azure.cvc_client.recognize_printed_text_in_stream(image,language='en')
        sentences = list()
        words = list()
        for region in ocr_result_local.regions:
            for line in region.lines:
                #print("Bounding box: {}".format(line.bounding_box))
                s = ""
                for word in line.words:
                    s += word.text + " "
                    words.append(word.text.lower())
                sentences.append(s)

        return {"sentences":sentences,"words":words}

    @staticmethod
    #文章の翻訳を行う
    def trans_sentence(text_input, to_lan):
        path = '/translate?api-version=3.0'
        params = '&to=' + to_lan
        constructed_url = t_end + path + params

        headers = {
            'Ocp-Apim-Subscription-Key': t_key,
            'Ocp-Apim-Subscription-Region': 'japaneast',
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # You can pass more than one object in body.
        body = [{
            'text': text_input
        }]
        response = requests.post(constructed_url, headers=headers, json=body)
        return response.json()[0]["translations"][0]["text"]