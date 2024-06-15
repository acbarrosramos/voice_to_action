
import logging
from flask import Flask, request
from twilio.rest import Client
import requests
from requests.auth import HTTPBasicAuth
from src.transcription import speech_to_text
from src.summarize import summarize_text_portuguese
from src.question_answer import question_answer
from dotenv import load_dotenv
import os
import threading

app = Flask(__name__)

load_dotenv()

# Configuraçã de logging
logging.basicConfig(level=logging.DEBUG)

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

DATA_PATH = "raw_data/transcription.txt"

def process_audio(media_url):
    """Processa o áudio recebido da URL e retorna a transcrição."""
    try:
        audio_content = requests.get(media_url, auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN), timeout=60).content
        logging.debug("Audio content fetched")

        audio_path = '/tmp/audio.ogg'
        with open(audio_path, 'wb') as audio_file:
            audio_file.write(audio_content)
        logging.debug("Audio content written to file")

        transcription = speech_to_text(audio_path)
        logging.debug(f"Transcription: {transcription}")

        subject = question_answer()
        logging.debug(f"Subject text: {subject}")

        return transcription, subject
    except Exception as e:
        logging.error(f"Error occurred during audio processing: {e}", exc_info=True)
        raise

def send_intermediate_message(from_number, to_number, subject):
    """Envia mensagem intermediária solicitando resumo."""
    try:
        intermediate_message = client.messages.create(
            from_=from_number,
            body=f"Parece que alguém mandou um podcast para você sobre \"{subject}\" 😂! \nDeseja saber os pontos principais? \nDigite \n1-Sim \n2-Não",
            to=to_number
        )
        logging.debug(f"Intermediate message sent: {intermediate_message.sid}")
    except Exception as e:
        logging.error(f"Error occurred sending intermediate message: {e}", exc_info=True)
        raise

def send_final_message(from_number, to_number, text):
    """Envia a mensagem final para o número de destino."""
    try:
        message = client.messages.create(
            from_=from_number,
            body=text,
            to=to_number
        )
        logging.debug(f"Message sent: {message.sid}")
    except Exception as e:
        logging.error(f"Error occurred sending final message: {e}", exc_info=True)
        raise

@app.route('/voice', methods=['POST'])
def webhook():
    """Webhook para receber áudio e processá-lo."""
    logging.debug("Webhook called")

    try:
        body = request.form['Body'].strip().lower()
        origin = request.form['From'].strip().lower()
        logging.debug(f"Origin: {origin}")

        receiver = request.form['To'].strip().lower()
        logging.debug(f"ReceiverNumber: {receiver}")

        num_media = int(request.form.get('NumMedia', 0))
        logging.debug(f"NumMedia: {num_media}")

        if num_media > 0:
            media_url = request.form['MediaUrl0']
            logging.debug(f"Media URL: {media_url}")

            # Processa o audio e envia o audio em uma thread separada
            threading.Thread(target=process_audio_and_send_summary, args=(media_url, receiver, origin)).start()

            return "OK", 200

        elif body == '1' or body == '2':
            # Lê a transcrição direto do arquivo
            with open(DATA_PATH, 'r', encoding='utf-8') as file:
                transcription = file.read()

            if body == '1':
                summarized_text = summarize_text_portuguese()
                send_final_message(receiver, origin, summarized_text)
            elif body == '2':
                send_final_message(receiver, origin, transcription)
            else:
                logging.warning("Invalid response from user")
                send_final_message(receiver, origin, "Resposta inválida. Por favor, digite 1 para resumir ou 2 para não resumir.")
            return "OK", 200

        else:
            logging.warning("No media found in the request")
            return "No media", 400
    except Exception as e:
        logging.error(f"Error occurred in webhook: {e}", exc_info=True)
        return "Internal Server Error", 500

@app.route('/')
def index():
    return "Hello, World!"

def process_audio_and_send_summary(media_url, from_number, to_number):
    """Função para processar o áudio e enviar o resumo."""
    try:
        transcription, subject = process_audio(media_url)

        if len(transcription) > 512:
            logging.debug("Transcription length greater than 512 characters, summarizing...")
            send_intermediate_message(from_number, to_number, subject)
        else:
            send_final_message(from_number, to_number, transcription)
    except Exception as e:
        logging.error(f"Error occurred during processing and sending summary: {e}", exc_info=True)

if __name__ == '__main__':
 app.run(host="0.0.0.0", port=8080, debug=True)
