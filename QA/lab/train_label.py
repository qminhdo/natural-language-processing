import re, collections, sys, os
import json
from collections import OrderedDict

from joblib.numpy_pickle_utils import xrange
from nltk import word_tokenize, pos_tag, ne_chunk, parse
from nltk.corpus import stopwords
from nltk.tree import Tree
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from collections import defaultdict
from scipy.sparse import csr_matrix

from sklearn.preprocessing import LabelBinarizer, Normalizer
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier

import scipy.sparse as sps  # sps.csr_matrix, sps.hstack
import numpy


def load_labelled_data(self, filename):
    train_set = []

    with open('data/cogcomp/train_set/train_5500.label', 'r') as f:
        for line in f:
            match = re.match('([A-Z]+:[a-z]+) (.+)', line)
            train_set.append((self.question_features(match.groups()[1]), match.groups()[0]))

    return train_set


def load_keywords(self):
    """Load the keywords in the cogcomp list directory

    :return keywords: { 'what' : ['What'], 'which': ['What'] ... }
    """
    keywords = defaultdict(list)
    dir = "data/cogcomp/lists"
    for dirname, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            with open(os.path.join(dirname, filename), 'r')as f:
                for line in f:
                    keywords[line.strip()].append(filename)
    return keywords


def find_q_type(self):
    train_set = self.load_labelled_data('data/train_set/train_5500.label')
    print(train_set[0])


def question_features(self, question):
    """

    :return features: {"w0:what": 1, "w1:is": 1, "kw:What": 1, "kw:prof": 1 ... }
    """
    features = defaultdict(int)
    words = word_tokenize(question)

    # First few words (positional)
    for idx, w in enumerate(words[0:2]):
        features['w%d:' % idx + w.lower()] = 1

    # Bag of words of keywords
    for word in words:
        if word in self.qc_keywords:
            for keyword in self.qc_keywords[word]:
                # get count of keyword occurence in the question
                features['kw:' + keyword] += 1

    return features


irrelevant_loc_words=["north", "east", "west","south","top","bottom","up","down"]
numbers = ["half","quarter","one","two","three","four","five","six","seven","eight","nine","ten","hundred","hundreds","thousand","thousands","million","millions","billion","billions"]
currency = ["dollar","dollars","pound","pounds","gbp","cent","cents","dime","dimes","penny","rupee","dinar","cost","costs","price","shillings","shilling"]
date_words=["monday","tuesday","wednesday","thursday","friday","saturday","sunday","yesterday","today","tomorrow","january","february","march","april","may","june","july","august","september","october","november","december", "year","years","month","months","decade","decades","century","week","fortnight","night", "weekdays","weeknights","a.m","p.m","a.m.","p.m."]
reason_words=["because","meant","cause","reason"]

POS_KEYS = ["VB","VBD","VBG","VBN","VBP","VBZ","JJ","NNS","NN","CD","JJR","JJS"]
