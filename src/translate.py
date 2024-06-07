
import torch
from transformers import MarianMTModel, MarianTokenizer

# Define the device
device = "cuda" if torch.cuda.is_available() else "cpu"

model_name_en_pt = 'Helsinki-NLP/opus-mt-tc-big-en-pt'
tokenizer_en_pt = MarianTokenizer.from_pretrained(model_name_en_pt)
model_en_pt = MarianMTModel.from_pretrained(model_name_en_pt).to(device)


def translate_english_to_portuguese(text):
        inputs = tokenizer_en_pt([text], return_tensors='pt', padding=True, truncation=True)
        inputs = inputs.to(device)

        translated = model_en_pt.generate(**inputs)
        translated_text = tokenizer_en_pt.decode(translated[0], skip_special_tokens=True)
        return translated_text
