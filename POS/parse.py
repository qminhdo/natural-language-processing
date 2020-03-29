#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
""" Tagging Assigment

Trained sentences count: 3742
Tested sentencess count: 470
Correct tagged non-terminal: 8456
Incorrect tagged non-terminal: 2594
Percentage of correctly classified non-terminal: 0.77%

"""
__author__ = "Quang Minh Do"

import re, sys
from collections import Counter


class Parse:
    def __init__(self, dicts, test_file):
        self.dicts = dicts
        self.test_txt = self.format_txt(self.read_file(test_file).lower())
        self.correct_count = 0
        self.incorrect_count = 0

        sentences = self.test_txt.split('./.')
        sentences.pop() # remove last sentence, it is empty

        # get ALL tags sequence
        self.get_all_tag_sequence(sentences)

        print("--------- REPORT ---------")
        print("Trained sentences count:", len(self.dicts.non_terminals_sentences))
        print("Tested sentencess count:", len(sentences))
        print("Correct tagged non-terminal:", self.correct_count)
        print("Incorrect tagged non-terminal:", self.incorrect_count)
        print("Percentage of correctly classified non-terminal:", str(round(self.correct_count / (self.incorrect_count + self.correct_count),2 )) + "%")

    def get_all_tag_sequence(self, sentences):
        for sentence in sentences:
            sentence = sentence.strip()
            f_sentence = self.remove_unknown_words(sentence)

            # get tag sequence
            tagged_sequence = self.get_tag_sequence(f_sentence)
            print("---Tag sequence:", ' '.join(tagged_sequence)[0:50] + ' ...')

            # compare tag with original sentence in test file, report incorrect and correct ones
            # get differences after filtering out unknown words
            self.incorrect_count += len(sentence.split(' ')) - len(f_sentence.split(' '))
            self.compare_tag_sequence(f_sentence,tagged_sequence)

    def format_txt(self,txt):
        txt = re.sub(r'[\t]', '', txt)
        txt = re.sub(r'[\n]', ' ', txt)
        txt = re.sub(r'[\s]{2,}', '', txt)
        return txt

    def get_tag_sequence(self, sentence):
        words = []
        # filter out the tag to pass into Tagging
        for word in sentence.split(' '):
            word = re.sub(r'/.*', '', word)
            words.append(word)

        f_sentence = ' '.join(words)
        print("Tagging sentence:", f_sentence[0:50] + " ...")

        tagging = Tagging(self.dicts, f_sentence)
        return tagging.tag_sequence

    def compare_tag_sequence(self, original_sentence, tagged_sentence):
        original_sentence_words = original_sentence.split(' ')
        tagged_sentence_words = tagged_sentence

        words = []
        # filter out the tag
        for word in original_sentence_words:
            word = re.sub(r'.*/', '', word)
            words.append(word)

        original_sentence_words = words

        for i in range(len(original_sentence_words)):
            if (original_sentence_words[i] == tagged_sentence_words[i]):
                self.correct_count += 1
            else:
                self.incorrect_count +=1

    def remove_unknown_words(self, sentence):
        words = []
        for w in sentence.split(' '):
            word = re.sub(r'/.*', '', w)  # filter out the tag
            # filter out unknown word
            add = False
            for t in self.dicts.non_terminals:
                if ((word + "/" + t) in self.dicts.emissions_dict.keys()):
                    add = True
                    break
            if add:
                words.append(w)

        return ' '.join(words)  # sentence without unknown word and tags

    def read_file(self, filename):
        try:
            file = open(filename, "r")
            return file.read()
        except:
            print("File not found")
            return


