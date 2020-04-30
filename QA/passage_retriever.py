import re, os
import nltk
from nltk import tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from question_classifier import QuestionClassifier

lemmatizer = WordNetLemmatizer()

stop_words = ["the", "a", "an"]
stop_words = [".", "?", "!"]
q_words = ["who", "what", "where", "when" "why",
           "whose", "which", "whom", "how", "do", "does",
           "is", "are", "should", "could", "will", "can", "could"]
quantifiers = ["few", "little", "much", "many"]
irrelevant_loc_words = ["north", "east", "west", "south", "top", "bottom", "up", "down"]


class PassageRetriever:
    """
    Return candidate passages along with their score
    This can then be passed to Answer processor where the answer will finilaize

    Steps:
    - Formulate possible answer phrase (AP) to perform similarity (done)

    - Loop through each documents:
    - If document contains the queries:
        - Build the passages matrix, also add the AP to the beginning of matrix
        - Find similarity of AP or matrix[0] to rest of passages in matrix
        - Pick all passages with score of 0.7 or more pick 10 if less than 0.7
        - Using heuristic, modifiy the score
        - Return passages with their score

    Experiment heuristics:
    # heuristic 3
    # ensure that sentence makes sense by having proper Clauses
    # grammar = r
    #   NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
    #   PP: {<IN><NP>}               # Chunk prepositions followed by NP
    #   VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
    #   CLAUSE: {<NP><VP>}           # Chunk NP, VP
    #
    # cp = RegexpParser(grammar, loop=2)
    # cp.parse(passage_cleaned)

    # heuristic 4
    # score for passage that does not contain question words
    """

    def __init__(self, q_classifier, queries):
        self.dirname = "data/assorted/"
        self.q_classifer = q_classifier
        self.queries = queries
        self.docs_passages = []

        self.answer_phrase = self.build_answer_phrase()
        self.candidate_passages = self.find_candidate_passages()

    def build_answer_phrase(self):
        """
        The Answer Phrase (AP) doesn't have to be in exact order
        because TFIDF use tokens to make comparision
        AP consists the matched groups when performing answer type extraction
        E.g if answer type is TREATMENT, we add "treatment for" to bag of word to
        increase chance of getting similar phrase

        :return: the answer phrase (bag of words)
        """

        matches = ""

        for group_ in self.q_classifer.matched_groups:
            content = self.q_classifer.matched_groups.get(group_)
            if content != None:
                matches += content + " "

        if (self.q_classifer.a_type == "DEFINITION"):
            phrase = "{}".format(matches)

        elif self.q_classifer.a_type == "SYMPTOM":
            phrase = "common symptom sign issues include : {}".format(matches)

        elif self.q_classifer.a_type == "TREATMENT":
            phrase = "treatment cure care heal medicine include : {}".format(matches)

        elif self.q_classifer.a_type == "CAUSES":
            phrase = "main causes form types include factor trigger : {}".format(matches)

        elif self.q_classifer.a_type == "FREQUENCY":
            phrase = "time day twice daily {}".format(matches)

        elif self.q_classifer.a_type == "LOCATION":
            phrase = "{}".format(matches)

        elif self.q_classifer.a_type == "TIME":
            phrase = "often {}".format(matches)

        elif self.q_classifer.a_type == "DESCRIPTION":
            phrase = "{}".format(matches)

        elif self.q_classifer.a_type == "PERSON":
            phrase = "contact approach visit doctor nurse{}".format(matches)

        elif self.q_classifer.a_type == "BINARY":
            phrase = "{}".format(matches)
        else:
            # OTHER type
            phrase = "{}".format(matches)

        final_phrase = []
        # remove stop words from phrase
        for w in word_tokenize(phrase):
            if w not in nltk.corpus.stopwords.words('english'):
                final_phrase.append(w)
        return ' '.join(final_phrase)

    def find_candidate_docs(self):
        """
        Find filename that match the queries to reduce time
        :return:
        """
        filenames_ = []
        for dirname, dirnames, filenames in os.walk(self.dirname):
            for filename in filenames:
                pattern = "({})".format('|'.join(self.queries))
                r = re.compile(pattern, re.IGNORECASE)
                match = r.search(filename, re.IGNORECASE)
                if match:
                    filenames_.append(filename)

        return filenames_

    def find_candidate_passages(self):
        """Loop through all available documents
        Find docs that match the queries
        Find all passages
        Find score of those passages

        :return list: passages and scores
        """
        candidate_passages = {}

        passages = []
        passages.append(self.answer_phrase)

        candidate_docs = self.find_candidate_docs()
        if len(candidate_docs) > 0:
            passages.extend(self.find_all_passages(candidate_docs))
        else:
            # Loop through all documents
            # Get all passages that are relevant so we can build TFIDF matrix
            for dirname, dirnames, filenames in os.walk(self.dirname):
                passages.extend(self.find_all_passages(filenames))


        # Find passages and their scores
        matrix = self.build_matrix(passages)
        passages_scores = self.find_passages_scores(passages, matrix)
        candidate_passages.update(passages_scores)
        return candidate_passages

    def find_all_passages(self, filename):
        queries_pattern = '(' + '|'.join(self.queries) + ')+'
        passages = []
        for filename in filename:
            with open(os.path.join(self.dirname, filename), 'r', encoding='utf8') as f:
                text = f.read()
                # check whether document contains that queries
                match = re.search(queries_pattern, text, re.IGNORECASE)

                # Document is relating to the question
                if match:
                    # Find candidate passages
                    passages.extend(tokenize.sent_tokenize(text))
        return passages

    def find_passages_scores(self, passages, matrix):
        """Find score of similarity all passages with the AP
        Additional heuristics:
        - check if sent begin if query is|are

        :param passages: contain the AP at index 0 and raw passages
        :param matrix: the TFIDF matrix of AP and raw passages
        :return passages_scores: the passages and the scores
        """

        passages_scores = {}
        for k, raw_passage in enumerate(passages[1:], start=1):
            total_score = 0
            passage_cleaned = self.clean_passage(raw_passage)

            # Do not use passages that are question

            is_question = self.check_if_question(passage_cleaned)
            if is_question:
                continue
            else:
                similarity_score = cosine_similarity(matrix[0], matrix[k])

                if (similarity_score > 0.01):
                    h1 = self.cal_h1(passage_cleaned)
                    h2 = self.cal_h2(passage_cleaned)

                    total_score = (similarity_score * 0.3) + (h1 * 0.5) + (h2 * 0.2)
                    passages_scores.update({passage_cleaned: total_score})
        return passages_scores

    def cal_h2(self, passage):
        """
        Score more point if passage contain the focus words
        score = 1 if contain all queries
        score = varies
        score = 0 if not
        :return: score
        """
        focus_words = self.q_classifer.matched_groups.get('focus').split()
        match_counter = 0
        for kw in focus_words:
            r = re.compile('({})'.format(kw), re.IGNORECASE)
            match = r.search(passage)
            match_counter += 1 if match else 0

        return match_counter / len(focus_words)

    def cal_h1(self, passage):
        """
        Heuristic 1: has aux keywords
        :return: score
        """
        pattern = '.*{}.*'.format(self.h1_pattern())
        r = re.compile(pattern, re.IGNORECASE)
        match = r.search(passage)
        return 1 if (match) else 0

    def h1_pattern(self):
        if (self.q_classifer.a_type == "DEFINITION"):
            focus = self.q_classifer.matched_groups.get('focus')
            verb = self.q_classifer.matched_groups.get('verb')
            pattern = '(' + focus + ').{1,20}(' + verb + ')'

        elif self.q_classifer.a_type == "SYMPTOM":
            focus = self.q_classifer.matched_groups.get('focus')
            pattern = '(symptom[s]?|sign[s]?|issue[s]?)+.*:.*'

        elif self.q_classifer.a_type == "TREATMENT":
            focus = self.q_classifer.matched_groups.get('focus')
            pattern = '(treatment[s]?|prevention|drug|medication[s]?|medicine)+.*:.*'

        elif self.q_classifer.a_type == "CAUSES":
            pattern = "(cause[s]?|type[s]?|factor[s]?|trigger).*:?.*"

        elif self.q_classifer.a_type == "FREQUENCY":
            pattern = "(time[s]?|twice|once|daily)"

        elif self.q_classifer.a_type == "TIME":
            pattern = ""

        elif self.q_classifer.a_type == "LOCATION":
            pattern = "(location|locate)"

        elif self.q_classifer.a_type == "DESCRIPTION":
            pattern = "(guide|guidance)"

        elif self.q_classifer.a_type == "PERSON":
            pattern = "(contact|meet|doctor[s]?|nurse[s]?|ask[s]?|call)"

        elif self.q_classifer.a_type == "BINARY":
            pattern = ""
        else:
            # a_type = "OTHER
            pattern = ""
        return pattern

    def check_if_question(self, passage):
        """
        convert passage into tokens
        check if contain any question words
        return True if is

        :return: boolean
        """
        q_words = ["who", "what", "where", "when" "why",
                   "whose", "which", "whom", "how", "do", "does", "?"]

        tokens = word_tokenize(passage)
        for token in tokens:
            if token in q_words:
                return True

        return False

    def clean_passage(self, raw_passage):
        stop_words = ["."]
        raw_passage = re.sub("\n", " ", raw_passage.lower())

        tokens = [token for i, token in enumerate(word_tokenize(raw_passage.lower()))
                  if token not in stop_words]
        return ' '.join(tokens)

    def build_matrix(self, passages):
        # Use TFIDF
        # the AP will be the first index
        tfidf_vectorizer = TfidfVectorizer()
        matrix = tfidf_vectorizer.fit_transform(passages)

        return matrix


if __name__ == "__main__":
    """
    For testing purpose
    This file can be running alone
    Run this file to see details as described below
    """
    from query_formulator import QueryFormulator

    questions = [
        # "How many times do I have to take aspirin in a day?",
        "What causes acne?"
        # Where does acne occur most?

    ]

    for q_ in questions:
        print("======================")
        q_classifier = QuestionClassifier(q_)
        queries = QueryFormulator(q_classifier).queries
        d = PassageRetriever(q_classifier, queries)
        print(d.candidate_passages)
