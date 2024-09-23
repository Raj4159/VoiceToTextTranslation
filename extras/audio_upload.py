import whisper

model = whisper.load_model("medium")

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("audio_input/file.wav")
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)


# Define ouput file name
output_file = "output/output.txt"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(f'{result.text}')

# print the recognized text
print(result.text)



