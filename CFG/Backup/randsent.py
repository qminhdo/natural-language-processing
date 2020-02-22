#!/usr/bin/env python3
""" Language Generation homework """
__author__ = "Quang Minh Do"

import sys
import re
from collections import defaultdict
import random


def is_comment(str):
    return True if re.search(r'^#', str) else False


def is_empty(str):
    return True if re.search(r'^\n$', str) else False


# def contains_or(str):
#     return True if re.search(r'.+\|.+', str) else False
#
#
# def split_or(str):
#     str = re.sub(r'\s\|\s', '#', str)
#     return str.split('#')


# Map symbol to dict
def gen_sym_dict(lines):
    for line in lines:
        if not is_comment(line) and not is_empty(line):
            l = filter_key_val(line)
            weight = l[0]
            key = l[1]
            rawVal = l[2]

            sym_dict[key].append(rawVal)
            # if contains_or(rawVal):
            #     val_list = split_or(rawVal)
            #     for val in val_list:
            #         sym_dict[key].append(val)
            # else:
            #     sym_dict[key].append(rawVal)

def filter_key_val(str):
    str = re.sub(r'\n', '', str)
    str = re.sub(r'#.*', '', str)
    return re.split(r'\t', str)


def is_terminal(key):
    return True if not key in sym_dict else False

def has_non_terminal(sentence):
    l = sentence.split(' ')

    for v in l:
        if (v in sym_dict):
            return True

def pick_rule_from(symbol):
    return random.choice(sym_dict[symbol])


def get_next_non_terminal(sentence):
    l = sentence.split(' ')
    for v in l:
        if (v in sym_dict):
            return v

def gen_sentence(grammar, sentence_count):
    file = open(grammar, "r")
    lines = file.readlines()

    gen_sym_dict(lines)

    for i in range(sentence_count):
        sentence = 'ROOT'
        while(has_non_terminal(sentence)):
            next_non_terminal = get_next_non_terminal(sentence)
            symbol = pick_rule_from(next_non_terminal)
            sentence = re.sub(next_non_terminal, symbol, sentence, 1)

        print(sentence)

# ====== Testing


# ======= Production
sym_dict = defaultdict(list)
gen_sentence("grammar.txt", 5)
# gen_sentence(sys.argv[1], int(sys.argv[2]))
print(sym_dict)