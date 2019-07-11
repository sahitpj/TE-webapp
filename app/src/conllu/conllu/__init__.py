from __future__ import unicode_literals

from conllu.models import TokenList
from conllu.parser import parse_token_and_metadata


def parse(data, fields=None, field_parsers=None):
    '''
    Here we assume a multiple sentence conll files conll files, however since we are handling single sentence conll files,
    we shall assume so, unless stated otherwise. For this we shall define a new function parse_single
    '''
    return [
        TokenList(*parse_token_and_metadata(sentence, fields=fields, field_parsers=field_parsers))
        for sentence in data.read()
        if sentence
    ]


def parse_single(data, fields=None, field_parsers=None):
    '''
    parse single is the function which shall handle single conll sentence files.
    '''
    l = data.read()
    return [
        TokenList(*parse_token_and_metadata(l, fields=fields, field_parsers=field_parsers))
    ]

def parse_incr(in_file, fields=None, field_parsers=None):
    for sentence in _iter_sents(in_file):
        yield TokenList(*parse_token_and_metadata(sentence, fields=fields, field_parsers=field_parsers))

def parse_tree(data):
    tokenlists = parse(data)

    sentences = []
    for tokenlist in tokenlists:
        sentences.append(tokenlist.to_tree())

    return sentences

def parse_tree_incr(in_file):
    for tokenlist in parse_incr(in_file):
        yield tokenlist.to_tree()

def _iter_sents(in_file):
    buf = []
    for line in in_file:
        if line == "\n":
            yield "".join(buf)[:-1]
            buf = []
        else:
            buf.append(line)
    if buf:
        yield "".join(buf)
