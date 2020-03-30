#!/usr/bin/env python3
""" ngram model homework """
__author__ = "Quang Minh Do"

import sys, re

class STestModel:
    def __init__(self, model_filename, sentences_filename):
        self.sentences_filename = sentences_filename
        self.model_filename = model_filename

        self.sentences = self.read_file(self.sentences_filename).read()
        self.sentences = self.remove_special_characters(self.sentences)
        self.sentences = self.sentences.split(".")

        for sentence in self.sentences:
            if(len(sentence) == 0):
                self.sentences.pop(self.sentences.index(sentence))

        self.words_count = 0
        self.ngram_model = {}
        self.build_ngram_model()

    def remove_special_characters(self, text):
        text = text.strip()
        text = re.sub(r'[^A-Za-z0-9.]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.lower()
        return text

    def compute_prob_sentences(self):
        probs = []
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

                tmp = self.prob_with_interpolation(word, previous_2_word, previous_word)
                prob *= tmp

            probs.append(prob)

        return probs


    def prob_with_interpolation(self, wi, wi2, wi1, lambda1 = 0.9, lambda2 = 0.09, lambda3 = 0.01):
        l1 = lambda1 * self.qml(wi, wi2, wi1)
        l2 = lambda2 * self.qml2(wi, wi1)
        l3 = lambda3 * self.qml3(wi)

        if (wi == "STOP") and l1 == 0 and l2 == 0:
            return 0
        else:
            return l1 + l2 + l3

    def qml3(self, wi):
        # compute maximum likelihood estimate
        # check if words exist in the ngram model
        # q(wi | wi) = Count(wi) / Count(wi-1)
        if not (wi in self.ngram_model.keys()):
            return 0

        return int(self.ngram_model[wi]) / self.words_count


    def qml2(self, wi, wi1):
        # compute maximum likelihood estimate
        # check if words exist in the ngram model
        # q(wi | wi-1) = Count(wi-1, wi) / Count(wi-1)
        bigram = wi1 + " " + wi

        if (bigram == "* *"):
            bigram = "STOP"

        if not (bigram in self.ngram_model.keys()) \
                or not (wi1 in self.ngram_model.keys()):
            return 0

        bigram_count = int(self.ngram_model[bigram])
        return bigram_count / int(self.ngram_model[wi1])


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

            # update words count for this corpus
            if not (re.search(r'\s+', key)):
                self.words_count += int(val)

            self.ngram_model[key] = val

    def get_ngram_model(self):
        return self.ngram_model

    def get_sentences(self):
        return self.sentences

class TestSTestModel:
    def __init__(self):
        sentence_filename = "text/sample_quiz_sentences.txt"
        model_filename = "text/sample_quiz.txt.model"
        self.tm = STestModel(model_filename, sentence_filename)

    def run_all_tests(self):
        print("=============================")
        print("Running tests")
        self.test_prob_with_interpolation()
        self.test_prob_with_interpolation2()
        self.test_prob_with_interpolation_with_spanish_text()
        print("End")
        print("=============================")

    def test_prob_with_interpolation(self):
        print("Test qml(wi, wi2, wi1) with interpolation")
        result = self.tm.prob_with_interpolation('book', 'the', 'green', 1/3,1/3,1/3) == 0.5714285714285714
        print("  it should equal 0.5714285714285714:", result)

    def test_prob_with_interpolation2(self):
        print("Test qml(wi, wi2, wi1) with spanish text")
        result = self.tm.prob_with_interpolation('hola', 'lalo', 'yes')
        print("  it should equal 0.0:", result)

    def test_prob_with_interpolation_with_spanish_text(self):
        sentence_filename = "text/Don Quijote.txt"
        model_filename = "text/Othello.model"
        tm = STestModel(model_filename, sentence_filename)

        print("test_ compute_prob_sentences() with spanish_sentences.txt")
        result = tm.compute_prob_sentences()
        print("  it should equal 0:", result[0])


######################
# Test

# t = TestSTestModel()
# t.run_all_tests()

######################
# Production
# if __name__ == "__main__":
#     sentences_filename = sys.argv[2]
#     model_filename = sys.argv[1]
#
#     tm = STestModel(model_filename, sentences_filename)
#     probs = tm.compute_prob_sentences()
#
#     sentences = tm.get_sentences()
#     for sentence in sentences:
#         print(sentence, ":", probs[sentences.index(sentence)])