from __future__ import print_function, unicode_literals

from collections import OrderedDict
import re

from .compat import text
from .parser import ParseException, head_to_token, serialize

DEFAULT_EXCLUDE_FIELDS = ('id', 'deprel', 'feats', 'head', 'deps', 'misc')


class TokenList(list):
    metadata = None

    def __init__(self, tokens, metadata=None):
        super(TokenList, self).__init__(tokens)
        if not isinstance(tokens, list):
            raise ParseException("Can't create TokenList, tokens is not a list.")

        self.metadata = metadata

    def __repr__(self):
        return 'TokenList<' + ', '.join(token['form'] for token in self) + '>'

    def __eq__(self, other):
        return super(TokenList, self).__eq__(other) \
            and (not hasattr(other, 'metadata') or self.metadata == other.metadata)

    def __ne__(self, other):
        return not self == other

    def clear(self):
        self[:] = []  # Supported in Python 2 and 3, unlike clear()
        self.metadata = None

    def copy(self):
        tokens_copy = self[:]  # Supported in Python 2 and 3, unlike copy()
        return TokenList(tokens_copy, self.metadata)

    def extend(self, iterable):
        super(TokenList, self).extend(iterable)
        if hasattr(iterable, 'metadata'):
            if hasattr(self.metadata, '__add__') and hasattr(iterable.metadata, '__add__'):
                self.metadata += iterable.metadata
            elif type(self.metadata) is dict and type(iterable.metadata) is dict:
                # noinspection PyUnresolvedReferences
                self.metadata.update(iterable.metadata)
            else:
                self.metadata = [self.metadata, iterable.metadata]

    def get_noun_chunks(self, subject):
        NP = ['NN', 'NNS', 'NNP', 'NNPS']
        AJ = ['JJ', 'JJR', 'JJS']
        if len(self) > 0 and isinstance(self[0], OrderedDict):
            annotated_sentence = list()
            for word in self:
                annotated_sentence.append("{}_{}".format(word['xpostag'], word['form']))
            flag = 0
            noun_chunks = []
            stack = []
            for i in annotated_sentence:
                matches = re.search(r'([\w.,]+)_([\w.,]+)', i)
                if matches and matches.group(1) in NP:
                    if flag == 0:
                        flag = 1
                    stack.append(matches.group(2))

                    if stack[-1][-1] == '.':
                        stack[-1] = stack[-1][:-1]
                        noun_chunks.append('_'.join(['NP'] + stack))
                        noun_chunks.append('.')
                        flag = 0
                        stack = []
                else:
                    if flag == 1:
                        noun_chunks.append('_'.join(['NP'] + stack))
                        stack = []
                        flag = 0
                    try:
                        if matches.group(2) in ['.', ';', ':', ',']:
                            noun_chunks.append(matches.group(1))
                        elif matches.group(1) == 'CD':
                            noun_chunks.append(i)
                        elif matches.group(1) in AJ:
                            noun_chunks.append('AJ_' + matches.group(2))
                        elif matches.group(1) == 'PRP':
                            if subject:
                                noun_chunks.append('NP_' + subject)
                            else:
                                noun_chunks.append('NP_' + matches.group(2))
                        else:
                            noun_chunks.append(matches.group(2))
                    except:
                        noun_chunks.append(',')

                
            return ' '.join(noun_chunks)
        else:
            raise ParseException("Can't create noun chuncks for a group of sentences")

    @property
    def tokens(self):
        return self

    @tokens.setter
    def tokens(self, value):
        self[:] = value  # Supported in Python 2 and 3, unlike clear()

    def serialize(self):
        return serialize(self)

    def to_tree(self):
        def _create_tree(head_to_token_mapping, id_=0):
            return [
                TokenTree(child, _create_tree(head_to_token_mapping, child["id"]))
                for child in head_to_token_mapping[id_]
            ]

        root = _create_tree(head_to_token(self))[0]
        root.set_metadata(self.metadata)
        return root


class TokenTree(object):
    token = None
    children = None
    metadata = None

    def __init__(self, token, children, metadata=None):
        self.token = token
        self.children = children
        self.metadata = metadata

    def set_metadata(self, metadata):
        self.metadata = metadata

    def __repr__(self):
        return 'TokenTree<' + \
            'token={id=' + text(self.token['id']) + ', form=' + self.token['form'] + '}, ' + \
            'children=' + ('[...]' if self.children else 'None') + \
            '>'

    def __eq__(self, other):
        return self.token == other.token and self.children == other.children \
            and self.metadata == other.metadata

    def serialize(self):
        if not self.token or "id" not in self.token:
            raise ParseException("Could not serialize tree, missing 'id' field.")

        def flatten_tree(root_token, token_list=[]):
            token_list.append(root_token.token)

            for child_token in root_token.children:
                flatten_tree(child_token, token_list)

            return token_list

        tokens = flatten_tree(self)
        tokens = sorted(tokens, key=lambda t: t['id'])
        tokenlist = TokenList(tokens, self.metadata)

        return serialize(tokenlist)

    def print_tree(self, depth=0, indent=4, exclude_fields=DEFAULT_EXCLUDE_FIELDS):
        if not self.token:
            raise ParseException("Can't print, token is None.")

        if "deprel" not in self.token or "id" not in self.token:
            raise ParseException("Can't print, token is missing either the id or deprel fields.")

        relevant_data = self.token.copy()
        for key in exclude_fields:
            if key in relevant_data:
                del relevant_data[key]

        node_repr = ' '.join([
            '{key}:{value}'.format(key=key, value=value)
            for key, value in relevant_data.items()
        ])

        print(' ' * indent * depth + '(deprel:{deprel}) {node_repr} [{idx}]'.format(
            deprel=self.token['deprel'],
            node_repr=node_repr,
            idx=self.token['id'],
        ))
        for child in self.children:
            child.print_tree(depth=depth + 1, indent=indent, exclude_fields=exclude_fields)
