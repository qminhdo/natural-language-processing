perplexity = __import__("perplexity")

######################
# Test
class UnitTest:
    def __init__(self):
        sentences_filename = "text/sample_quiz_sentences.txt"
        model_filename = "text/sample_quiz.txt.model"

        self.p = perplexity.Perplexity(model_filename, sentences_filename)


    def run_all_tests(self):
        print("=============================")
        print("Running tests for perplexity.py")
        self.test_compute_I()
        self.test_compute_log_prob()
        self.test_compute_perplexity()
        print("End")
        print("=============================")

    def test_compute_I(self):
        print("Test compute_I()")
        probs = [3/25, 1/25]
        sentences_words_count = 9
        result = self.p.compute_I(probs, sentences_words_count) == -0.8558610976475881
        print("  it should equal -0.8558610976475881:", result)

    def test_compute_log_prob(self):
        print("Test compute_log_prob()")
        probs = [0, 1, 2]
        result = self.p.compute_log_prob(probs) == -32.219280948873624
        print("  it should equal -32.219280948873624:", result)

    def test_compute_perplexity(self):
        print("Test compute_perplexity()")
        self.p.probs =  [3/25, 1/25]

        self.p.sentences_words_count = 9
        print("RESULT:",self.p.compute_perplexity() )
        result = self.p.compute_perplexity() == 1.8098386665194313
        print("  it should equal 1.8098386665194313:", result)

t = UnitTest()
t.run_all_tests()

prob = 1e-10
sum = math.log(prob, 2) * 3000
# sum = -10000000000
print("sum log", sum)
L = sum/ 2000

print("test perplexity :",2**(-L))