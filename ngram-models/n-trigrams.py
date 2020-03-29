#!/usr/bin/env python3
""" ngram model homework """
__author__ = "Quang Minh Do"

import sys, re
from collections import defaultdict
from collections import Counter

# python n-trigrams.py <input-file> <model-file>
"""
Given a sentence “I am Sam. Sam I am”
The <model> should look like this:
I 2
am 2
Sam 2
STOP 2
I am 2
am Sam 1
Sam I 1
Sam STOP 1
* Sam 1
* I 1
am STOP 1
* * I 1
* I am 1
I am Sam 1
am Sam STOP 1
* * Sam 1
* Sam I 1
Sam I am 1
I am STOP 1
"""


class NTrigram:
    def __init__(self, input_filename, model_filename):
        self.filename = input_filename
        self.model_filename = model_filename
        self.text = self.read_file().read()
        self.model = {}
        self.build_ngram_model()

    def remove_special_characters(self, text):
        text = text.strip()
        text = re.sub(r'[^A-Za-z0-9.]', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        return text

    def build_ngram_model(self):
        sentences = self.build_sentences(self.text)

        u_gram_list = self.build_ngram(sentences, 4, 1)
        bi_gram_list = self.build_ngram(sentences, 2, 2)
        tri_gram_list = self.build_ngram(sentences, 0, 3)

        tmp_model = u_gram_list + bi_gram_list + tri_gram_list
        self.set_model(tmp_model)

    def build_sentences(self, text):
        text = self.remove_special_characters(text)
        sentences = text.split('.')

        # we don't need the empty sentence after last period from self.text
        if(len(sentences[-1]) == 0):
            sentences.pop()

        for k, v in enumerate(sentences):
            v = v.strip()
            v = "* * " + v + " STOP"
            sentences[k] = v

        return sentences

    def build_ngram(self, sentences, start, n):
        list = [self.ngrams(sentence[start:], n) for sentence in sentences]
        tpm_list = []
        for i in list:
            for j in i:
                tpm_list.append(j)

        return tpm_list

    def ngrams(self, text, n):
        words = text.split(' ')
        return (
            [' '.join(words[i:i + n]) for i in range(len(words) - n + 1)]
        )

    def read_file(self):
        try:
            file = open(self.filename, "r")
            return file
        except:
            print("File not found")
            return

    def save_model_to_file(self):
        output_filename = self.model_filename
        fdata = self.format_data(self.model)

        file = open(output_filename, 'w')
        file.write(fdata)
        file.close()

    def format_data(self, data):
        fdata = ""
        for key, val in data.items():
            fdata += "{}\t{}\n".format(key, val)

        return fdata

    def get_model(self):
        return self.model

    def set_model(self, model):
        self.model = Counter(model)



######################
# Production
if __name__ == "__main__":
    input_filename = sys.argv[1]
    model_filename = sys.argv[2]
    ntrigram = NTrigram(input_filename, model_filename)
    ntrigram.save_model_to_file()
