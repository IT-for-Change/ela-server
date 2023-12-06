import spacy
from elautil import dataclasses as dc, config as cfg, logger

nlp = None

def initialize():
    global nlp
    nlpmodel = cfg.ELA_NLP_MODEL
    logger.info(f'Initializing NLP model. Loading {nlpmodel}')
    nlp = spacy.load(nlpmodel)
    logger.info('Model loaded')
    return

def process(item, asr_text):

    logger.debug(f'Loading transcribed text for NLP')
    doc = nlp(asr_text)
    logger.debug(f'NLP complete')
    annotated_text = ''
    for token in doc:
        word = token.text
        pos = token.pos_
        annotated_text += word + '_' + pos + ' '
    
    annotated_text = annotated_text.strip()
    logger.debug(f'Annotated text : {annotated_text}')

    results = dc.NLPResults()
    results.annotated_text = annotated_text
    results.grammar_analysis = ''
    return results
