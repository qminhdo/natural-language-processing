import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag


grammar = r"""
  NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
  PP: {<IN><NP>}               # Chunk prepositions followed by NP
  VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
  CLAUSE: {<NP><VP>}           # Chunk NP, VP
  """
cp = nltk.RegexpParser(grammar)



sent = "is medicine necessary to lower the fever"
tokens = word_tokenize(sent)
tagged = pos_tag(tokens)

chunks = cp.parse(tagged)
print(chunks)
