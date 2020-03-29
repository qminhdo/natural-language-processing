#!/usr/bin/env python3
""" ngram model homework """
__author__ = "Quang Minh Do"

import sys, re

class TestModel:
    def __init__(self, model_filename, sentences_filename):
        self.sentences_filename = sentences_filename
        self.model_filename = model_filename
        self.sentences = self.read_file(self.sentences_filename).read().split(".")

        self.words_count = 0
        self.ngram_model = {}
        self.build_ngram_model()


    def compute_prob_sentences(self):
        prob_list = []
        for sentence in self.sentences:
            prob = 1
            sentence = sentence.strip()

            words = sentence.split(' ')
            words.reverse()
            words.append("*")
            words.append("*")
            words.reverse()
            words.append("STOP")

            for word in words[2:]:
                word_index = words.index(word)
                previous_word = words[word_index - 1]
                previous_2_word = words[word_index - 2]

                prob *= self.qml(word, previous_2_word, previous_word)

            prob_list.append(prob)

        return prob_list


    def qml(self, wi, wi2, wi1):
        # compute maximum likelihood estimate
        # check if words exist in the ngram model
        # q(wi | wi-2, wi-1) = Count(wi-2, wi-1, wi) / Count(wi-2, wi-1)
        trigram = wi2 + " " + wi1 + " " + wi
        bigram = wi2 + " " + wi1

        if (bigram == "* *"):
            bigram = "STOP"

        if not (trigram in self.ngram_model.keys()) \
                or not (bigram in self.ngram_model.keys()):
            return 0

        trigram_count = int(self.ngram_model[trigram])
        bigram_count =  int(self.ngram_model[bigram])
        return trigram_count / bigram_count


    def read_file(self, filename):
        try:
            file = open(filename, "r")
            return file
        except:
            print("File not found")
            return

    def build_ngram_model(self):
        lines = self.read_file(self.model_filename).readlines()

        for line in lines:
            line = re.sub(r'\n', '', line)
            line = line.split('\t')
            key = line[0]
            val = line[1]

            if not (re.search(r'\s+', key)):
                self.words_count += int(val)

            self.ngram_model[key] = val

    def get_ngram_model(self):
        return self.ngram_model

    def get_sentences(self):
        return self.sentences

class TestTestModel:
    def __init__(self):
        sentence_filename = "text/sample3_sentences.txt"
        model_filename = "text/sample3.txt.model"
        self.tm = TestModel(sentence_filename, model_filename)

    def run_all_tests(self):
        print("=============================")
        print("Running tests")
        self.test_compute_prob_sentences()

        print("End")
        print("=============================")

    def test_compute_prob_sentences(self):
        print("Test prob of a sentence")
        result = self.tm.compute_prob_sentences()[0] == 0.12
        print("  it should equal 0.12:", result)

######################
# Testing
# t = TestTestModel()
# t.run_all_tests()

# sentence_filename = "sample3_sentences.txt"
# model_filename = "sample3.txt.model"

# tm = TestModel(model_filename, sentence_filename)
# probs = tm.compute_prob_sentences()
# print(probs)


######################
# Production
if __name__ == "__main__":
    sentences_filename = sys.argv[2]
    model_filename = sys.argv[1]

    tm = TestModel(model_filename, sentences_filename)
    probs = tm.compute_prob_sentences()

    sentences = tm.get_sentences()
    for sentence in sentences:
        print("Prob of sentence:", probs[sentences.index(sentence)])


