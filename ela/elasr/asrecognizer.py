from elautil import dataclasses as dc, config as cfg, logger
import whisper_timestamped as whisper

model = None

def initialize():
    global model
    logger.info(f'Initializing ASR model. Loading {cfg.ELA_ASR_MODEL}')
    model = whisper.load_model(cfg.ELA_ASR_MODEL, device=cfg.ELA_ASR_INFERENCE_DEVICE)
    logger.info('Model initialized')
    return


def recognize(item):
    global model

    audioFile = item.submissionfile
    logger.debug(f'Loading audio {audioFile} for inference')
    audio = whisper.load_audio(audioFile)
    logger.debug(f'Transcribing {audioFile}')
    result = whisper.transcribe(model, audio, beam_size=5, best_of=5, temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),detect_disfluencies=True, vad=True)
    asr_text = result["text"]
    asr_text = asr_text.lower()
    logger.debug(f'Transcribed text: {asr_text}')

    all_words = []
    segments = result["segments"]
    for segment in segments:
        all_words.extend(segment["words"])

    word_timings = str(all_words)

    results = dc.ASRResults()
    results.text = asr_text
    results.word_timings = word_timings
    return results
