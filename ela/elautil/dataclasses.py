from enum import Enum


class PackageType(Enum):
    ECUBE = 0
    BYRA = 1
    SIMPLE = 2

class PackageMeta:
    pkgtype = ''
    schoolpkgid = ''
    schoolcode = ''
    collectiontime = ''

class ActivityItem:
    userid = ''
    username = ''
    lessonid = ''
    assignmentid = ''
    attemptnumber = 0
    attempttime = ''
    submissionfile = ''
    packagemetadata = None

class AssessmentItem:
    assessmenttype = ''
    schoolcode = ''
    pkg_id = ''
    collectedtime = ''
    username = ''
    assignmentid = ''
    lessonid = ''
    attempttime = ''
    attemptnumber = ''
    recordingfile = ''
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