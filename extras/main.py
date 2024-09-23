import pyaudio # Soundcard audio I/O access library
import wave # Python 3 module for reading / writing simple .wav files
import whisper
import subprocess
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit.IndicTransToolkit import IndicProcessor


def transcribe_audio(audio_file):
    # Load the Whisper model
    model = whisper.load_model("medium")

    # Load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)

    # Make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # Detect the spoken language
    _, probs = model.detect_language(mel)
    detected_language = max(probs, key=probs.get)
    print(f"Detected language: {detected_language}")

    # Decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # Define output file name and save the transcription
    output_file = "output/transcribe_output.txt"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f'{result.text}')

    # Return the recognized text
    return result.text

# Example usage
# recognized_text = transcribe_audio("audio_input/file.wav")
# print("Recognized text:", recognized_text)





def translate_file(input_file_path, src_lang, tgt_lang, output_file_path='output/translation.txt'):
    """
    Translates sentences from one Indic language to another using IndicTrans model.

    Parameters:
        input_file_path (str): Path to the input text file containing sentences to be translated.
        src_lang (str): Source language code (e.g., 'hin_Deva').
        tgt_lang (str): Target language code (e.g., 'mar_Deva').
        output_file_path (str): Path to the output file to save translations.
    """

    # Initialize the model and tokenizer
    model_name = "ai4bharat/indictrans2-indic-indic-1B"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)
    ip = IndicProcessor(inference=True)

    def read_sentences_from_file(file_path):
        """
        Reads sentences from a text file and returns them as a list.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                sentences = [line.strip() for line in file if line.strip()]
            return sentences
        except Exception as e:
            print(f"An error occurred while reading the file: {str(e)}")
            return []

    # Read input sentences
    input_sentences = read_sentences_from_file(input_file_path)
    if not input_sentences:
        print("No sentences to translate.")
        return

    # Preprocess the sentences
    batch = ip.preprocess_batch(
        input_sentences,
        src_lang=src_lang,
        tgt_lang=tgt_lang,
    )

    # Determine the device (CPU or GPU)
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(DEVICE)

    # Tokenize the sentences and generate input encodings
    inputs = tokenizer(
        batch,
        truncation=True,
        padding="longest",
        return_tensors="pt",
        return_attention_mask=True,
    ).to(DEVICE)

    # Generate translations using the model
    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            use_cache=True,
            min_length=0,
            max_length=256,
            num_beams=5,
            num_return_sequences=1,
        )

    # Decode the generated tokens into text
    with tokenizer.as_target_tokenizer():
        generated_tokens = tokenizer.batch_decode(
            generated_tokens.detach().cpu().tolist(),
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )

    # Postprocess the translations, including entity replacement
    translations = ip.postprocess_batch(generated_tokens, lang=tgt_lang)

    # Save each translation to a text file
    with open(output_file_path, "w", encoding="utf-8") as file:
        for i, (input_sentence, translation) in enumerate(zip(input_sentences, translations)):
            print(f"{src_lang}: {input_sentence}")
            print(f"{tgt_lang}: {translation}")
            
            # Write the translation to the file
            file.write(f"{src_lang}: {input_sentence}\n")
            file.write(f"{tgt_lang}: {translation}\n\n")

        print(f"Saved translations to {output_file_path}")

# Example usage
input_file_path = "output/transcribe_output.txt"
src_lang = 'hin_Deva'
tgt_lang = 'mar_Deva'
translate_file(input_file_path, src_lang, tgt_lang)



