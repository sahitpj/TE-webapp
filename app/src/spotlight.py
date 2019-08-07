import sys
sys.path.append("../..")
sys.path.append("..")

from .pyspotlight import spotlight
from .Constants import Constants


class Spotlight_Pipeline(object):

    def __init__(self, language):
        self.language = language.lower()
        self.spotlight_config = spotlight.Config()
        self.spotlight_address = None
        if self.language == 'english':
            self.spotlight_address = self.spotlight_config.spotlight_address
        elif self.language == 'spanish':
            self.spotlight_address = Constants.spotlight_spanish_endpoint
        elif self.language == 'german':
            self.spotlight_address = Constants.spotlight_german_endpoint
        elif self.language == 'french':
            self.spotlight_address = Constants.spotlight_french_endpoint
        else:
            raise Exception("Given language is not supported or does not exist. Only english, french, german, spanish are supported")

    def read_annotations(self, annotations):
        return [ i['URI'] for i in annotations ]

    def annotate_word(self, word):
        try:
            annotations = spotlight.annotate(self.spotlight_address,
                                        word)
            return self.read_annotations(annotations)
        except spotlight.SpotlightException:
            print("URI not found")
            return None


    def annotate_triple(self, triple, addn_props):
        SUBJECT = None
        PREDICATE = None
        OBJECT = None
        if isinstance(triple[0], list) or isinstance(triple[0], tuple):
            main_word = triple[0][0]
            combined_word = ' '.join(list(triple[0][1]) + list(triple[0][0]))
            annotation = self.annotate_word(combined_word)
            print(annotation)
            if annotation:
                annotation = self.annotate_word(main_word)
            if annotation:
                SUBJECT = annotation
        else:
            annotation = self.annotate_word(triple[0])
            if annotation:
                SUBJECT = annotation

        if isinstance(triple[2], list) or isinstance(triple[0], tuple):
            main_word = triple[2][0]
            combined_word = ' '.join(list(triple[2][1]) + list(triple[2][0]))
            annotation = self.annotate_word(combined_word)[0]
            if annotation:
                annotation = self.annotate_word(main_word)
            if annotation:
                OBJECT = annotation
        else:
            annotation = self.annotate_word(triple[2])
            if annotation:
                OBJECT = annotation

        if triple[1] == Constants.hypernym_PREDICATE:
            PREDICATE = Constants.hypernym_annotation
        
        else:
            try:
                PREDICATE = addn_props[triple[1]]
            except:
                try:
                    num_list = properties.properties[triple[1]]
                    PREDICATE = properties.ontologies_list[num_list[0]]
                except:
                    None

            
        return (SUBJECT, PREDICATE, OBJECT)
    
        
    def annotate(self, text):
        return spotlight.annotate(self.spotlight_address, text)

    


