from collections import defaultdict
from gensim import corpora

documents = [
    "Human machine interface for lab abc computer applications",
    "A survey of user opinion of computer system response time",
    "The EPS user interface management system",
    "System and human system engineering testing of EPS",
    "Relation of user perceived response time to error measurement",
    "The generation of random binary unordered trees",
    "The intersection graph of paths in trees",
    "Graph minors IV Widths of trees and well quasi ordering",
    "Graph minors A survey",
]

# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [
    [word for word in document.lower().split() if word not in stoplist]
    for document in documents
]

# remove words that appear only once
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [
    [token for token in text if frequency[token] > 1]
    for text in texts
]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]





def _word2vec():
    sample = open("data/sample.txt", "r")
    s = sample.read()
    f = s.replace("\n", " ")
    data = []

    for i in tokenize.sent_tokenize(f):
        temp = []

        for j in tokenize.word_tokenize(i):
            temp.append(j.lower())

        data.append(temp)

    model1 = Word2Vec(data, min_count=1, size=100, window=5)
    # Print results
    print("Cosine similarity between 'alice' " +
          "and 'wonderland' - CBOW : ",
          model1.wv.similarity('alice', 'wonderland'))

    print("Cosine similarity between 'alice' " +
          "and 'machines' - CBOW : ",
          model1.wv.similarity('alice', 'machines'))
