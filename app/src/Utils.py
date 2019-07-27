from .Constants import Constants
from .spotlight import Spotlight_Pipeline 
from .properties import Properties
from nltk.stem import PorterStemmer

constants = Constants()
properties = Properties()
ps = PorterStemmer()

def hearst_get_triplet(hearst_pattern):
    OBJECT = None
    PREDICATE = hearst_pattern[-2] #the property
    SUBJECT = hearst_pattern[-3]
    if hearst_pattern[-1] == 'first':
        OBJECT = hearst_pattern[0][-1]
    else:
        OBJECT = hearst_pattern[0][0]
    return (SUBJECT, PREDICATE, OBJECT)

def hypernym_clean(hypernym):
    """
    Used for the case of dependencies, where words are returned along with the POS
    """
    SUBJECT = hypernym[0][0]
    PREDICATE = 'hypernym'
    OBJECT = hypernym[2][0]
    return (SUBJECT, PREDICATE, OBJECT)


def directRelation_clean(direct_relation):
    """
    Nmod relation is converted to a hypernym relation of low confidence
    """
    SUBJECT = direct_relation[0][0]
    PREDICATE = direct_relation[1]
    if PREDICATE == 'nmod':
        PREDICATE = 'hypernym (low confidence)'
    OBJECT = direct_relation[2][0]
    return (SUBJECT, PREDICATE, OBJECT)

def short_relations_clean(short_relation, prepositions):
    # The following method assumes the level goes to 2 only. A generalized algorithm will be written later
    SUBJECT = short_relation[0][0]
    print(prepositions)
    OBJECT = short_relation[1][-1][-1][0]
    relations = list()
    predicates = list()
    for p in short_relation[1]:
        if p[0][1] in constants.VERBS:
            PREDICATE = p[0][0]
            predicates.append(PREDICATE)
    for predicate in predicates:
        for preposition in prepositions:
            relations.append((SUBJECT, Properties.DELIMITER.join([ps.stem(predicate), get_preposition(preposition)]), OBJECT))
    return relations
        
def annotate_triple(triple, language):
    spipe = Spotlight_Pipeline(language)
    SUBJECT = None
    PREDICATE = None
    OBJECT = None
    if isinstance(triple[0], list) or isinstance(triple[0], tuple):
        main_word = triple[0][0]
        combined_word = ' '.join(list(triple[0][1]) + list(triple[0][0]))
        annotation = spipe.annotate_word(combined_word)
        print(annotation)
        if annotation[0] == combined_word:
            annotation = spipe.annotate_word(main_word)
        if annotation[0] != main_word:
            SUBJECT = annotation
    else:
        annotation = spipe.annotate_word(triple[0])
        if annotation[0] != triple[0]:
            SUBJECT = annotation

    if isinstance(triple[2], list) or isinstance(triple[0], tuple):
        main_word = triple[2][0]
        combined_word = ' '.join(list(triple[2][1]) + list(triple[2][0]))
        annotation = spipe.annotate_word(combined_word)[0]
        if annotation[0] == combined_word:
            annotation = spipe.annotate_word(main_word)
        if annotation[0] != main_word:
            OBJECT = annotation
    else:
        annotation = spipe.annotate_word(triple[2])
        if annotation[0] != triple[2]:
            OBJECT = annotation

    if triple[1] == Constants.hypernym_PREDICATE:
        PREDICATE = Constants.hypernym_annotation
    
    else:
        try:
            num_list = properties.properties[triple[1]]
            PREDICATE = properties.ontologies_list[num_list[0]]

        except:
            None
        
    return (SUBJECT, PREDICATE, OBJECT)
    

def get_preposition(dep):
    return dep[2][0]