import os,time
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import json
import requests

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time



# Google Translite 
from googletrans import Translator
translator = Translator()




account_sid = "************************************"
auth_token  = ""************************************""
subscription_key = ""************************************""
endpoint = "https"************************************"ces.azure.com/"



url = "https"************************************"io/v1/completions?x"
headers = {
  'Content-Type': 'application/json',
  'customer-id': '2846838767',
  'x-api-key': 'zqt_qa9P78jtl6QnbUVE4c_ClWuAfcTvt8DnKWUtwg'
}

def What(Qusation):
    global answer
    answer = "" 
    payload = json.dumps({
      "model": "text-davinci-003",
      "prompt": Qusation,
      "max_tokens": 150,
      "temperature": 0 })
    response = requests.request("POST", url, headers=headers, data=payload)
    AI_Response = response.text
    AI_Response_json = json.loads(AI_Response)
    #print(AI_Response_json['choices'][0]['text'])
    answer = AI_Response_json['choices'][0]['text']





# Medicine_string
def Medicine_string():
    time.sleep(7)
    linesss = " تم التعرف على الدواء  \n "
    linesss += '''
    اسم الدو{NAME}  

{NAME}  

{NAME}   الهضمي

    استخدامات الدواء:
{NAME}  

    موانع استخدام الدواء: 

    يمنع استعمال دواء في الحالات التالية:
{NAME}  
    '''
    send_text(sender,linesss)
    message = client.messages.create(media_url=['https://{site}icine_string.m4a'],from_='whatsapp:+14155238886',to=sender)
# --------------> 





def Medicne():
    time.sleep(7)
    linesss = " تم التعرف على الدواء  \n "
    linesss += '''
تم التعرف على الدواء..
          
اسم الدوا{NAME}
{NAME}السعودية  

{NAME} السكري

استخدامات الدواء:

{NAME}

موانع استخدام الدواء: 

{NAME}

الاثار الجانبية:

{NAME}
    '''
    send_text(sender,linesss)
    message = client.messages.create(media_url=['https://xxxxxx.co/511/{Medicne}.m4a'],from_='whatsapp:+14155238886',to=sender)
# --------------> 





app = Flask(__name__)
client = Client(account_sid, auth_token)

def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)

def send_text(sender,xbody):
    xmessage = client.messages.create(from_='whatsapp:+14155238886',body=xbody,to=sender)
    #xmessage = client.messages.create(from_='whatsapp:+14155238886',body='Hi,Your order number is O12235234',to=sender)



@app.route('/', methods=["GET", "POST"])
def welcom():
    return "welcome ,..."




@app.route('/message', methods=["GET", "POST"])
def reply():
    global sender
    sender = request.form.get('From')
    message = request.form.get('Body')
    media_url = request.form.get('MediaUrl0') 
    print(f'{sender} sent {message}')

    result_arabic = translator.translate(message, src='en', dest='ar')

    #print(result)

    if media_url:

        computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
        # Get an image with text
        read_image_url = media_url
        # Call API with URL and raw response (allows you to get the operation location)
        read_response = computervision_client.read(read_image_url,  raw=True)
        # Get the operation location (URL with an ID at the end) from the response
        read_operation_location = read_response.headers["Operation-Location"]
        # Grab the ID from the URL
        operation_id = read_operation_location.split("/")[-1]

        # Call the "GET" API and wait for it to retrieve the results 
        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)
        # Print the detected text, line by line
        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    send_text(sender,'جاري التحقق من الصورة  🔍 .. ')
                    Medicne(sender)
                    Qusation = message
                    What(Qusation)
                    send_text(sender,answer)
                        
                        
                    else:
                        #send_text(sender,str(line.text))
                        pass 

                send_text(sender,'لم يتم التعرف على الدواء')
        #return respond('Thank you! Your image was received.')
    else:

        #msg = response.message(" ارجو ارسال صورة علبة الدواء ")
        Qusation = message
        What(Qusation)
        send_text(sender,answer)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
