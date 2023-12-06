from elautil import fileops, db, logger
from elanlp import nlprocessor
from elasr import asrecognizer

def initialize():
    asrecognizer.initialize()
    nlprocessor.initialize()
    return

def performAssessment(uploadPkgId):

    packageMetadata = fileops.loadPackageMetaData(uploadPkgId)

    activityItems = fileops.loadActivityData(packageMetadata)

    for item in activityItems:
        id = getId(packageMetadata,item)
        logger.info('Assessing {}'.format(item.username))
        asrresults = asrecognizer.recognize(item)
        nlpresults = nlprocessor.process(item,asrresults.transcribed_text)

    return

def getId(metadata, item):
    id = metadata.schoolpkgid + '|' \
        + metadata.schoolcode + '|'  \
        + item.username + '|' + item.lessonid + '|' \
        + item.assignmentid + '|' + item.attemptnumber
    return id
        
