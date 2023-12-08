
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
    asrresult = None
    nlpresult = None

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
