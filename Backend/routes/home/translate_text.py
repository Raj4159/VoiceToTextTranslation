from fastapi import APIRouter, HTTPException
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit.IndicTransToolkit import IndicProcessor
import torch

app = APIRouter()

# Initialize the model and tokenizer (loaded once)
model_name = "ai4bharat/indictrans2-indic-indic-1B"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model.to(DEVICE)
ip = IndicProcessor(inference=True)

# Synchronous translation function
async def translate_text_sync(input_text: str, src_lang: str, tgt_lang: str) -> str:
    input_sentences = [input_text]

    # Preprocess the sentences
    batch = ip.preprocess_batch(input_sentences, src_lang=src_lang, tgt_lang=tgt_lang)

    # Generate translations
    inputs = tokenizer(batch, truncation=True, padding="longest", return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        generated_tokens = model.generate(**inputs, num_beams=5, max_new_tokens=50)

    # Decode the tokens into translations
    with tokenizer.as_target_tokenizer():
        generated_tokens = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

    # Ensure translations is a list and handle accordingly
    translations = ip.postprocess_batch(generated_tokens, lang=tgt_lang)

    return translations[0] if translations else ""  # Return the first translation or empty if none

# New API route for text translation
@app.post("/Translate_Text/")
async def translate_text_endpoint(text: str, tgt_lang: str = "mar_Deva", src_lang: str = "hin_Deva"):
    try:
        # Log the received inputs
        print(f"Received text: {text}")
        print(f"Source language: {src_lang}, Target language: {tgt_lang}")

        # Await the asynchronous translation function
        translated_text = await translate_text_sync(text, src_lang, tgt_lang)

        # Log the output
        print(f"Translated text: {translated_text}")

        return {
            "original_text": text,
            "translated_text": translated_text,
            "target_language": tgt_lang,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")