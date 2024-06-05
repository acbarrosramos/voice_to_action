
import logging
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import requests
from requests.auth import HTTPBasicAuth
from src.transcription import speech_to_text
from src.summarize import summarize_text_portuguese
from dotenv import load_dotenv
import os
import threading

app = Flask(__name__)

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
ORIGIN_NUMBER = os.getenv('ORIGIN_NUMBER')
TO_NUMBER = os.getenv('TO_NUMBER')

def process_audio_and_send_summary(media_url, from_number, to_number):
    try:
        audio_content = requests.get(media_url, auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN), timeout=60).content
        logging.debug("Audio content fetched")

        audio_path = '/tmp/audio.ogg'
        with open(audio_path, 'wb') as audio_file:
            audio_file.write(audio_content)
        logging.debug("Audio content written to file")

        transcription = speech_to_text(audio_path)
        logging.debug(f"Transcription: {transcription}")

        text = transcription
        if len(transcription) > 512:
            logging.debug("Transcription length greater than 512 characters, summarizing...")

            # Send intermediate message
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            intermediate_message = client.messages.create(
                from_=from_number,
                body="*_Parece que alguém mandou um podcast para você 😂! Aguarde, estamos resumindo sua mensagem..._*",
                to=to_number
            )
            logging.debug(f"Intermediate message sent: {intermediate_message.sid}")


            text = summarize_text_portuguese(transcription)
            logging.debug(f"Summarized text: {text}")

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        logging.debug("Twilio client created")

        message = client.messages.create(
            from_=from_number,
            body=text,
            to=to_number
        )
        logging.debug(f"Message sent: {message.sid}")
    except Exception as e:
        logging.error(f"Error occurred during processing: {e}", exc_info=True)

@app.route('/voice', methods=['POST'])
def webhook():
    logging.debug("Webhook called")

    number = request.form['Body'].strip().lower()
    logging.debug(f"numerbody: {number}")

    try:
        num_media = int(request.form.get('NumMedia', 0))
        logging.debug(f"NumMedia: {num_media}")

        if num_media > 0:
            media_url = request.form['MediaUrl0']
            from_number = ORIGIN_NUMBER
            to_number = TO_NUMBER
            logging.debug(f"Media URL: {media_url}")

            # Process the audio and send the summary in a separate thread
            threading.Thread(target=process_audio_and_send_summary, args=(media_url, from_number, to_number)).start()

            return "OK", 200
        else:
            logging.warning("No media found in the request")
            return "No media", 400
    except Exception as e:
        logging.error(f"Error occurred: {e}", exc_info=True)
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(debug=True)
