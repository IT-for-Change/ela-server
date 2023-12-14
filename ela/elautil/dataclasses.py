from enum import Enum

class ActivityItem:
    userid = ''
    username = ''
    lessonid = ''
    assignmentid = ''
    attemptnumber = 0
    attempttime = ''
    submissionfile = ''
    packagemetadata = None


class PackageMeta:
    schoolpkgid = ''
    schoolcode = ''
    collectiontime = ''


class AssessmentItem:
    schoolcode = ''
    pkg_id = ''
    collectedtime = ''
    username = ''
    assignmentid = ''
    lessonid = ''
    attempttime = ''
    attemptnumber = ''
    asrresult = None
    nlpresult = None

class AuditItemStatus(Enum):
    NOT_INITIALIZED = 0
    STARTED = 1
    ASR_COMPLETE = 2
    NLP_COMPLETE = 3
    FINISHED = 4
    
class AssessmentAuditItem:
    schoolcode = ''
    pkg_id = ''
    audit_time = 0
    status = AuditItemStatus.NOT_INITIALIZED

class ASRResult:
    transcribed_text = ''
    word_timings = ''

class NLPResult:
    annotated_text = ''
    grammar_analysis = ''

class RuntimeConfig:
    config = {}
    def __init__(self):
        self.config = {}

    def set(self,name,val):
        self.config[name] = val
    
    def get(self,name):
        return self.config[name]

    def getAll(self):
        return self.config.items()
