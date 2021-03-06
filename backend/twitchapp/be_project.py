# -*- coding: utf-8 -*-
"""BE project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JaKriWy2wmNcCOQoTNdK3VzDb29ry3OE
"""
from demoapp.settings import BASE_DIR
import pandas as pd
import numpy as np
import os
from sklearn.metrics import precision_score, f1_score, accuracy_score, recall_score, \
    precision_recall_fscore_support
import nltk
""" nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet') """

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify

import re, string, random


# eval_data = 'C:/Users/pattn/Downloads/twitch project/data.csv'
# df = pd.read_csv(eval_data, usecols=['message', 'sentiment', 'emotion', 'emotion2'], encoding= 'unicode_escape')

# # eval_data = "labeled_dataset.csv"
# # df = pd.read_csv(eval_data, usecols=['message', 'emotion'], encoding= 'unicode_escape')

# df

# df = df.dropna(subset=['emotion'])

# df['emotion'] = pd.Categorical(df['emotion'])

# df['emotion'].cat.categories

# np.unique(df['emotion'].cat.codes)

# df['emotion_code'] = df['emotion'].cat.codes

# # df[df['emotion_code'] == -1]['emotion_code'] = 2

# df[df['emotion_code'] == 0]

import pandas as pd
l1=['what the hell was that','do it you wont','Fuck your couch!','No Spoils!','u look like u suck dick for money']
df=pd.DataFrame(l1,columns=['message'])

"""## Tokenization"""

# !pip install emoji

import pickle
import re
import emoji
import pandas as pd
from itertools import groupby
from nltk.corpus import stopwords
import os


EMOTICONS = r"""
    (?:
      [<>3Oo0|]?
      [:;=8Xx%]                     # eyes
      [']?                        # optional tear
      [\-o\*\']?                 # optional nose
      [\)\]\(\[dDpP/\:\}\{@\|\\X><c3$LSÞ] # mouth
      |
      [\)\]\(\[dDpP/\:\}\{@\|\\X><c3$LSÞ] # mouth
      [\-o\*\']?                 # optional nose
      [']?                        # optional tear
      [:;=8Xx%]                     # eyes
      [<>Oo0|]?
      |<3|<\/3|<\\3
      |
     \( ͡° ͜ʖ ͡°\)                 # lenny face
    |
    ¯\\_\(ツ\)_/¯                  # meh
      |
      >_>|<_<
      |
      @};-|@}->--|@}‑;‑|@>‑‑>‑‑     #rose
      |
      O_O|o\‑o|O_o|o_O|o_o|O\-O     #schock
      |
      >.<|v.v|>>|<<
      |
      \(>_<\)|\^\^|\^_\^|\(-__-\)|\(-_-\)|\(/◕ヮ◕\)/|\(\^o\^\)丿
      |\('_'\)|\(/_;\)|\(T_T\)|\(;_;\)|\(=\^·\^=\)|\(\*_\*\)|\(\+_\+\)|\(@_@\)
      |\(ง •̀_•́\)ง
    )"""

#pattern to match urls.
URL = r"(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+"

