from nltk import tokenize
import warnings
import spacy

"""
Classify a question
Find out the coarse and fine class of a question
"""
nlp = spacy.load("en_core_web_md")

ENTY_dismed = open("../data/cogcomp/train_set/dismed.txt").read()
DES_def =  open("../data/cogcomp/train_set/def.txt").read()
LOC_city = open("../data/cogcomp/train_set/LOCATION_city.txt").read()

docs = {"ENTY:dismed": ENTY_dismed, "DES:def": DES_def, "LOC:city": LOC_city}
labels = {}

for k,v in enumerate(docs):
    labels.update({k: nlp(v.lower())})

answer_query = "What is fever?".lower()
question = nlp(answer_query)

result = []
for k, label in enumerate(labels):
    print(label.similarity(question))

# nlp_latin = spacy.load("/tmp/la_vectors_wiki_lg")
# doc1 = nlp_latin("Caecilius est in horto")
# doc2 = nlp_latin("servus est in atrio")
# doc1.similarity(doc2)