
import time
import torch
from concurrent.futures import ThreadPoolExecutor, as_completed
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline, MarianMTModel, MarianTokenizer

# Define the device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load models and tokenizers
model_name_pt_en = 'unicamp-dl/translation-pt-en-t5'
tokenizer_pt_en = T5Tokenizer.from_pretrained(model_name_pt_en)
model_pt_en = T5ForConditionalGeneration.from_pretrained(model_name_pt_en).to(device)

model_name_en_pt = 'Helsinki-NLP/opus-mt-tc-big-en-pt'
tokenizer_en_pt = MarianTokenizer.from_pretrained(model_name_en_pt)
model_en_pt = MarianMTModel.from_pretrained(model_name_en_pt).to(device)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0 if torch.cuda.is_available() else -1)

def summarize_text_portuguese(input_text):
    def translate_pt_to_en(text):
        input_text = f"translate Portuguese to English: {text}"
        inputs = tokenizer_pt_en([input_text], return_tensors='pt', max_length=512, truncation=True, padding=True)
        inputs = inputs.to(device)

        translated = model_pt_en.generate(**inputs, max_length=250, num_beams=1, early_stopping=True)
        translated_text = tokenizer_pt_en.decode(translated[0], skip_special_tokens=True)
        return translated_text

    def translate_en_to_pt(text):
        inputs = tokenizer_en_pt([text], return_tensors='pt', padding=True, truncation=True)
        inputs = inputs.to(device)

        translated = model_en_pt.generate(**inputs)
        translated_text = tokenizer_en_pt.decode(translated[0], skip_special_tokens=True)
        return translated_text

    def summarize_text(text):
        pipeline_output = summarizer(text, max_length=109, min_length=30, do_sample=False)
        summary_text = pipeline_output[0]['summary_text']
        return summary_text

    def parallel_translate_pt_to_en(texts):
        start_time = time.time()
        with ThreadPoolExecutor() as executor:
            future_to_text = {executor.submit(translate_pt_to_en, text): text for text in texts}
            translated_texts = []
            for future in as_completed(future_to_text):
                translated_texts.append(future.result())
        end_time = time.time()
        processing_time = end_time - start_time
        print('traduzindo pt to en',processing_time)
        return translated_texts, processing_time

    def parallel_translate_en_to_pt(texts):
        start_time = time.time()
        with ThreadPoolExecutor() as executor:
            future_to_text = {executor.submit(translate_en_to_pt, text): text for text in texts}
            translated_texts = []
            for future in as_completed(future_to_text):
                translated_texts.append(future.result())
        end_time = time.time()
        processing_time = end_time - start_time
        print('traduzindo en to pt',processing_time)
        return translated_texts, processing_time

    # Translate Portuguese to English
    translated_text, pt_to_en_time = parallel_translate_pt_to_en([input_text])
    translated_text = translated_text[0]

    # Summarize English text
    summary_text = summarize_text(translated_text)

    # Translate English summary to Portuguese
    translated_summary, en_to_pt_time = parallel_translate_en_to_pt([summary_text])
    translated_summary = translated_summary[0]

    return translated_summary
