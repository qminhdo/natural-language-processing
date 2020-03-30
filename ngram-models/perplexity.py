#!/usr/bin/env python3

""" ngram model homework """
__author__ = "Quang Minh Do"

import sys, re
import math
import codecs
s_test_model = __import__("s-test-model")

class Perplexity:
    def __init__(self, model_filename, sentences_filename):
        self.sentences_filename = sentences_filename
        self.model_filename = model_filename
        self.sentences_words_count = 0
        self.sentences_count = 0
        self.build_sentences()

        tm = s_test_model.STestModel(model_filename, sentences_filename)
        self.probs = tm.compute_prob_sentences()

    def build_sentences(self):
        self.sentences = self.read_file(self.sentences_filename).read()
        self.sentences = self.remove_special_characters(self.sentences)
        self.sentences = self.sentences.split(".")

        for sentence in self.sentences:
            sentence = sentence.strip()

            if not (len(sentence) == 0):
                self.sentences_count += 1
                # print(sentence.split(' '))
                self.sentences_words_count += len(sentence.split(' '))

    def compute_I(self, probs, sentences_words_count):
        # sum of all prob divide by total of words in test data
        log_probs_total = self.compute_log_prob(probs)
        return log_probs_total * (1/ sentences_words_count)

    def compute_log_prob(self, probs):
        log_probs_total = 0

        for prob in probs:
            if (prob == 0.0):
                prob = 1e-5
            log_probs_total += math.log(prob, 2)

        return log_probs_total

    def compute_perplexity(self):
        i = self.compute_I(self.probs, self.sentences_words_count)

        return 2**(-i)

    def remove_special_characters(self, text):
        text = text.strip()
        text = re.sub(r'[^A-Za-z0-9.]', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        return text

    def read_file(self, filename):
        try:


            file = codecs.open(filename , encoding="Latin-1", errors="replace")
            # file = open(filename, mode="r", encoding="utf-8",errors="replace")
            return file
        except:
            print("File not found")
            return



######################
# Production
if __name__ == "__main__":
    # model_filename = sys.argv[1]
    # sentences_filename = sys.argv[2]
    model_filename = "text/Othello.model"
    sentences_filename = "text/utf8"
    p = Perplexity(model_filename, sentences_filename)
    print("Perpexity:", p.compute_perplexity())
