import sys
import nltk
from question_classifier import QuestionClassifier
from query_formulator import QueryFormulator
from passage_retriever import PassageRetriever
from answer_processor import AnswerProcessor

sys.path.append(".")
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('maxent_ne_chunker')

def main():

    with open('TESTS.txt', 'r', encoding='utf8') as f:
        for question in f:
            print("\n============================")
            print("Answering question: ", question, end="")
            print("processing ...")
            try:
                q_classifier = QuestionClassifier(question)
                queries = QueryFormulator(q_classifier).queries
                passages_scores = PassageRetriever(q_classifier, queries).candidate_passages
                best_answer = AnswerProcessor(q_classifier, passages_scores).best_answer
                print("Answer: ")
                print(best_answer)

            except:
                print("Some thing went wrong")


if (__name__ == "__main__"):
    main()
