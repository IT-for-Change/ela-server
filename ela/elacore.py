from elautil import fileops, logger, db, dataclasses as dc
from elanlp import nlprocessor
from elasr import asrecognizer

assessmentdb = None

def initialize():
    global assessmentdb
    asrecognizer.initialize()
    nlprocessor.initialize()
    assessmentdb = db.ELAAssessmentDatabase()
    return

def performAssessment(uploadPkgId):

    global assessmentdb

    packageMetadata = fileops.loadPackageMetaData(uploadPkgId)

    activityItems = fileops.loadActivityData(packageMetadata)

    for item in activityItems:
        id = getId(packageMetadata,item)
        logger.info('Assessing {}'.format(item.username))
        asrresult = asrecognizer.recognize(item)
        nlpresult = nlprocessor.process(item,asrresult.transcribed_text)
        
        assessment_item = newAssessmentItem(item, packageMetadata, asrresult, nlpresult)
        assessmentdb.save_assessment(assessment_item)

    return

def newAssessmentItem(activity_item, pkg_metadata, asrresult, nlpresult):
    assessmentitem = dc.AssessmentItem()
    assessmentitem.schoolcode = pkg_metadata.schoolcode
    assessmentitem.pkg_id = pkg_metadata.schoolpkgid
    assessmentitem.collectedtime = pkg_metadata.collectiontime
    assessmentitem.username = activity_item.username
    assessmentitem.assignmentid = activity_item.assignmentid
    assessmentitem.lessonid = activity_item.lessonid
    assessmentitem.attempttime = activity_item.attempttime
    assessmentitem.asrresult = asrresult
    assessmentitem.nlpresult = nlpresult    
    return assessmentitem


def getId(metadata, item):
    id = metadata.schoolpkgid + '|' \
        + metadata.schoolcode + '|'  \
        + item.username + '|' + item.lessonid + '|' \
        + item.assignmentid + '|' + item.attemptnumber
    return id
        
