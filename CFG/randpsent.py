#!/usr/bin/env python3
""" Context Free Grammars """
__author__ = "Quang Minh Do"

import sys
import re
from collections import defaultdict
import random


class SentenceGenerator:

    def __init__(self, grammar, counts):
        self.sym_dict = defaultdict(list)
        self.gen_sentence(grammar, counts)

    def is_comment(self, str):
        return True if re.search(r'^#', str) else False

    def is_empty(self, str):
        return True if re.search(r'^\n$', str) else False

    # Map symbol to dict
    def gen_sym_dict(self, lines):
        for line in lines:
            if not self.is_comment(line) and not self.is_empty(line):
                l = self.filter_key_val(line)
                key = l[1]
                raw_val = l[2]
                weight = int(l[0])
                filtered_val = re.sub(r'[0-9]+\s', '', raw_val)

                if len(self.sym_dict[key]) == 0:
                    self.sym_dict[key].append([filtered_val])
                    self.sym_dict[key].append([weight])
                else:
                    self.sym_dict[key][0].append(filtered_val)
                    self.sym_dict[key][1].append(weight)

    def filter_key_val(self, str):
        str = re.sub(r'\n', '', str)
        str = re.sub(r'#.*', '', str)
        return re.split(r'\t', str)

    def set_weight(rawVal):
        if (rawVal.split(' ')[0].isdigit()):
            weight = int(rawVal.split(' ')[0])
        else:
            weight = 1

        return weight

    def is_terminal(self, key):
        return True if not key in self.sym_dict else False

    def has_non_terminal(self, sentence):
        l = sentence.split(' ')

        for v in l:
            if (v in self.sym_dict):
                return True

    def pick_rule_from(self, symbol):
        choices = random.choices(self.sym_dict[symbol][0], self.sym_dict[symbol][1], k=1)
        return choices[0]

    def get_next_non_terminal(self, sentence):
        l = sentence.split(' ')
        for v in l:
            if (v in self.sym_dict):
                return v

    def gen_sentence(self, grammar, sentence_count):
        file = open(grammar, "r")
        lines = file.readlines()

        self.gen_sym_dict(lines)

        for i in range(sentence_count):
            sentence = 'ROOT'
            while (self.has_non_terminal(sentence)):
                next_non_terminal = self.get_next_non_terminal(sentence)
                symbol = self.pick_rule_from(next_non_terminal)
                sentence = re.sub(next_non_terminal, symbol, sentence, 1)

            print(sentence)
            print(end="\n")


# ====== Testing


# ======= Production
SentenceGenerator("grammar2.txt", 15)

# count = 1
# if (len(sys.argv) > 2):
#     count = int(sys.argv[2])
#
# SentenceGenerator(sys.argv[1], count)