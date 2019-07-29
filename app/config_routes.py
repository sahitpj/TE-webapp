from flask import redirect, render_template, jsonify, request, make_response, abort, g, session, Response
from flask_cors import CORS, cross_origin

from app import app_flask
from .src.pyspotlight import spotlight
from .src.hpatterns import HearstPatterns
from .src.hpatternUtils import parse_hearst_patterns, add_hearst_patterns
from .src.Utils import hearst_get_triplet, hypernym_clean, directRelation_clean, short_relations_clean, annotate_triple
from .src.parseTree import TripleExtraction
from .src.deps import TripleExtraction_Deps, TripleExtraction_Deps_SS
from .src.multiLang import TripleExtraction_Deps_Lang, TripleExtraction_Lang
from .src.spotlight import Spotlight_Pipeline
from nltk.tokenize import sent_tokenize
import nltk

# spotlight_config = spotlight.Config()
# spotlight_address = spotlight_config.spotlight_address

HEARST_PATTERNS_METHODS = ['Default', 'Non-greedy', 'Semi-greedy']

@app_flask.route('/config', methods=['GET'])
def getConfigPage():
    return render_template('config.html')

@app_flask.route('/config-search', methods=['GET', 'POST'])
def getConfigResults():
    q_allow_given_hearst = request.form.get("allow_given_hearst")
    q_hearst_pattern_type = request.form.get("pattern-method")
    q_use_parse_tree = request.form.get("parse-tree")
    q_use_dependencies = request.form.get("use-dependencies")
    q_dependency_num = request.form.get("dependencies-number")
    q_text = request.form.get("comment")
    q_spotlight = request.form.get("spotlight")
    q_hearst_input = request.form.get("hearst-input-type")
    q_language = request.form.get("language")

    hearst_patterns = request.form.get("hearst-patterns")

    triples = list()

    annotations = None
    annotated_text = list()

    if q_spotlight == 'Yes':
        spipe = Spotlight_Pipeline(q_language)
        annotations = spipe.annotate(q_text)                              
        ptr = 0
        flag = 0
        annotated_text.append([0, q_text[:annotations[0]['offset']]])
        start_ptr = len(annotations[0]['surfaceForm']) + annotations[0]['offset']
        annotated_text.append([1, annotations[0]])
        for i in range(1, len(annotations)):
            end_ptr = annotations[i]['offset']
            annotated_text.append([0, q_text[start_ptr:end_ptr]])
            start_ptr = end_ptr + len(annotations[i]['surfaceForm'])
            annotated_text.append([1, annotations[i]])

    if q_allow_given_hearst:
        hpatterns1 = None
        hpatterns2 = None
        patterns1 = None
        patterns2 = None
        if q_hearst_pattern_type == HEARST_PATTERNS_METHODS[0]:
            addn_patterns = add_hearst_patterns(parse_hearst_patterns(hearst_patterns), q_hearst_pattern_type, q_hearst_input)
            hpatterns1 = HearstPatterns(extended = True, same_sentence = True)
            hpatterns1.add_patterns(addn_patterns, q_hearst_pattern_type)
            hpatterns2 = HearstPatterns(extended = True, same_sentence = False)
            hpatterns2.add_patterns(addn_patterns, q_hearst_pattern_type)
            patterns1 = [ hearst_get_triplet(pattern) for pattern in hpatterns1.find_hearstpatterns_spacy(q_text)]
            patterns2 = [ hearst_get_triplet(pattern) for pattern in hpatterns2.find_hearstpatterns_spacy(q_text)]
            print(patterns1, patterns2)
            
        elif q_hearst_pattern_type == HEARST_PATTERNS_METHODS[1]:
            addn_patterns = add_hearst_patterns(parse_hearst_patterns(hearst_patterns), q_hearst_pattern_type, q_hearst_input)
            hpatterns1 = HearstPatterns(extended = True, same_sentence = True, greedy = True)
            hpatterns1.add_patterns(addn_patterns, q_hearst_pattern_type)
            hpatterns2 = HearstPatterns(extended = True, same_sentence = False, greedy = True)
            hpatterns2.add_patterns(addn_patterns, q_hearst_pattern_type)
            patterns1 = [ hearst_get_triplet(pattern) for pattern in hpatterns1.find_hearstpatterns_spacy(q_text)]
            patterns2 = [ hearst_get_triplet(pattern) for pattern in hpatterns2.find_hearstpatterns_spacy(q_text)]
        else:
            addn_patterns = add_hearst_patterns(parse_hearst_patterns(hearst_patterns), q_hearst_pattern_type, q_hearst_input)
            hpatterns1 = HearstPatterns(extended = True, same_sentence = True, semi = True)
            hpatterns1.add_patterns(addn_patterns, q_hearst_pattern_type)
            hpatterns2 = HearstPatterns(extended = True, same_sentence = False, semi = True)
            hpatterns2.add_patterns(addn_patterns, q_hearst_pattern_type)
            patterns1 = [ hearst_get_triplet(pattern) for pattern in hpatterns1.find_hearstpatterns_spacy(q_text)]
            patterns2 = [ hearst_get_triplet(pattern) for pattern in hpatterns2.find_hearstpatterns_spacy(q_text)]

        triples += patterns1 + patterns2

    if q_use_parse_tree == 'Yes':
        if q_language == 'English':
            text_extraction = TripleExtraction()
            triplets = list()
            for sentence in sent_tokenize(q_text):
                triple = text_extraction.treebank(sentence)
                triplets.append(triple)
            print(triplets)
            triples += triplets
        else:
            text_extraction = TripleExtraction_Lang(q_language)
            triplets = list()
            for sentence in sent_tokenize(q_text):
                triple = text_extraction.treebank(sentence)
                triplets.append(triple)
            print(triplets)
            triples += triplets


    if q_use_dependencies == 'Yes':
        NOUN_RELATIONS = ['nmod', 'hypernym (low confidence)']
        text_extraction = None
        if q_language == 'English':
            text_extraction = TripleExtraction_Deps()
        else:
            text_extraction = TripleExtraction_Deps_Lang(q_language)
        triplets = list()
        sr = list()
        sr_preps = list()
        cleaned_hypernyms = list()
        for sentence in sent_tokenize(q_text):
            # triple = text_extraction_tree.treebank(sentence)
            # triplets.append(triple)
            dependencies = text_extraction.dependency_triplets(sentence)
            direct_relations, short_relations, hypernyms, prepositions = text_extraction.short_relations(dependencies, 2)
            sr.extend(short_relations)
            sr_preps.extend(prepositions)
            cleaned_hypernyms.extend([ hypernym_clean(hypernym) for hypernym in hypernyms ])
            cleaned_drs = [ directRelation_clean(direct_relation) for direct_relation in direct_relations ]
            for i in cleaned_drs:
                if i[1] in NOUN_RELATIONS:
                    triplets.append(i)
        for short_relation in range(len(sr)):
            triplets.extend(short_relations_clean(sr[short_relation], sr_preps[short_relation]))
        triplets.extend(cleaned_hypernyms)
        triples += triplets
    
    annotated_triples = None
    if q_spotlight == 'Yes':
        spipe = Spotlight_Pipeline(q_language)
        annotated_triples = list()
        for triple in triples:
            annotated_triples.append(spipe.annotate_triple(triple))

    return render_template('triplets.html', annotations=annotations, annotated_text=annotated_text, triplets=triples, q_text=q_text, annotated_triples=annotated_triples)
