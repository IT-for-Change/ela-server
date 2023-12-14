import os

#mandatory variables
ELA_LOG_DIR = os.environ['ELA_LOG_DIR']
ELA_TRIGGER_DIR = os.environ['ELA_TRIGGER_DIR']
ELA_TRIGGER_FILE = os.environ['ELA_TRIGGER_FILE']
ELA_ASR_MODEL = os.environ['ELA_ASR_MODEL']
ELA_ASR_INFERENCE_DEVICE = os.environ['ELA_ASR_INFERENCE_DEVICE'] 
ELA_NLP_MODEL = os.environ['ELA_NLP_MODEL']
PKG_UPLOAD_BASE_DIR = os.environ['PKG_UPLOAD_BASE_DIR']
ELA_LOCALDB_DIR = os.environ['ELA_LOCALDB_DIR']
ELA_SERVER_TIMEZONE = os.environ['ELA_SERVER_TIMEZONE']

#optional
ELA_LOG_LEVEL = os.environ.get('LOGLEVEL', 'INFO')


#constants
ELA_LOG_FILE = 'ela.log'
ELA_ASSESSMENTAUDIT_LOCALDB_NAME = 'ela-audit.db'
#fileops
PKG_CSV_REL_DIR = 'data'
PKG_AUDIO_REL_DIR = 'data/audio'
PKG_META_LOG_DIR = 'log'