class Tagging:
    def __init__(self, dicts, sentence):
        self.dicts = dicts
        self.orginial_sentence = sentence
        self.sentence = sentence.lower()
        self.tag_sequence = []
        self.viterbiMatrix = {'0**': 1}  # init viterbi result
        self.bpMatrix = {}
        self.bpResult = {}

        self.compute_pi()

    # get all possible tags for the sentence
    def get_tags(self, words):
        tags = []

        for key,value in self.dicts.emissions_dict.items():
            k = re.sub(r'/.*', '', key)
            t = re.sub(r'.*/', '', key)

            for word in words:
                if k == word:
                    tags.append(t)

        return list(set(tags))

    def compute_pi(self):
        words = self.sentence.split(' ')
        n = len(words)

        tags = self.get_tags(words)

        # offset words element index by 1, k starting index is 1 not at 0
        words.reverse()
        words.append('')
        words.reverse()

        s = {-1: '*', 0: '*'}  # s[-1] = s[0] = '*'
        # s.update({1: tags})
        # s.update({2: 'STOP'})
        for i in range(1, len(words)):  # sk = S for k belongs {1..n}
            s.update({i: tags})
        s.update({len(s) - 1: 'STOP'})  # s(n+1) = {STOP}

        mlh = MaximumLikelihood(self.dicts)

        # tag sequence
        y = [""] * (n + 1)

        # loop over words
        for k in range(1, n + 1):
            for u in s.get(k-1):
                for v in s.get(k):
                    results = []
                    highest = -1

                    for w in s.get(k - 2):
                        pi = self.viterbiMatrix[str(k - 1) + w + u]
                        if (pi == 0 or pi == 0.0):
                            tmp = 0
                        else:
                            e = self.compute_emission(words[k], v)
                            if (e == 0 or e == 0.0):
                                tmp = 0
                            else:
                                qml = mlh.qml_with_interpolation(v, w, u)
                                tmp = pi * qml * e

                        results.append(tmp)

                        if tmp > highest:
                            highest = tmp
                            self.bpMatrix.update({str(k) + u + v: w})

                    self.viterbiMatrix.update({str(k) + u + v: max(results)})

        # compute tag sequence
        highest = -1
        for u in s.get(1):
            for v in s.get(1):
                tm = (self.viterbiMatrix.get(str(n) + u + v))
                if not (str(n) + u + v) in self.viterbiMatrix.keys():
                    tm = 0

                tmp_result = tm * mlh.qml_with_interpolation("STOP", str(u), str(v))
                if (tmp_result > highest):
                    highest = tmp_result
                    y[n-1] = u
                    y[n] = v

        k = n - 2
        while(k > 0):
            y[k] = self.bpMatrix.get(str(k+2) + y[k+1] + y[k+2])
            k -= 1

        y.reverse()
        y.pop()
        y.reverse()

        self.tag_sequence = y

    # compute emission probability estimation
    def compute_emission(self, word, tag):
        if not (tag in self.dicts.singleNT_dict.keys()):
            return 0
        else:
            return self.dicts.emissions_dict[word + '/' + tag] / self.dicts.singleNT_dict[tag]


class MaximumLikelihood:
    def __init__(self, dicts, sentence = ""):
        self.dicts = dicts
        self.sentence = sentence

    def prob_of_sentence(self):
        pass

    # can be use as standalone to compute qml(wi | wi-2, wi - 1)
    # default for lambdas are defined, can be changed as needed
    def qml_with_interpolation(self, wi, wi2, wi1, lambda1=0.9, lambda2=0.09, lambda3=0.01):
        # print("wi:", wi)
        # print("wi - 1:", wi1)
        # print("wi - 2:", wi2)
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
        if not (wi in self.dicts.singleNT_dict.keys()):
            return 0

        return int(self.dicts.singleNT_dict[wi]) / self.dicts.words_count

    def qml2(self, wi, wi1):
        # compute maximum likelihood estimate
        # check if words exist in the ngram model
        # q(wi | wi-1) = Count(wi-1, wi) / Count(wi-1)
        bigram = wi1 + " " + wi

        if not (bigram in self.dicts.twoNT_dict.keys()) \
                or not (wi1 in self.dicts.singleNT_dict.keys()):
            return 0

        bigram_count = int(self.dicts.twoNT_dict[bigram])
        return bigram_count / int(self.dicts.singleNT_dict[wi1])

    def qml(self, wi, wi2, wi1):
        # compute maximum likelihood estimate
        # check if words exist in the ngram model
        # q(wi | wi-2, wi-1) = Count(wi-2, wi-1, wi) / Count(wi-2, wi-1)
        trigram = wi2 + " " + wi1 + " " + wi
        bigram = wi2 + " " + wi1

        if not (trigram in self.dicts.threeNT_dict.keys()) \
                or not (bigram in self.dicts.twoNT_dict.keys()):
            return 0

        trigram_count = int(self.dicts.threeNT_dict[trigram])
        bigram_count = int(self.dicts.twoNT_dict[bigram])

        return trigram_count / bigram_count


