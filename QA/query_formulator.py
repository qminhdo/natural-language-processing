import nltk
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.corpus import wordnet

wn_senses = set()
wn_senses.update(['illness.n.01', 'disorder.n.01', 'medicine.n.02', 'drug.n.01',
                  'ill_health.n.01', 'injury.n.01', 'distress.n.01',
                  'pain.n.02', 'pain.n.01', 'disease.n.01',
                  'condition.n.01', 'organ.n.01', 'symptom.n.01',
                  'liquid_body_substance.n.01', 'bodily_property.n.01',
                  'tumor.n.01'])

custom_stop_words = ["few", "little", "much", "more", "cause", "symptom", "treatment", "prevent"]
wn_stop_words = set(stopwords.words('english'))
wn_stop_words.update(custom_stop_words)


class QueryFormulator:
    """
    Prepare the queries for the DocumentRetriever
    Look for direct related query keywords
    If sense is not found
    Then use focus word as query
    """

    def __init__(self, q_classifer):
        self.q_classifer = q_classifer
        self.stop_words = wn_stop_words
        self.senses = self.find_senses(self.q_classifer.tokens)
        self.queries = self.find_queries(self.senses)

    def find_queries(self, senses):
        """
        If the words match the senses
        Add to the queries list
        If no senses, use focus word as query

        :param senses:
        :return list: the query that will be used for PassageRetriever. Sample: {'cancer', 'aspirin'}
        """
        queries = set()
        for token in senses:
            queries.add(token)

        if (len(queries) == 0):
            focus = self.q_classifer.matched_groups['focus'].split()
            focus = [f for f in focus if f not in set(stopwords.words('english'))]
            queries = focus

        return queries

    def find_senses(self, tokens):
        """ Get all the senses of word and hypernym

        :return dict: senses  {'aspirin': 'medicine.n.02', 'cancer': 'tumor.n.01'}
        """
        senses = dict()
        for token in tokens:
            senses_tmp = set()
            if token not in self.stop_words:
                w_syns = wordnet.synsets(token)
                senses_tmp.update(self.find_hypernyms(w_syns))

                for sense in senses_tmp:
                    if sense in wn_senses:
                        senses.update({token: sense})

        return senses

    def find_hypernyms(self, syns):
        """
        Loop through hypernyms tree and find senses
        :param syns:
        :return:
        """
        names = set()
        # Find hypernyms of each syn
        for syn in syns:
            hypernyms = syn.hypernyms()
            # find hypernyms one more level up
            for hypernym in hypernyms:
                names.add(hypernym.name())
                hypernyms_second = hypernym.hypernyms()
                for h in hypernyms_second:
                    names.add(h.name())
        return names


if __name__ == "__main__":
    """
    For testing purpose
    This file require QuestionClassifier
    
    Run this file to see details as described below
    """
    from question_classifier import QuestionClassifier

    questions = [
        "Who do I contact if I have coronavirus?"
        # "what are the treatment for hay fever",
        # "treatment for hay fever",
        # "what are the symptoms of hay fever",
        # "what is hay fever",
        # "what cause depression",
        # "how many times do i take aspirin in a day",
        # "where does acne occur most",
        # "where do i go to take vaccine for hay fever",
        # "why do i have hay fever",
        # "who do i contact if i have hay fever",
        # "is aspirin lethal",
        # "Can ADHD cause depression",
        # "what do i do if i have fever",
        # "What happens during a diagnosis of adult ADHD?"
    ]

    for q_ in questions:
        print("=======================")
        print(q_)
        q_classifier = QuestionClassifier(q_)
        q = QueryFormulator(q_classifier)
        print("Senses:", q.senses)  # {'aspirin': 'medicine.n.02', 'cancer': 'tumor.n.01'}
        print("Queries:", q.queries)  # {'cancer', 'aspirin'}
