from transformers import AutoProcessor, SeamlessM4TModel
# import torchaudio
from scipy.io import wavfile   

processor = AutoProcessor.from_pretrained("facebook/hf-seamless-m4t-medium")
model = SeamlessM4TModel.from_pretrained("facebook/hf-seamless-m4t-medium")

# from text
text_inputs = processor(text = "Hello, my dog is cute", src_lang="eng", return_tensors="pt")
audio_array_from_text = model.generate(**text_inputs, tgt_lang="hin")[0].cpu().numpy().squeeze()


sample_rate = model.config.sample_rate if hasattr(model.config, 'sample_rate') else 16000
wavfile.write("out_from_text.wav", rate=sample_rate, data=audio_array_from_text)












# from fastapi import APIRouter, HTTPException, File, UploadFile
# from transformers import AutoProcessor, SeamlessM4Tv2Model
# from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
# from IndicTransToolkit.IndicTransToolkit import IndicProcessor
# from scipy.io import wavfile
# import torch
# import os
# import tempfile


# language_mapping = {
#     "eng_Latn": "eng",       
#     "hin_Deva": "hin",        
#     "kan_Knda": "kan",        
#     "tam_Taml": "tam",        
#     "tel_Telu": "tel",        
#     "urd_Arab": "urd",        
#     "ben_Beng": "ben",        
# }


# # Initialize FastAPI router
# app = APIRouter()


# # Translation function
# def translate_text(input_text, src_lang, tgt_lang):
    
#     # Translation model from IndicTrans
#     translation_model_name = "ai4bharat/indictrans2-indic-indic-1B"
#     translation_tokenizer = AutoTokenizer.from_pretrained(translation_model_name, trust_remote_code=True)
#     translation_model = AutoModelForSeq2SeqLM.from_pretrained(translation_model_name, trust_remote_code=True)
    
#     # Preprocess the text for translation
#     ip = IndicProcessor(inference=True)
#     batch = ip.preprocess_batch([input_text], src_lang=src_lang, tgt_lang=tgt_lang)
#     DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
#     translation_model.to(DEVICE)

#     # Generate translations
#     inputs = translation_tokenizer(batch, truncation=True, padding="longest", return_tensors="pt").to(DEVICE)
#     with torch.no_grad():
#         generated_tokens = translation_model.generate(**inputs, num_beams=5)

#     # Decode the tokens into translations
#     with translation_tokenizer.as_target_tokenizer():
#         generated_tokens = translation_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    
#     translations = ip.postprocess_batch(generated_tokens, lang=tgt_lang)
#     return translations[0]


# # Text-to-speech function
# def text_to_speech(text, tgt_lang):
    
#     try:    
#         # Load models
#         processor = AutoProcessor.from_pretrained("facebook/hf-seamless-m4t-medium")
#         model = SeamlessM4Tv2Model.from_pretrained("facebook/hf-seamless-m4t-medium")
        
#         # Process the input text with the processor
#         text_inputs = processor(text=text, src_lang=tgt_lang, return_tensors="pt")

#         # Move model and inputs to the GPU if available
#         # DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
#         # model.to(DEVICE)  
#         # text_inputs = {key: value.to(DEVICE) for key, value in text_inputs.items()}  

#         # Generate the audio from the text in the target language
#         audio_array = model.generate(**text_inputs, tgt_lang=tgt_lang)[0].cpu().numpy().squeeze()

#         # Define sample rate and write to a temporary file
#         sample_rate = model.config.sample_rate if hasattr(model.config, 'sample_rate') else 16000
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
#             wavfile.write(temp_audio_file.name, rate=sample_rate, data=audio_array)

#         return temp_audio_file.name  # Return the path to the generated audio file
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # API route to translate and convert text to speech
# @app.post("/translate_and_tts/")
# async def translate_and_tts(text: str, tgt_lang: str):
#     try:
#         # Step 1: Translate the input text into the target language using IndicTrans code
#         translated_text = translate_text(text, src_lang="eng_Latn", tgt_lang=tgt_lang)
        
#         # Step 2: Map the IndicTrans tgt_lang code to SeamlessM4T code for text-to-speech
#         seamless_lang_code = language_mapping.get(tgt_lang)
        
#         # Raise an error if there's no corresponding language in the TTS model
#         if not seamless_lang_code:
#             raise HTTPException(status_code=400, detail=f"TTS model does not support the target language: {tgt_lang}")
        
#         # Step 3: Convert the translated text to speech using the SeamlessM4T language code
#         audio_file_path = text_to_speech(translated_text, seamless_lang_code)

#         # Return the translated text and the path to the audio file
#         return {
#             "translated_text": translated_text,
#             "audio_file": audio_file_path  # Path to the audio file generated from text
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