class TrainDict:
    def __init__(self, training_file):
        self.training_txt = self.read_file(training_file).lower()

        self.words_count = 0
        self.emissions_dict = Counter()  # Emission count dictionary
        self.singleNT_dict = Counter()  # single non-terminal count dict  Counter({'nn': 11735, 'in': 9343, ... })
        self.twoNT_dict = Counter()  # two non-terminal count dict Counter({'* *': 3744, 'at nn': 3594, ... })
        self.threeNT_dict = Counter()  # three non-terminal count dict Counter({'in at nn': 1506, ...})

        self.non_terminals = {}  # ['at', 'np-tl', 'nn-tl', ... ]
        self.non_terminals_txt = ''   # "at np-tl nn-tl jj-tl nn-tl ..."
        self.non_terminals_sentences = []  # ["* * at np-tl nn-tl STOP", ...]

        self.build_all_dict()

    def build_all_dict(self):
        self.build_non_terminals()
        self.build_emissions_dict()
        self.build_singleNT_dict()
        self.build_twoNT_dict()
        self.build_threeNT_dict()

    def build_non_terminals(self):
        r = re.compile(r'(?<=/)[^\s]*')
        self.non_terminals = r.findall(self.training_txt)
        self.words_count = len(self.non_terminals)  # Add words to total words count, including "."

        self.non_terminals_txt = ' '.join(self.non_terminals)
        self.non_terminals_txt = re.sub(r'[\n\t]', '', self.non_terminals_txt)

        self.non_terminals = set(self.non_terminals)

        tmp_sentences = self.non_terminals_txt.split('.')
        new_sentences = []

        for sentence in tmp_sentences:
            sentence = sentence.strip()
            if not (len(sentence) == 0):
                new_sentences.append("* * " + sentence + " STOP")  # Add START and STOP symbols to each sentence

        self.non_terminals_sentences = new_sentences

    def build_emissions_dict(self):
        self.training_txt = re.sub(r'[\t]', '', self.training_txt)
        self.training_txt = re.sub(r'[\n]', ' ', self.training_txt)
        self.training_txt = re.sub(r'[\s]{1,}', ' ', self.training_txt)
        entries = self.training_txt.split(' ')
        entries.pop()
        self.emissions_dict = Counter(entries)


    def build_singleNT_dict(self):
        for sentence in self.non_terminals_sentences:
            aux = Counter(self.ngrams(sentence, 1))
            self.singleNT_dict.update(aux)

        aux = Counter({'.': self.singleNT_dict.get('STOP')})
        self.singleNT_dict.update(aux)

    def build_twoNT_dict(self):
        for sentence in self.non_terminals_sentences:
            aux = Counter(self.ngrams(sentence, 2))
            self.twoNT_dict.update(aux)

    def build_threeNT_dict(self):
        for sentence in self.non_terminals_sentences:
            aux = Counter(self.ngrams(sentence, 3))
            self.threeNT_dict.update(aux)

    def ngrams(self, text, n):
        words = text.split(' ')

        return (
            [' '.join(words[i:i + n]) for i in range(len(words) - n + 1)]
        )

    def read_file(self, filename):
        try:
            file = open(filename, "r")
            return file.read()
        except:
            print("File not found")
            return


#####################
# Test
class TestTrainDict:
    def __init__(self, training_file):
        self.dicts = TrainDict(training_file)

    def test_build_all_dict(self):
        print("Test build_all_dict()")
        print("It should have build correct dicts:")

        # print("emissions:", self.dicts.emissions_dict)
        # print("singleNT:", self.dicts.singleNT_dict)
        # print("twoNT:", self.dicts.twoNT_dict)
        # print("threeNT:", self.dicts.threeNT_dict)
        # print("words_count:", self.dicts.words_count)

        print("  emissions:", self.dicts.emissions_dict["the/at"] == 5254)
        print("  singleNT:", self.dicts.singleNT_dict["nn"] == 11735)
        print("  twoNT:", self.dicts.twoNT_dict["* *"] == 3744)
        print("  threeNT:", self.dicts.threeNT_dict["in at nn"] == 1506)
        print("  words_count:", self.dicts.words_count == 88995)

    def test_all(self):
        print("============ ============")
        print("Test TrainDict")
        self.test_build_all_dict()
        print("============")


class TestMaximumLikeliHood:
    def __init__(self):
        training_file = "sample_qml.txt"
        self.dicts = TrainDict(training_file)
        self.sentence = "foo"
        self.mlh = MaximumLikelihood(self.dicts, self.sentence)

    def test_qml_with_interpolation(self):
        print("Test qml_with_interpolation()")
        result = self.mlh.qml_with_interpolation('book', 'the', 'green', 1 / 3, 1 / 3, 1 / 3)
        result = result == 0.5714285714285714
        print("  it should equal 0.5714285714285714:", result)

    def test_all(self):
        print("============ ============")
        print("Test MaximumLikeliHood")
        self.test_qml_with_interpolation()
        print("============")


class TestTagging:
    def __init__(self, training_file):
        self.dicts = TrainDict(training_file)
        # self.tagging = Tagging(self.dicts, "A few weeks")
        # self.tagging = Tagging(self.dicts, "The biggest single act")
        self.tagging = Tagging(self.dicts, "The biggest single act")
        # print(self.tagging.tag_sequence)

    def test_compute_pi(self):
        print("Test comput_pi()")

        pass

    def test_all(self):
        print("============ ============")
        print("Test Tagging")
        self.test_compute_pi()
        print("============")


class TestParse:
    def __init__(self, training_file, test_file):
        self.dicts = TrainDict(training_file)
        self.p = Parse(self.dicts, test_file)

    def test_compute_pi(self):
        pass

    def test_all(self):
        print("============ ============")
        print("Test Parse")
        # self.test_compute_pi()
        print("============")

training_file = 'ca_train.txt'
test_file = 'ca_test.txt'
# test1 = TestTrainDict(training_file)
# test2 = TestMaximumLikeliHood()
# test3 = TestTagging(training_file)
# test4 = TestParse(training_file, test_file)

# test1.test_all()
# test2.test_all()
# test3.test_all()
# test4.test_all()
######################
# Production

training_file = sys.argv[1]
test_file = sys.argv[2]
dicts = TrainDict(training_file)
parse = Parse(dicts, test_file)


