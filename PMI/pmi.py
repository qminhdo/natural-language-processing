#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
""" PMI Assigment
Calculate Pointwise Mutial Information
"""

__author__="Quang Minh Do"

import re, sys, math

c_count_dict = {}

def build_corpus_count_dict(filename):
    try:
        file = open(filename, "r")
    except:
        print("File not found")
        return

    lines = file.readlines()

    for str in lines:
        str = re.sub(r'\n', '', str)
        str = str.split('\t')
        key = str[0]
        val = str[1]

        c_count_dict[key] = val

def cal_pmi(words_list):
    words = '_'.join(words_list)
    words_count = int(c_count_dict[words])

    corpus_words_count = int(c_count_dict['@total@'])
    first_word_count = int(c_count_dict[words_list[0]])
    second_word_count = int(c_count_dict[words_list[1]])

    p = (words_count * corpus_words_count) / (first_word_count * second_word_count)
    return round(math.log(p,2), 2)


######################
# Testing
def testing():
    sys_input = "the future"
    build_corpus_count_dict('out.dat')

# testing()

######################
# Production
filename = sys.argv[1]
words = sys.argv[2:]

build_corpus_count_dict(filename)
print(cal_pmi(words))