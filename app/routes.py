from flask import redirect, render_template, jsonify, request, make_response, abort, g, session, Response
from flask_cors import CORS, cross_origin

from app import app_flask
from .src.pyspotlight import spotlight
from .src.hpatterns import HearstPatterns
from .src.Utils import hearst_get_triplet, hypernym_clean, directRelation_clean, short_relations_clean, annotate_triple
from .src.treegex import TripleExtraction
from .src.deps import TripleExtraction_Deps
from nltk.tokenize import sent_tokenize
import nltk

spotlight_config = spotlight.Config()
spotlight_address = spotlight_config.spotlight_address

METHODS = ['Hearst Patterns', 'Parse-Tree', 'Dependencies', 'Dependencies with coreferences']
HEARST_PATTERNS_METHODS = ['Default', 'Non-greedy', 'Semi-greedy']

@app_flask.route('/', methods=['GET'])
@cross_origin(supports_credentials=True)
def index():
    return render_template('index.html')


@app_flask.route('/search', methods = ['GET', 'POST'])
def search():
    """
    Triplet extraction function for the application. Triggered by the 'get triplets' button
    """
    triples = list()
    annotations = None
    annotated_text = list()
    q_text = request.form.get("comment")
    q_confidence = request.form.get("confidence")
    q_spotlight = request.form.get("allow_spotlight")
    q_method = request.form.get("method")

    print(q_method)

    sentences = nltk.sent_tokenize(q_text)
    word_tokenized_sentences = list()
    all_words = list()
    for sent in sentences:
        words = nltk.word_tokenize(sent)
        word_tokenized_sentences.append(words)
        all_words.extend(words)

    if q_spotlight:
        annotations = spotlight.annotate(spotlight_address,
                                        q_text)
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


    if q_method == METHODS[0]:
        hpatterns1 = None
        hpatterns2 = None
        patterns1 = None
        patterns2 = None
        q_pattern_method = request.form.get("pattern-method")
        if q_pattern_method == HEARST_PATTERNS_METHODS[0]:
            hpatterns1 = HearstPatterns(extended = True, same_sentence = True)
            hpatterns2 = HearstPatterns(extended = True, same_sentence = False)
            patterns1 = [ hearst_get_triplet(pattern) for pattern in hpatterns1.find_hearstpatterns_spacy(q_text)]
            patterns2 = [ hearst_get_triplet(pattern) for pattern in hpatterns2.find_hearstpatterns_spacy(q_text)]
            print(patterns1, patterns2)
            
        elif q_pattern_method == HEARST_PATTERNS_METHODS[1]:
            hpatterns1 = HearstPatterns(extended = True, same_sentence = True, greedy = True)
            hpatterns2 = HearstPatterns(extended = True, same_sentence = False, greedy = True)
            patterns1 = [ hearst_get_triplet(pattern) for pattern in hpatterns1.find_hearstpatterns_spacy(q_text)]
            patterns2 = [ hearst_get_triplet(pattern) for pattern in hpatterns2.find_hearstpatterns_spacy(q_text)]
        else:
            hpatterns1 = HearstPatterns(extended = True, same_sentence = True, semi = True)
            hpatterns2 = HearstPatterns(extended = True, same_sentence = False, semi = True)
            patterns1 = [ hearst_get_triplet(pattern) for pattern in hpatterns1.find_hearstpatterns_spacy(q_text)]
            patterns2 = [ hearst_get_triplet(pattern) for pattern in hpatterns2.find_hearstpatterns_spacy(q_text)]

        triples += patterns1 + patterns2

    elif q_method == METHODS[1]:
        text_extraction = TripleExtraction()
        triplets = list()
        for sentence in sent_tokenize(q_text):
            triple = text_extraction.treebank(sentence)
            triplets.append(triple)
        print(triplets)
        triples += triplets

    elif q_method == METHODS[2] or q_method == METHODS[3]:

        NOUN_RELATIONS = ['nmod', 'hypernym (low confidence)']

        text_extraction = TripleExtraction_Deps()
        text_extraction_tree = TripleExtraction()
        triplets = list()
        sr = list()
        for sentence in sent_tokenize(q_text):
            triple = text_extraction_tree.treebank(sentence)
            dependencies = text_extraction.dependency_triplets(sentence)
            direct_relations, short_relations, hypernyms = text_extraction.short_relations(dependencies, 2)
            sr.extend(short_relations)
            cleaned_hypernyms = [ hypernym_clean(hypernym) for hypernym in hypernyms ]
            cleaned_drs = [ directRelation_clean(direct_relation) for direct_relation in direct_relations ]
            for i in cleaned_drs:
                if i[1] in NOUN_RELATIONS:
                    triplets.append(i)
            for short_relation in sr:
                triplets.extend(short_relations_clean(short_relation))
            triplets.extend(cleaned_hypernyms)
            triplets.append(triple)
        # print(triplets)
        # print(direct_relations)
        print(sr)
        triples += triplets

    annotated_triples = None
    if q_spotlight:
        annotated_triples = list()
        for triple in triples:
            annotated_triples.append(annotate_triple(triple))
        

    return render_template('triplets.html', annotations=annotations, annotated_text=annotated_text, triplets=triples, q_text=q_text, annotated_triples=annotated_triples)
    