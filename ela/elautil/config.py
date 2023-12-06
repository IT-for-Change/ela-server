import os

#mandatory variables
ELA_LOG_DIR = os.environ['ELA_LOG_DIR']
ELA_LOG_FILE = os.environ['ELA_LOG_FILE']
ELA_TRIGGER_DIR = os.environ['ELA_TRIGGER_DIR']
ELA_TRIGGER_FILE = os.environ['ELA_TRIGGER_FILE']
ELA_ASR_MODEL = os.environ['ELA_ASR_MODEL']
ELA_ASR_INFERENCE_DEVICE = os.environ['ELA_ASR_INFERENCE_DEVICE'] 
ELA_NLP_MODEL = os.environ['ELA_NLP_MODEL']
PKG_UPLOAD_BASE_DIR = os.environ['PKG_UPLOAD_BASE_DIR']


#fileops
PKG_CSV_REL_DIR = 'data'
PKG_AUDIO_REL_DIR = 'data/audio'
PKG_META_LOG_DIR = 'log'
