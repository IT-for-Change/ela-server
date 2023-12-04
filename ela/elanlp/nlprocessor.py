from elautil import eladataclasses as dc

def initialize():
    return

def process(ActivityItem):
    results = dc.NLPResults()
    results.annotated_text = ''
    results.grammar_analysys = ''
    return results
