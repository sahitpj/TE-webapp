
class Constants(object):
    """
    Important constants used by this package
    """
    prepositons = ['on', 'at', 'in', 'until', 'to', 'from', 'into', 'for', 'under', 'as', 'to']
    hypernym_annotation = "http://purl.org/linguistics/gold/hypernym"
    hypernym_PREDICATE = 'hypernym'

    german_port = 9005
    french_port = 9006

    LANGUAGES = ['English', 'Spanish', 'German', 'French']

    spotlight_french_endpoint = "http://localhost:2225/rest/annotate"
    spotlight_german_endpoint = "http://localhost:2226/rest/annotate"
    spotlight_spanish_endpoint = "http://localhost:2231/rest/annotate"

    def __init__(self):
        self.VERBS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        self.NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']

        self.ADECTIVES = ['JJ', 'JJR', 'JJS']
        self.preposition_relations = ['case']

class LanguageException(Exception):
    """
    Exception raised when the language is not supported or does not exist
    """
    pass