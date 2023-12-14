import spacy
import whisper_timestamped as whisper
import json


audio = whisper.load_audio("hello.ogg")
model = whisper.load_model("tiny.en.pt", device="cpu")
#result = whisper.transcribe(model, audio, language="en")
result = whisper.transcribe(model, audio, beam_size=5, best_of=5, temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),detect_disfluencies=True, vad=True)
asr_text = result["text"]
asr_text = asr_text.lower().strip()
print(asr_text)

# Extract all "words" elements
all_words = []
segments = result["segments"]
for segment in segments:
    all_words.extend(segment["words"])

word_timings = str(all_words)
#print(f'Word timings: {word_timings}')

nlp = spacy.load("en_core_web_trf")
doc = nlp(asr_text)
annotated_text = ''
for token in doc:
    word = token.text
    pos = token.pos_
    if (pos == 'PUNCT'): 
        continue
    annotated_text += word + ': ' + pos + ' '

print(annotated_text.strip())
