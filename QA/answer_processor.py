import re

class AnswerProcessor:
    """
    Possible answer type:
        DEFINITION, TREATMENT, DESCRIPTION, SYMPTOMS
        The job of a answer processor is to return the answer correctly

        The answer types are:
        * Definition  # usually a word, exact meaning and must be correct
        * Description # more detailed, can be bias
        * Treatment / Prevention  # have related keywords like "treatment, heal, care, prevent"
        * Symptom # have related keywords like "cause, symptom"
        * Binary (yes/no verification)
        * Location  $ body part related
        * Time # frequency of taking drug, occurence of disease, how long it last

    http://sujitpal.blogspot.com/2014/12/semantic-similarity-for-short-sentences.html
    """

    def __init__(self, q_classifier, passages_scores):
        """
        :param q_classifier: QuestionClassifier instance
        :param passages_scores: dict of passage: score
        """
        self.passages_scores = passages_scores
        self.q_classifer = q_classifier
        self.best_answer = self.get_best_answer()

    def get_best_answer(self):
        # Sort passages and scores
        sorted_ps = (sorted(self.passages_scores.items(), key=
                        lambda kv: (kv[1], kv[0]), reverse=True))

        ps = sorted_ps[0:2]
        answer = ""

        for ps_ in ps:
            ans = ps_[0].capitalize()
            ans = re.sub('\.', ' ', ans)
            answer += ans + ' . '

        return answer

    def normalize_passages(self):
        pass


if __name__ == "__main__":
    pass
