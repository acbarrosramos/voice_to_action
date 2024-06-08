
import openai
import logging
from dotenv import load_dotenv
import os

# Configuração de  logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY')

openai.api_key = OPENAI_KEY


def summarize_text_portuguese():

    DATA_PATH = "raw_data/transcription.txt"

    # Verifica se o arquivo existe
    if os.path.exists(DATA_PATH):
        # Abre o arquivo em modo de leitura e lê o conteúdo
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            text = file.read()
    else:
        # Se o arquivo não existir, imprime uma mensagem de erro
        logging.debug(f"Erro: O arquivo '{DATA_PATH}' não foi encontrado.")
        return ""

    context = text

    prompt = f"Sumarize esse texto de forma a trazer somente os pontos principais em formato de tópicos e antes de enviar o resumo coloque: Os principais pontos da mensagem são: '{context}'"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages = [{"role": "user", "content": prompt}],
        max_tokens = 130
    )

    summary = response["choices"][0]["message"]["content"].strip()

    if not summary.endswith('.'):
        summary += '...'

    return summary

