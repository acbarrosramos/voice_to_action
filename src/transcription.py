from pydub import AudioSegment
import speech_recognition as sr
import io
import os

def speech_to_text(audio_file):
    DATA_PATH = "raw_data"
    recognizer = sr.Recognizer()

    file_extension = os.path.splitext(audio_file)[1][1:]

    audio_data = AudioSegment.from_file(audio_file, format=file_extension)

    # Converter para WAV e criar um buffer de bytes --preprocessing
    wav_buffer = io.BytesIO()
    audio_data.export(wav_buffer, format="wav")  # Converta para WAV
    wav_buffer.seek(0)

    # Usar BytesIO como entrada para o Recognizer
    with sr.AudioFile(wav_buffer) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language='pt-BR')
        transcription_file_path = os.path.join(DATA_PATH, "transcription.txt")
        with open(transcription_file_path, "w") as f:
            f.write(text)
        return text
    except sr.UnknownValueError:
        return "Não foi possível entender o áudio"
    except sr.RequestError as e:
        return "Erro ao solicitar reconhecimento de fala; {0}".format(e)
