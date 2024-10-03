from fastapi import APIRouter, HTTPException, File, UploadFile
from transformers import AutoProcessor, SeamlessM4TModel
from scipy.io import wavfile
import torch
import os
import tempfile


language_mapping = {
    "eng_Latn": "eng",       
    "hin_Deva": "hin",        
    "kan_Knda": "kan",        
    "tam_Taml": "tam",        
    "tel_Telu": "tel",        
    "urd_Arab": "urd",        
    "ben_Beng": "ben",        
}


# Initialize FastAPI router
app = APIRouter()


# Text-to-speech function
def generate_speech(text, src_lang, tgt_lang):
    
    try:    
        # Load models
        processor = AutoProcessor.from_pretrained("facebook/hf-seamless-m4t-medium")
        model = SeamlessM4TModel.from_pretrained("facebook/hf-seamless-m4t-medium")
        
        
        # Process the input text with the processor
        text_inputs = processor(text=text, src_lang=src_lang, return_tensors="pt")

        # Move model and inputs to the GPU if available
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(DEVICE)  
        text_inputs = {key: value.to(DEVICE) for key, value in text_inputs.items()}  

        # Generate the audio from the text in the target language
        audio_array = model.generate(**text_inputs, tgt_lang=tgt_lang)[0].cpu().numpy().squeeze()
        
        
        # Define sample rate and write to a temporary file
        sample_rate = model.config.sample_rate if hasattr(model.config, 'sample_rate') else 16000
        
        temp_dir = "E:/Translate/Backend/Temp_files"  # Change this to your desired directory
        os.makedirs(temp_dir, exist_ok=True)
             
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir=temp_dir) as temp_audio_file:
            wavfile.write(temp_audio_file.name, rate=sample_rate, data=audio_array)
            audio_file_path = temp_audio_file.name
            
            
        return temp_audio_file.name  # Return the path to the generated audio file
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    


# API route to translate and convert text to speech
@app.post("/Text_to_Speech/")
async def text_to_speech(text: str, src_lang: str, tgt_lang: str):
    try:
        # Step 1: Map the IndicTrans tgt_lang code to SeamlessM4T code for text-to-speech
        src_lang_code = language_mapping.get(src_lang)      # converting 'eng_Latn' to 'eng'
        tgt_lang_code = language_mapping.get(tgt_lang)      # converting 'hin_Deva' to 'hin'
        
        # Raise an error if there's no corresponding language in the TTS model
        if not tgt_lang_code:
            raise HTTPException(status_code=400, detail=f"TTS model does not support the target language: {tgt_lang}")
        
        # Step 2: Convert the translated text to speech using the SeamlessM4T language code
        audio_file_path = generate_speech(text, src_lang_code, tgt_lang_code)

        # Return the translated text and the path to the audio file
        return {
            "audio_file": audio_file_path  # Path to the audio file generated from text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

