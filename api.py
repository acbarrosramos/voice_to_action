from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import requests
from requests.auth import HTTPBasicAuth
from transcription import speech_to_text
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

@app.route('/voice', methods=['POST', 'GET'])
def webhook():

    num_media = int(request.form['NumMedia'])
    if num_media > 0:
        media_url = request.form['MediaUrl0']
        audio_content = requests.get(media_url, auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)).content


        audio_path = '/tmp/audio.ogg'
        with open(audio_path, 'wb') as audio_file:
            audio_file.write(audio_content)

        transcription = speech_to_text(audio_path)

        resp = MessagingResponse()
        resp.message(transcription)
        return str(resp)
    else:
        return "No media", 400

if __name__ == '__main__':
    app.run(debug=True)
