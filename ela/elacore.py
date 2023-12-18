from elautil import fileops, logger, db, dataclasses as dc
from elanlp import nlprocessor
from elasr import asrecognizer

auditdb = db.ELAAssessmentAuditDatabase()

def initialize():
    asrecognizer.initialize()
    nlprocessor.initialize()
    return

def performAssessment(uploadPkgId, uploadPkgMode):

    global auditdb

    packageMetadata = fileops.loadPackageMetaData(uploadPkgId, uploadPkgMode)
   
    auditdb.audit(packageMetadata,dc.AuditItemStatus.STARTED)

    activityItems = fileops.loadActivityData(packageMetadata)

    assessmentdb = db.ELAAssessmentDatabase(packageMetadata)

    for item in activityItems:

        id = getId(packageMetadata,item)

        logger.info('Assessing {}'.format(id))

        asrresult = asrecognizer.recognize(item)

        #auditdb.audit(packageMetadata,dc.AuditItemStatus.ASR_COMPLETE)

        nlpresult = nlprocessor.process(item,asrresult.transcribed_text)

        #auditdb.audit(packageMetadata,dc.AuditItemStatus.NLP_COMPLETE)
        
        assessment_item = newAssessmentItem(item, packageMetadata, asrresult, nlpresult)

        assessmentdb.save_assessment(assessment_item)
    
    auditdb.audit(packageMetadata,dc.AuditItemStatus.FINISHED)
    
    return

def audit(packageMetadata, status):
    auditdb.audit(packageMetadata.schoolcode,packageMetadata.schoolpkgid,status)
    return

def newAssessmentItem(activity_item, pkg_metadata, asrresult, nlpresult):
    assessmentitem = dc.AssessmentItem()
    assessmentitem.assessmenttype = pkg_metadata.pkgtype
    assessmentitem.schoolcode = pkg_metadata.schoolcode
    assessmentitem.pkg_id = pkg_metadata.schoolpkgid
    assessmentitem.collectedtime = pkg_metadata.collectiontime
    assessmentitem.username = activity_item.username
    assessmentitem.assignmentid = activity_item.assignmentid
    assessmentitem.lessonid = activity_item.lessonid
    assessmentitem.attempttime = activity_item.attempttime
    assessmentitem.recordingfile = activity_item.submissionfile
    assessmentitem.asrresult = asrresult
    assessmentitem.nlpresult = nlpresult
    return assessmentitem


def getId(metadata, item):
    id = metadata.schoolpkgid + '|' \
        + metadata.schoolcode + '|'  \
        + item.username + '|' + item.lessonid + '|' \
        + item.assignmentid + '|' + item.attemptnumber + '|' \
        + item.submissionfile
    return id
        
