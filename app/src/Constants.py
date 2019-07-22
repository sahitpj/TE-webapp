
class Constants(object):
    """
    Important constants used by this package
    """
    prepositons = ['on', 'at', 'in', 'until', 'to', 'from', 'into', 'for', 'under', 'as', 'to']
    hypernym_annotation = "http://purl.org/linguistics/gold/hypernym"
    hypernym_PREDICATE = 'hypernym'

    def __init__(self):
        self.VERBS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        self.NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']

        self.ADECTIVES = ['JJ', 'JJR', 'JJS']
        self.preposition_relations = ['case']
