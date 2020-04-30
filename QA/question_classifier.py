import re
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

lemmatizer = WordNetLemmatizer()

stop_words = ["the", "a", "an"]
q_words = ["who", "what", "where", "when" "why",
           "whose", "which", "whom", "how", "do", "does",
           "is", "are", "should", "could", "will", "can", "could"]

# naive_a_type_reg = {
#     "PERSON": r'^(who)',
#     "DATE": r'^(when)',
#     "NOUN": r'^(what)',
#     "PHRASE": r'(why|wow)',
#     "NUMERIC": r'^(how (many|much))',
#     "REASON": r'^(how (can|could|should)',
#     "BINARY": r'^(do|does|did|are|is|was|were|have|has|can|will|should|could)',
#     "STATEMENT": r'^(my|his|her|their|our|its)'
# }

class QuestionClassifier:
    """
    Parse one question at a time

    The job of a question classifier is to have information available for:
        - the question type/class
        - the answer type, and the match group such as FOCUS, OTHER, VERB, PRONOUN
        - the question tokens, tagged
        - cleaned question

    All COARSE class:
        * ABBR
        * DESC
        * ENTY
        * HUM
        * LOC
        * NUM

    SOME FINE class samples:
        * ENTY:dismed
        * ENTY:body
        * DES:def
        * DES:desc
        * DES:reason
        * ...
    For this QA system, we focus on dismed only
    So it is assumed that user will only ask dismed question only
    """

    def __init__(self, q):
        """
        Return samples:
            Raw Tokens: ['what', 'cause', 'fever']
            Filtered and Lemmatized tokens:  ['what', 'cause', 'fever']
            Tagged: [('what', 'WP'), ('cause', 'NN'), ('fever', 'NN')]
            Entities: (S what/WP cause/NN fever/NN)
            Question type: ENTY:dismed
            Question word:  ['what']
            Answer type: CAUSES
            Focus word: fever

        :param q: the raw question
        """
        self.q_raw = q
        self.q_cleaned = ""
        self.q_tagged = []
        self.tokens_raw = []
        self.tokens = []
        self.ner = ""
        self.q_keywords = []
        self.q_word = ""
        self.focus = ""
        self.matched_groups = []

        self.pre_process_question()
        self.q_type = self.find_q_type()
        self.a_type = self.find_a_type()

    def pre_process_question(self):
        self.tokens_raw = word_tokenize(self.remove_alien_char(self.q_raw.lower()))
        self.tokens = [lemmatizer.lemmatize(token) for i, token in enumerate(self.tokens_raw)
                       if token not in stop_words]
        self.q_cleaned = ' '.join(self.tokens)
        self.q_tagged = pos_tag(self.tokens)
        self.entities = ne_chunk(self.q_tagged)

        self.q_word = self.tokens[0] if self.tokens[0] in q_words else ""

        self.q_keywords = [token for i, token in enumerate(self.tokens)
                           if token not in set(stopwords.words('english'))
                           and token not in set(q_words)]

    def remove_alien_char(self, str):
        """Remove unwannted words/character,?,! from question
        Only accept alphanumeric, space, period
        :return: String of filtered text
        """
        reg = r'[^a-z0-9\s]*'
        return re.sub(reg, '', str)

    def find_q_type(self):
        """TODO
        Tried to used Tensor flow, but run too slow
        Use default type for now since the QA only answer
        disease and medication question
        :return: the question type
        """
        q_type = "ENTY:dismed"
        return q_type

    def find_a_type(self):
        """
        Each a type must include
            FOCUS word(s)
            OTHER for any words after FOCUS group

        Optional:
            VERB the verb used with question e.g are,is
                This willl be use to build answer phrase e.g "FOCUS VERB OTHER"

        Make sure to remove alien characters such as question mark
        :return:
        """
        a_type = "OTHER"
        a_types_reg = {
            "TREATMENT": 'what\s?(?P<verb>is|are)?.*(treatment[s]?)\s(of|for)?\s(?P<focus>\w+( \w+)?)(?P<other>.*)',
            "SYMPTOM": 'what\s?(?P<verb>is|are)?.*(symptom[s]?).*of\s(?P<focus>\w+( \w+)?)(?P<other>.*)',
            "DEFINITION": 'what\s(?P<verb>is|are)\s(?P<focus>\w+( \w+)?)\s?(?P<other>.*)?',
            "CAUSES": 'what\s?(?P<verb>cause[s]?)\s(?P<focus>\w+( \w+)?)(?P<other>.*)',
            "FREQUENCY": 'how\s(?P<frequency>long|many|much|high|low)\s(?P<focus>.*)',
            "TIME": 'when\s?(?P<verb>do|does|can|could|should|is|are)?\s?(?P<pronoun>i|you|we|they|he|she|it)?\s?(?P<focus>.*)',
            "LOCATION": 'where\s?(do|does|can|could|should|is|are)?\s?(?P<focus>.*)',
            "DESCRIPTION": 'why\s?(do|does|can|could|should|is|are)?\s?(?P<pronoun>i|you|we|they|he|she|it)?\s?(?P<focus>.*)',
            "PERSON": 'who\s?(do|does|can|could|should|is|are)?\s?(?P<pronoun>i|you|we|they|he|she|it)?\s?(?P<focus>.*)',
            "BINARY": '^(do|does|did|are|is|was|were|have|has|can|will|should|could)\s(?P<pronoun>i|you|we|they|he|she|it)?\s?(?P<focus>.*)',
            "OTHER": '(?P<focus>.*)'
        }

        for k, type in enumerate(a_types_reg):
            r = re.compile(r'{}'.format(a_types_reg.get(type)))
            match = r.search(self.q_cleaned)

            if match:
                if len(match.groupdict()) != 0:
                    self.matched_groups = match.groupdict()
                return type
        return a_type


if __name__ == "__main__":
    """
    For testing purpose
    This file can be running alone
    Run this file to see details as described below
    """
    questions = [
        "Who do I contact if I have coronavirus?"
    ]

    for q_ in questions:
        q = QuestionClassifier(q_)

        print("=================")
        print("Raw Tokens:", q.tokens_raw)
        print("Filtered and Lemmatized tokens: ", q.tokens)
        print("Tagged:", q.q_tagged)
        # print("Entities:", q.entities)
        print("Question type:", q.q_type)
        print("Question word: ", q.q_word)
        print("Answer type:", q.a_type)
        print("Focus word:", q.matched_groups.get('focus'))
