from .properties import Properties
from nltk.stem import PorterStemmer
from .Constants import Constants
import re

props = Properties()
ps = PorterStemmer()

def parse_hearst_patterns(q_hearst_patterns):
    patterns = [ r[1:-1].split(',') for r in  q_hearst_patterns.split(';') ] #delimter for the input hearst patterns
    return patterns

def add_hearst_patterns(template, t):
    """
    Template is of the form 
    ({verb+preposition}, first/last)
    The pattern is then converted into its' type which can be 
        - default
        - non-greedy
        - semi-greedy

    The first/last part is added as a regex parameter
    """
    try:
        verb, proposition = template[0].split("_") # "_" is the default delimiter, mentioned in the Properties class
    except:
        raise RuntimeError("delimiter is not set to the proper value, check the properties file")

    pattern = None
    if t == 'Default':
        pattern = r'NP_(\w+).*?({}).*?{}.*?.*?NP_(\w+)'.format(verb, preposition)
    elif t == 'Non-Greedy':
        pattern = r'.*NP_(\w+).*?({}).*?{}.*?NP_(\w+)'.format(verb, preposition)
    else:
        pattern = r'.*?NP_(\w+).*?({}).*?{}.*?NP_(\w+)'.format(verb, preposition)

    heart_pattern = (pattern, template[1], verb+preposition.capitalize(), 3)
    return heart_pattern


def create_default():
    patterns = list()
    for val in list(props.properties.keys()): 
        verb, preposition  = val.split(props.DELIMITER)
        pattern = r'NP_(\w+).*?({}).*?{}.*?.*?NP_(\w+)'.format(verb, preposition)
        for num in props.properties[val]:
            t = props.ontologies_list[num][1]
            patterns.append((pattern, t, verb+preposition.capitalize(), 3))
    return patterns

def create_greedy():
    patterns = list()
    for val in list(props.properties.keys()): 
        verb, preposition  = val.split(props.DELIMITER)
        pattern = r'.*NP_(\w+).*?({}).*?{}.*?NP_(\w+)'.format(verb, preposition)
        for num in props.properties[val]:
            t = props.ontologies_list[num][1]
            patterns.append((pattern, t, verb+preposition.capitalize(), 3))
    return patterns

def create_semi():
    patterns = list()
    for val in list(props.properties.keys()): 
        verb, preposition  = val.split(props.DELIMITER)
        pattern = r'.*?NP_(\w+).*?({}).*?{}.*?NP_(\w+)'.format(verb, preposition)
        for num in props.properties[val]:
            t = props.ontologies_list[num][1]
            patterns.append((pattern, t, verb+preposition.capitalize(), 3))
    return patterns

    
def annotate_predicate_ps(predicate):
    root_verb = ps.stem(predicate[0])
    prepositons = Constants.prepositons
    annotations = list()
    k = list()
    for word in predicate[1]:
        if word in prepositons:
            k.append(word)
    for prep in k:
        p = root_verb+props.DELIMITER+prep
        try:
            nums = props.properties[p]
            for number in nums:
                annotations.append(props.ontologies_list[number][0])
        except:
            None
    if len(annotations) == None:
        return None
    else:
        return annotations

def clean_hearst_triple(triple):
    SUBJECT = triple[0]
    OBJECT = triple[2]
    PREDICATE = props.DELIMITER.join([word.lower() for word in re.findall(r'[a-zA-Z][^A-Z]*', triple[1])])
    return (SUBJECT, PREDICATE, OBJECT)
    