from elautil import eladataclasses as dc

def initialize():
    return


def recognize(ActivityItem):
    results = dc.ASRResults()
    results.text = ''
    results.word_timings = ''
    return results
