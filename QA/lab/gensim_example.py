from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec

path = ("dismed.model")
print(path)

text = open("data/cogcomp/train_set/dismed.txt", "r")
model = Word2Vec(text, size=100, window=5, min_count=1, workers=4)
model.save("dismed.model")