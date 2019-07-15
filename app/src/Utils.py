from .Constants import Constants
from .spotlight import Spotlight_Pipeline 

constants = Constants()
spipe = Spotlight_Pipeline()

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
    SUBJECT = hypernym[0][0]
    PREDICATE = 'hypernym'
    OBJECT = hypernym[2][0]
    return (SUBJECT, PREDICATE, OBJECT)


def directRelation_clean(direct_relation):
    SUBJECT = direct_relation[0][0]
    PREDICATE = direct_relation[1]
    if PREDICATE == 'nmod':
        PREDICATE = 'hypernym (low confidence)'
    OBJECT = direct_relation[2][0]
    return (SUBJECT, PREDICATE, OBJECT)

def short_relations_clean(short_relation):
    # The following method assumes the level goes to 2 only. A generalized algorithm will be written later
    SUBJECT = short_relation[0][0]
    relations = list()
    for p in short_relation[1]:
        if p[0][1] in constants.VERBS:
            PREDICATE = p[0][0]
            OBJECT = p[2][0]
            relations.append((SUBJECT, PREDICATE, OBJECT))
    return relations
        
def annotate_triple(triple):
    SUBJECT = None
    PREDICATE = triple[1]
    OBJECT = None
    if isinstance(triple[0], list):
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

    if isinstance(triple[2], list):
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

    return (SUBJECT, PREDICATE, OBJECT)
    