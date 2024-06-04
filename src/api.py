# from flask import Flask, request, jsonify
# from twilio.twiml.messaging_response import MessagingResponse
# import requests
# from requests.auth import HTTPBasicAuth
# from src.transcription import speech_to_text
# from dotenv import load_dotenv
# import os

# app = Flask(__name__)

# load_dotenv()

# TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
# TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

# @app.route('/voice', methods=['POST', 'GET'])
# def webhook():

#     num_media = int(request.form['NumMedia'])
#     if num_media > 0:
#         media_url = request.form['MediaUrl0']
#         audio_content = requests.get(media_url, auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)).content


#         audio_path = '/tmp/audio.ogg'
#         with open(audio_path, 'wb') as audio_file:
#             audio_file.write(audio_content)

#         transcription = speech_to_text(audio_path)

#         resp = MessagingResponse()
#         resp.message(transcription)
#         return str(resp)
#     else:
#         return "No media", 400

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, session  # Importando a sessão
from twilio.twiml.messaging_response import MessagingResponse
import requests
from requests.auth import HTTPBasicAuth
from src.transcription import speech_to_text
from src.summarize import summarize_text_portuguese
from dotenv import load_dotenv
import os
from twilio.rest import Client



app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Definindo a chave secreta para a sessão

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN )


@app.route('/voice', methods=['POST', 'GET'])
def webhook():
    if 'Body' in request.form:
        body = request.form['Body'].strip().lower()
        print(f"User response: {body}")

        # Verificando se estamos esperando a decisão do usuário para sumarizar o texto
        if session.get('waiting_for_summary_decision'):  # Checando a sessão para verificar se estamos esperando a decisão do usuário
            print(f"Waiting for summary decision: {body}")
            if body == '1':
                transcription = session.get('transcription', '')
                if transcription:
                    summarized_text = summarize_text_portuguese(transcription)
                    session.pop('transcription', None)
                    session.pop('waiting_for_summary_decision', None)
                    session.modified = True
                    resp = MessagingResponse()
                    resp.message(summarized_text)

                    print("Summary:", summarized_text)
                    print("resp", str(resp))

                    return str(resp)
                else:
                    resp = MessagingResponse()
                    resp.message("Erro ao obter a transcrição para resumir.")
                    return str(resp)
            elif body == '2':
                transcription = session.get('transcription', '')
                session.pop('transcription', None)
                session.pop('waiting_for_summary_decision', None)
                session.modified = True
                resp = MessagingResponse()
                resp.message(transcription)
                print("Transcription:", transcription)
                print("resp", str(resp))
                return str(resp)

        num_media = int(request.form.get('NumMedia', 0))
        print(f"NumMedia: {num_media}")
        if num_media > 0:
            media_url = request.form['MediaUrl0']
            print(f"Media URL: {media_url}")
            audio_content = requests.get(media_url, auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)).content

            audio_path = '/tmp/audio.ogg'
            with open(audio_path, 'wb') as audio_file:
                audio_file.write(audio_content)

            transcription = speech_to_text(audio_path)
            print(f"Transcription: {transcription}")
            session['transcription'] = transcription
            session.modified = True

            if len(transcription) > 512:
                resp = MessagingResponse()
                resp.message("Mensagem muito longa. Deseja resumir a mensagem? Responda com '1 - Sim' ou '2 - Não'.")
                session['waiting_for_summary_decision'] = True
                session.modified = True
                return str(resp)
            else:
                resp = MessagingResponse()
                resp.message(transcription)
                return str(resp)
        else:
            resp = MessagingResponse()
            resp.message("Nenhum arquivo de mídia foi enviado.")
            return str(resp)
    else:
        resp = MessagingResponse()
        resp.message("Não há nenhuma transcrição em espera. Por favor, envie uma mensagem de voz.")
        return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
