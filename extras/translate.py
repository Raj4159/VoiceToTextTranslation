import torch
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)
from IndicTransToolkit.IndicTransToolkit import IndicProcessor

# Initialize the model and tokenizer
model_name = "ai4bharat/indictrans2-indic-indic-1B"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)
ip = IndicProcessor(inference=True)


def read_sentences_from_file(file_path):
    """
    Reads sentences from a text file and returns them as a list.

    Parameters:
        file_path (str): The path to the text file containing the sentences.

    Returns:
        list: A list of sentences read from the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read all lines from the file and strip any leading/trailing whitespace
            sentences = [line.strip() for line in file if line.strip()]
        return sentences
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")
        return []

# Define input sentences and language codes
input_file_path = 'output/transcribe_output.txt'  # Path to your text file
input_sentences = read_sentences_from_file(input_file_path)

# input_sentences = [
#     "जब मैं छोटा था, मैं हर रोज़ पार्क जाता था।",
#     "हमने पिछले सप्ताह एक नई फिल्म देखी जो कि बहुत प्रेरणादायक थी।",
#     "अगर तुम मुझे उस समय पास मिलते, तो हम बाहर खाना खाने चलते।",
#     "मेरे मित्र ने मुझे उसके जन्मदिन की पार्टी में बुलाया है, और मैं उसे एक तोहफा दूंगा।",
# ]

src_lang, tgt_lang = "hin_Deva", "mar_Deva"

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

# Save each translation to a separate text file
file_name = f"output/translation.txt"  

with open(file_name, "w", encoding="utf-8") as file:
    for i, (input_sentence, translation) in enumerate(zip(input_sentences, translations)):
        print(f"{src_lang}: {input_sentence}")
        print(f"{tgt_lang}: {translation}")
        
        # Write the translation to the file
        file.write(f"{src_lang}: {input_sentence}\n")
        file.write(f"{tgt_lang}: {translation}\n\n")  # Adding \n for a new line between translations

        print(f"Saved translations to {file_name}")

