from fastapi import APIRouter, File, UploadFile, HTTPException
import os
import torch
import whisper
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit.IndicTransToolkit import IndicProcessor
import tempfile

# Define your FastAPI app
app = APIRouter()

# Language mapping for Whisper detected language to IndicTransToolkit language codes
language_mapping = {
    "en": "eng_Latn",        # English
    "zh": "mandarin",        # Mandarin (Whisper detects Chinese)
    "de": "german",          # German (Whisper only)
    "es": "castilian",       # Spanish (Castilian)
    "ru": "russian",         # Russian (Whisper only)
    "ko": "korean",          # Korean (Whisper only)
    "fr": "french",          # French (Whisper only)
    "ja": "japanese",        # Japanese (Whisper only)
    "pt": "portuguese",      # Portuguese (Whisper only)
    "tr": "turkish",         # Turkish (Whisper only)
    "pl": "polish",          # Polish (Whisper only)
    "hi": "hin_Deva",        # Hindi
    "mr": "mar_Deva",        # Marathi
    "ta": "tam_Taml",        # Tamil
    "te": "tel_Telu",        # Telugu
    "kn": "kan_Knda",        # Kannada
    "ml": "mal_Mlym",        # Malayalam
    "gu": "guj_Gujr",        # Gujarati
    "pa": "pan_Guru",        # Punjabi
    "ur": "urd_Arab",        # Urdu
    "bn": "ben_Beng",        # Bengali
    "as": "asm_Beng",        # Assamese
    "ne": "npi_Deva",        # Nepali
    "or": "ory_Orya",        # Odia (Oriya)
    # Add more language mappings as necessary
}


# Transcribe function
def transcribe_audio_from_bytes(audio_bytes: bytes):
    model = whisper.load_model("medium")

    # Save the audio bytes to a temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        temp_audio_file.write(audio_bytes)
        temp_audio_file_path = temp_audio_file.name

    # Use Whisper's load_audio function to process the saved file
    audio = whisper.load_audio(temp_audio_file_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    _, probs = model.detect_language(mel)
    detected_language = max(probs, key=probs.get)

    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    
    # Clean up the temporary file
    os.remove(temp_audio_file_path)

    return result.text, detected_language
# Translation function (as before)
def translate_text(input_text, src_lang, tgt_lang):
    model_name = "ai4bharat/indictrans2-indic-indic-1B"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)
    ip = IndicProcessor(inference=True)

    # Preprocess the text for translation
    batch = ip.preprocess_batch([input_text], src_lang=src_lang, tgt_lang=tgt_lang)
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(DEVICE)

    # Generate translations
    inputs = tokenizer(batch, truncation=True, padding="longest", return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        generated_tokens = model.generate(**inputs, num_beams=5)

    # Decode the tokens into translations
    with tokenizer.as_target_tokenizer():
        generated_tokens = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    
    translations = ip.postprocess_batch(generated_tokens, lang=tgt_lang)

    return translations[0]  # Return the first translation

# API route to transcribe and translate
@app.post("/transcribe_and_translate/")
async def transcribe_and_translate(audio: UploadFile = File(...), tgt_lang: str = "hin_Deva"):
    try:
        # Read the uploaded audio file as bytes
        audio_bytes = await audio.read()

        # Transcribe audio from bytes
        transcribed_text, detected_language = transcribe_audio_from_bytes(audio_bytes)
        
        # Map detected language to IndicTrans language codes
        if detected_language in language_mapping:
            src_lang = language_mapping[detected_language]
        else:
            raise HTTPException(status_code=400, detail=f"Detected language {detected_language} is not supported for translation.")
        
        # Translate transcribed text
        translation = translate_text(transcribed_text, src_lang=src_lang, tgt_lang=tgt_lang)
        
        return {
            "transcription": transcribed_text,
            "detected_language": detected_language,
            "translation": translation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






# # Transcription function (assumed to have already run, saving the transcribed text)
# def transcribe_audio(audio_file_path):
#     model = whisper.load_model("medium")
#     audio = whisper.load_audio(audio_file_path)
#     audio = whisper.pad_or_trim(audio)
#     mel = whisper.log_mel_spectrogram(audio).to(model.device)

#     _, probs = model.detect_language(mel)
#     detected_language = max(probs, key=probs.get)

#     options = whisper.DecodingOptions()
#     result = whisper.decode(model, mel, options)
    
#     # Save the transcription to a text file
#     output_file = "output/transcribe_output.txt"
#     with open(output_file, "w", encoding="utf-8") as file:
#         file.write(f'{result.text}')
    
#     return result.text, detected_language

# # Translation function (from your code)
# def translate_file(input_file_path, src_lang, tgt_lang, output_file_path='output/translation.txt'):
#     model_name = "ai4bharat/indictrans2-indic-indic-1B"
#     tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
#     model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)
#     ip = IndicProcessor(inference=True)

#     def read_sentences_from_file(file_path):
#         with open(file_path, 'r', encoding='utf-8') as file:
#             sentences = [line.strip() for line in file if line.strip()]
#         return sentences

#     input_sentences = read_sentences_from_file(input_file_path)

#     # Preprocess the sentences
#     batch = ip.preprocess_batch(input_sentences, src_lang=src_lang, tgt_lang=tgt_lang)
#     DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
#     model.to(DEVICE)

#     # Generate translations
#     inputs = tokenizer(batch, truncation=True, padding="longest", return_tensors="pt").to(DEVICE)
#     with torch.no_grad():
#         generated_tokens = model.generate(**inputs, num_beams=5)

#     # Decode the tokens into translations
#     with tokenizer.as_target_tokenizer():
#         generated_tokens = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    
#     translations = ip.postprocess_batch(generated_tokens, lang=tgt_lang)

#     # Save translations to file
#     with open(output_file_path, "w", encoding="utf-8") as file:
#         for i, (input_sentence, translation) in enumerate(zip(input_sentences, translations)):
#             file.write(f"{src_lang}: {input_sentence}\n")
#             file.write(f"{tgt_lang}: {translation}\n\n")
    
#     return translations

# # Single API route to handle both transcription and translation
# @app.post("/transcribe_and_translate/")
# async def transcribe_and_translate(audio: UploadFile = File(...), tgt_lang: str = "hin_Deva"):
#     try:
#         # Save the uploaded audio file temporarily
#         audio_file_path = f"output/{audio.filename}"
#         with open(audio_file_path, "wb") as f:
#             f.write(await audio.read())
        
#         # Transcribe audio and get detected language
#         transcribed_text, detected_language = transcribe_audio(audio_file_path)
        
#         # Map detected language to IndicTrans language codes
#         if detected_language in language_mapping:
#             src_lang = language_mapping[detected_language]
#         else:
#             raise HTTPException(status_code=400, detail=f"Detected language {detected_language} is not supported for translation.")
        
#         # Pass transcribed text to the translation function
#         translations = translate_file(
#             input_file_path="output/transcribe_output.txt", 
#             src_lang=src_lang, 
#             tgt_lang=tgt_lang
#         )
        
#         return {
#             "transcription": transcribed_text,
#             "detected_language": detected_language,
#             "translations": translations
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
