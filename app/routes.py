from flask import redirect, render_template, jsonify, request, make_response, abort, g, session, Response
from flask_cors import CORS, cross_origin

from app import app_flask
from .src.pyspotlight import spotlight
import nltk

spotlight_config = spotlight.Config()
spotlight_address = spotlight_config.spotlight_address

@app_flask.route('/', methods=['GET'])
@cross_origin(supports_credentials=True)
def index():
    return render_template('index.html')


@app_flask.route('/search', methods = ['GET', 'POST'])
def search():

    annotations = None
    annotated_text = list()
    q_text = request.form.get("comment")
    q_confidence = request.form.get("confidence")
    q_spotlight = request.form.get("allow_spotlight")

    sentences = nltk.sent_tokenize(q_text)
    word_tokenized_sentences = list()
    all_words = list()
    for sent in sentences:
        words = nltk.word_tokenize(sent)
        word_tokenized_sentences.append(words)
        all_words.extend(words)

    print(all_words)
    print(q_spotlight)
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


    print(annotated_text)
    return render_template('triplets.html', annotations=annotations, annotated_text=annotated_text)
    