import logging
from transformers import pipeline
import os


# Configuração de  logging
logging.basicConfig(level=logging.DEBUG)

def question_answer():
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

    model_name = 'pierreguillou/bert-base-cased-squad-v1.1-portuguese'
    nlp = pipeline("question-answering", model=model_name)

    question = "Do que se trata essa mensagem?"

    result = nlp(question=question, context=context)

    return result['answer']
