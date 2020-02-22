#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
""" PMI Assigment
Build  a dictionary for frequency of unigram and bigram
"""
__author__="Quang Minh Do"

import re, sys

class CorpusStats:
    def __init__(self, filename):
        self.text = self.read_file(filename)
        self.text = self.remove_special_characters(self.text)
        self.ngrams_dict = {}

        # count of all words
        self.words_count = self.get_words_count()

        one_gram = self.ngrams(1)
        bi_gram = self.ngrams(2)
        self.ngrams_dict.update(self.build_ngrams_dict(one_gram))
        self.ngrams_dict.update(self.build_ngrams_dict(bi_gram))

    def read_file(self, filename):
        try:
            file = open(filename, "r")
            return file.read()
        except:
            print("File not found")
            return

    def get_words_count(self):
        return len(self.text.split(' '))

    def ngrams(self, n):
        self.text = self.text.lower()
        words = self.text.split(' ')

        return (
            [' '.join(words[i:i + n]) for i in range(len(words) - n + 1)]
        )

    def build_ngrams_dict(self, data):
        words_dict = {}

        for word in data:
            # bigrams are separated by underscore
            word = re.sub(r'\s', '_', word)

            count = words_dict.get(word, 0) + 1
            words_dict[word] = count

        return words_dict

    def format_data(self):
        fdata = ""
        for key, val in self.ngrams_dict.items():
            fdata += "{}\t{}\n".format(key, val)

        fdata += "@total@\t{}".format(str(self.words_count))
        return fdata

    def save_data(self, output_filename):
        fdata = self.format_data()
        file = open(output_filename, 'w')
        file.write(fdata)
        file.close()

    def remove_special_characters(self, line):
        line = line.strip()
        line = re.sub('[^a-z0-9 ]+', '', line)
        line = re.sub('[\s\s]+', ' ', line)
        return line


#####################
# Testing
def testing():
    c_stats = CorpusStats('shorterReviews.txt')
    c_stats.save_data('out.dat')

#testing()


######################
# Production
input_filename = sys.argv[1]
output_filename = sys.argv[2]
c_stats = CorpusStats(input_filename)
c_stats.save_data(output_filename)
