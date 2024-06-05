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


# import logging
# from flask import Flask, request
# from twilio.twiml.messaging_response import MessagingResponse
# from twilio.rest import Client
# import requests
# from requests.auth import HTTPBasicAuth
# from src.transcription import speech_to_text
# from src.summarize import summarize_text_portuguese
# from dotenv import load_dotenv
# import os

# app = Flask(__name__)

# load_dotenv()

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)

# TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
# TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

# @app.route('/voice', methods=['POST'])
# def webhook():
#     logging.debug("Webhook called")
#     try:
#         num_media = int(request.form.get('NumMedia', 0))
#         logging.debug(f"NumMedia: {num_media}")

#         if num_media > 0:
#             media_url = request.form['MediaUrl0']
#             logging.debug(f"Media URL: {media_url}")

#             audio_content = requests.get(media_url, auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN), timeout=60).content
#             logging.debug("Audio content fetched")

#             audio_path = '/tmp/audio.ogg'
#             with open(audio_path, 'wb') as audio_file:
#                 audio_file.write(audio_content)
#             logging.debug("Audio content written to file")

#             transcription = speech_to_text(audio_path)
#             logging.debug(f"Transcription: {transcription}")

#             text = transcription
#             if len(transcription) > 512:
#                 logging.debug("Transcription length greater than 512 characters, summarizing...")
#                 text = summarize_text_portuguese(transcription)
#                 logging.debug(f"Summarized text: {text}")

#             client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#             logging.debug("Twilio client created")

#             message = client.messages.create(
#                 from_='whatsapp:+14155238886',
#                 body=text,
#                 to='whatsapp:+5521979020427'
#             )
#             logging.debug(f"Message sent: {message.sid}")

#             resp = MessagingResponse()
#             msg = resp.message()
#             msg.body(message.body)
#             logging.debug("Response prepared")

#             return str(resp)
#         else:
#             logging.warning("No media found in the request")
#             return "No media", 400
#     except Exception as e:
#         logging.error(f"Error occurred: {e}", exc_info=True)
#         return "Internal Server Error", 500

# if __name__ == '__main__':
#     app.run(debug=True)


# # Example usage
# text = "O rápido coelho marrom saltou sobre o cão preguiçoso. Era uma manhã brilhante e ensolarada, e o coelho estava animado para começar o dia. Ele correu pelos campos verdes, sentindo o frescor da grama sob suas patas. O cão, por outro lado, estava deitado preguiçosamente à sombra de uma árvore, observando o coelho com indiferença. Enquanto o coelho continuava sua jornada, ele encontrou uma linda borboleta que dançava no ar. Fascinado, ele a seguiu por entre as flores coloridas, perdendo-se na beleza da natureza."

# # Summarize Portuguese text
# summary_portuguese = summarize_text_portuguese(text)
# print("Texto resumido em português:", summary_portuguese)
# print("Texto resumido em português:", summary_portuguese)



# import logging
# from flask import Flask, request
# from twilio.twiml.messaging_response import MessagingResponse
# from twilio.rest import Client
# import requests
# from requests.auth import HTTPBasicAuth
# from src.transcription import speech_to_text
# from src.summarize import summarize_text_portuguese
# from src.question_answer import question_answer
# from dotenv import load_dotenv
# import os
# import threading

# app = Flask(__name__)

# load_dotenv()

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)

# TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
# TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
# ORIGIN_NUMBER = os.getenv('ORIGIN_NUMBER')
# TO_NUMBER = os.getenv('TO_NUMBER')

# def process_audio_and_send_summary(media_url, from_number, to_number):
#     try:
#         audio_content = requests.get(media_url, auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN), timeout=60).content
#         logging.debug("Audio content fetched")

#         audio_path = '/tmp/audio.ogg'
#         with open(audio_path, 'wb') as audio_file:
#             audio_file.write(audio_content)
#         logging.debug("Audio content written to file")

#         transcription = speech_to_text(audio_path)
#         logging.debug(f"Transcription: {transcription}")

#         text = transcription
#         subject = question_answer()
#         logging.debug(f"Subject text: {subject}")
#         if len(transcription) > 512:
#             logging.debug("Transcription length greater than 512 characters, summarizing...")

#             # Send intermediate message
#             client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#             intermediate_message = client.messages.create(
#                 from_=from_number,
#                 body= f"*_Parece que alguém mandou um podcast para você sobre {subject} 😂! Deseja resumir? Digite 1-Sim 2-Não_*",
#                 to=to_number
#             )
#             logging.debug(f"Intermediate message sent: {intermediate_message.sid}")


#             text = summarize_text_portuguese(transcription)
#             logging.debug(f"Summarized text: {text}")

#         client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#         logging.debug("Twilio client created")

#         message = client.messages.create(
#             from_=from_number,
#             body=text,
#             to=to_number
#         )
#         logging.debug(f"Message sent: {message.sid}")
#     except Exception as e:
#         logging.error(f"Error occurred during processing: {e}", exc_info=True)

# @app.route('/voice', methods=['POST'])
# def webhook():
#     logging.debug("Webhook called")

#     number = request.form['Body'].strip().lower()
#     logging.debug(f"numerbody: {number}")

#     try:
#         num_media = int(request.form.get('NumMedia', 0))
#         logging.debug(f"NumMedia: {num_media}")

#         if num_media > 0:
#             media_url = request.form['MediaUrl0']
#             from_number = ORIGIN_NUMBER
#             to_number = TO_NUMBER
#             logging.debug(f"Media URL: {media_url}")

#             # Process the audio and send the summary in a separate thread
#             threading.Thread(target=process_audio_and_send_summary, args=(media_url, from_number, to_number)).start()

#             return "OK", 200
#         else:
#             logging.warning("No media found in the request")
#             return "No media", 400
#     except Exception as e:
#         logging.error(f"Error occurred: {e}", exc_info=True)
#         return "Internal Server Error", 500

# if __name__ == '__main__':
#     app.run(debug=True)