# The components of the tokenizer:
REGEXPS = (
    # ASCII Emoticons
    EMOTICONS
    ,
    # HTML tags:
    r"""<[^>\s]+>"""
    ,
    # ASCII Arrows
    r"""[\-]+>|<[\-]+"""
    ,
    # Twitter like hashtags:
    r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"""
    ,
    # Remaining word types:
    r"""
    #(?:[^\W\d_](?:[^\W\d_]|['\-_])+[^\W\d_]) # Words with apostrophes or dashes.
	(?:[^\W_](?:[^\W\d_]|['\-_\d])+[^\W_]) # Words with apostrophes or dashes. (modified)
    |
    (?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, including fractions, decimals.
    |
    (?:[\w_]+)                     # Words without apostrophes or dashes.
    |
    (?:\.(?:\s*\.){1,})            # Ellipsis dots.
    |
    (?:\S)                         # Everything else that isn't whitespace.
    """
    )

# Regular expression for negation by Christopher Potts
NEGATION = r"""
    (?:
        ^(?:never|no|nothing|nowhere|noone|none|not|
            havent|hasnt|hadnt|cant|couldnt|shouldnt|
            wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint
        )$
    )
    |
    n't"""

URL_RE = re.compile(URL)
NUM = re.compile("(?<=^|(?<=\s)|(?<=\())#{,1}\d{1,}(?=$|(?=\s)|(?=\)))")
USERNAME = re.compile("(?<=^|(?<=\s))@\w+(?=$|(?=\s))")
COMMAND = re.compile("(?<=^|(?<=\s))!#?[a-zA-Z]+(?=$|(?=\s))")
MAIL = re.compile("[\w.+-]+@[\w-]+\.(?:[\w-]\.?)+[\w-]")

SHORTENING_OF =  re.compile("(.)\\1{2,}")

# pattern to find punctuation
CLAUSE_PUNCT = r'^[.:;!?]$'

# pattern to find non alphabetical chars
NON_ALPHABETICAL = re.compile('[^A-Za-z ]')


# create lexicon of emoji
emoji_lexicon = emoji.UNICODE_EMOJI

######################################################################
# This is the core tokenizing regex:

WORD_RE = re.compile(r"""(%s)""" % "|".join(REGEXPS), re.VERBOSE | re.I
                     | re.UNICODE)

# WORD_RE performs poorly on these patterns:
HANG_RE = re.compile(r'([^a-zA-Z0-9])\1{3,}')

# The emoticon string gets its own regex so that we can preserve case for
# them as needed:
EMOTICON_RE = re.compile(EMOTICONS, re.VERBOSE | re.I | re.UNICODE)

# These are for regularizing HTML entities to Unicode:
ENT_RE = re.compile(r'&(#?(x?))([^&;\s]+);')

#negation and punctuation matching patterns
NEGATION_RE = re.compile(NEGATION, re.VERBOSE)
CLAUSE_PUNCT_RE = re.compile(CLAUSE_PUNCT)

def load_labeled_emotes():
    emotes = set(pd.read_table(os.path.join(BASE_DIR,"twitchapp\emote_average.tsv"))["word"])
    return emotes

def mark_negation(token_list, emotes, double_neg_flip=False):
    neg_scope = False
    for i, word in enumerate(token_list):
        if NEGATION_RE.search(word):
            if not neg_scope or (neg_scope and double_neg_flip):
                neg_scope = not neg_scope
                continue
            else:
                token_list[i] += '_NEG'
        elif neg_scope and (CLAUSE_PUNCT_RE.search(word) or word in emotes):
            neg_scope = not neg_scope
        elif neg_scope and not CLAUSE_PUNCT_RE.search(word):
            token_list[i] += '_NEG'

    return token_list

class TwitchTokenizer:

    def __init__(self, preserve_case=True):
        self.preserve_case = preserve_case
        self.emotes = load_labeled_emotes()

    def tokenize(self, text):
        text = URL_RE.sub("URL", text)

        # Shorten problematic sequences of characters
        safe_text = HANG_RE.sub(r'\1\1\1', text)
        # Tokenize:
        words = WORD_RE.findall(safe_text)
        # Possibly alter the case, but avoid changing emoticons like :D into :d:
        if not self.preserve_case:
            words = list(map((lambda x : x if EMOTICON_RE.search(x) else
                              x.lower()), words))
        token_list = []
        for word in words:
            if not re.match(EMOTICON_RE,word):
                if word not in ["URL", "NUM", "USERNAME", "COMMAND", "MAIL"]: # do not lowercase tags
                    word = word.lower()
                # shortening: normalizing of words with chacters occuring more than twice in succession e.g. "looooove" -> "loove"
                word = re.sub(SHORTENING_OF, r'\1\1', word)
            token_list.append(word)

        # remove all non-alphabetical characters, keep line emoticons, unicode-emoji & emotes
        def keep_token(token):
            if re.match(NON_ALPHABETICAL,token) and not re.match(EMOTICON_RE,token) and token not in self.emotes \
            and token not in emoji_lexicon:
                return False
            else:
                return True

        return token_list

def preprocess(df):
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    from nltk.stem import WordNetLemmatizer

    from nltk.tokenize import TweetTokenizer
    tokenizer = TwitchTokenizer()
    df['tokenized_message'] = df.apply(lambda row: tokenizer.tokenize(row['message']), axis=1)

    #nltk.download('stopwords')
    en_stopwords = set(stopwords.words('english'))

    en_stopwords.discard('not')

    en_stopwords.add("i'm")
    en_stopwords.add("i've")

    stripped_stopwords = [word.replace("'", "") for word in en_stopwords] 
    negated_stopwords = [word+"_NEG" for word in en_stopwords] 
    [en_stopwords.add(word) for word in stripped_stopwords if word not in en_stopwords]

    def return_new_list(row):
        k = 0
        new_list = list()
        for w in row['tokenized_message']:
            if w not in en_stopwords:
                new_list.append(w)    
        return new_list
    df['new_tokenized_message'] = df.apply(return_new_list, axis=1)
    lemmatizer = WordNetLemmatizer()

    def lemmatize_text(row):
        fin = [lemmatizer.lemmatize(w, 'v') for w in row['new_tokenized_message']]
        return fin
    df['text_lemmatized'] = df.apply(lemmatize_text, axis=1)
    df['final_lemmatized_message'] = [' '.join(map(str, l)) for l in df['text_lemmatized']]
    X_test = df['final_lemmatized_message']
    
    vectorizer = pickle.load(open(os.path.join(BASE_DIR,'twitchapp\\vectorizer.sav'),'rb'))
    X_test  = vectorizer.transform(X_test)
    model = pickle.load(open(os.path.join(BASE_DIR,'twitchapp\\LRModel.sav'),'rb'))

    def model_evaluate_test(model):
        y_pred = model.predict(X_test)
        #print('y_pred')
        #print(y_pred)
        d={0:'Angry', 1:'Disgust', 2:'Excited', 3:'Happy', 4:'Neutral', 5:'Sad', 6:'Surprise'}
        #print(d)
        #print(type(y_pred))
        unique, counts = np.unique(y_pred, return_counts=True)
        c=dict(zip(unique, counts))
        ans={}
        for x in d.keys():
            if(x in c.keys()):
                ans[d[x]]=c[x]
        #print(ans)
        return ans
    y_pred=model_evaluate_test(model)
    return y_pred
#preprocess(df)


