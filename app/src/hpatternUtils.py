from .properties import Properties
from nltk.stem import PorterStemmer
from .Constants import Constants
import re

props = Properties()
ps = PorterStemmer()

def parse_hearst_patterns(q_hearst_patterns):
    patterns = [ r[1:-1].split(',') for r in  q_hearst_patterns.split(';') ] #delimter for the input hearst patterns
    return patterns


def add_hearst_patterns(templates, t, q_hearst_input):
    """
    1. Template is of the form 
    ({verb+preposition}, first/last)
    The pattern is then converted into its' type which can be 
        - default
        - non-greedy
        - semi-greedy

    The first/last part is added as a regex parameter

    2. Template is where the direct required template format is inputted.
    in such a case the templates are directly returned
    """
    if q_hearst_input =='verb+prep':
        hearst_patterns = list()
        props = list()
        for template in templates:
            props.append((template[0], template[-1]))
            if len(template) > 2:
                try:
                    verb, preposition = template[0].split("_") # "_" is the default delimiter, mentioned in the Properties class
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
                hearst_patterns.append(heart_pattern)
        return hearst_patterns, props
    else:
        props = list()
        hearst_patterns = list()
        for template in templates:
            if len(template) == 2:
                props.append((template[0], template[-1]))
            else:
                props.append((template[2], template[-1]))
                hearst_patterns.append(template[:-1])
        return hearst_patterns, props


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
    