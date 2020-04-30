import nltk

class QuestionClassifier:
    def get_classifier(self):
        fine_grain = True
        classifier = QuestionClassifier(fine_grain)
        train_set = classifier.load_labelled_data('data/cogcomp/train_set/train_5500.label', fine_grain=fine_grain)
        accuracy = 0
        for C in [5 * x for x in range(19, 30)]:
            # for C in [0.1,0.01,0.001,0.0001,0.00001]:
            classifier.train_classifier(train_set, C=C, fine_grain=fine_grain)
            tempAcc = nltk.classify.accuracy(classifier.classifier, test_set)
            if tempAcc > accuracy:
                accuracy = tempAcc
                C_VAL = C
            # print C,":", tempAcc
        # print "Training with C ", C_VAL
        classifier.train_classifier(train_set, C=C_VAL, fine_grain=fine_grain)
        return classifier

q_classifier = QuestionClassifier.get_classifier()
q_type = q_classifier.classify("What is fever?")