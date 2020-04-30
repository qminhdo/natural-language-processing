from nltk import tokenize
import os
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

lemmatizer = WordNetLemmatizer()

stop_words = ["the", "a", "an"]
q_words = ["who", "what", "where", "when" "why",
           "whose", "which", "whom", "how", "do", "does",
           "is", "are", "should", "could", "will", "can", "could"]
quantifiers = ["few", "little", "much", "many"]
irrelevant_loc_words = ["north", "east", "west", "south", "top", "bottom", "up", "down"]

"""

"""


class PassageRetriever:
    def __init__(self, question, docs, q_type, a_type):
        self.question = question
        self.docs = docs
        self.q_type = q_type
        self.a_type = a_type
        self.dirname = "data/assorted"

    def get_candidate_passages(self):
        candiates_passages = []

        for doc in self.docs:
            passage = []
            doc = open(os.path.join(dirname, doc), "r").read()
            sents = tokenize.sent_tokenize(doc)

            for k, v in enumerate(sents):
                tokens = [lemmatizer.lemmatize(token) for i, token in enumerate(word_tokenize(v))
                          if token not in stop_words]
                tagged = pos_tag(tokens)

                # Loop for passage that has words with similar meaning
                print("+++++++++++++")
                print(word_tokenize(v))

                passage.append(v)

            candiates_passages.append(passage)

        return candiates_passages


if __name__ == "__main__":
    docs = ['drug_1.txt', 'drug_2.txt']
    dirname = "data/assorted"
    q_type = "ENTITY:desmed"
    a_type = "DEFINITION"

    question = "Does aspirin treat cancer?"
    tokens = ["Does", "aspirin", "treat", "cancer"]

    p = PassageRetriever(question, docs, q_type, a_type)
    passages = p.get_candidate_passages()
    # print(passages)
