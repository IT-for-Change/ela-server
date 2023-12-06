from elautil import fileops, db
from elanlp import nlprocessor
from elasr import asrecognizer

def initialize():
    nlprocessor.initialize()
    asrecognizer.initialize()
    return

def performAssessment(uploadPkgId):

    packageMetadata = fileops.loadPackageMetaData(uploadPkgId)

    activityItems = fileops.loadActivityData(packageMetadata)

    for item in activityItems:
        print('Assessing {}'.format(item.username))
        asrresults = asrecognizer.recognize(item)

        nlpresults = nlprocessor.process(asrresults.transcribed_text)

    return