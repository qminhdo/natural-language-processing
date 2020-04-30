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
            ans = re.sub(r'\.', ' ', ans)
            ans = re.sub(r',$', '', ans)
            ans += '.\n\n'

            # if the answer contain a List
            # format the answer such that for there will be a list after ":"
            r = re.compile(r':\s?(?P<section>.*)\s?\.', re.IGNORECASE)
            match = r.search(ans, re.IGNORECASE)
            section = ""

            if match:
                section = match.groupdict().get('section').strip()

                # check if section contain child list
                r_ = re.compile(r'(;)', re.IGNORECASE)
                match_ = r_.search(ans, re.IGNORECASE)

                section = self.build_list(section, ';') if match_ else self.build_list(section, ',')
                section = ":\n\t- " + section
                ans = re.sub(r, section, ans)

            answer += ans

        return answer

    def build_list(self, text, deliminator):
        sents_list = text.split(deliminator)
        sents_list = set(sents_list)
        sents_list = list(sents_list)
        sents_list = [sent.strip().capitalize() for sent in sents_list if sent.strip() != ""]
        text = "\n\t- ".join(sents_list)
        return text

if __name__ == "__main__":
    pass