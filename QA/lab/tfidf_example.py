

"""
Text feature extraction
"""

from sklearn.feature_extraction.text import CountVectorizer

"""
 CountVectorizer()
 use for term frequency
 uses default analyzer called WordNGramAnalyzer to remove
 unnecessary characters e.g. lowercase, accesnts, filter stop words...
"""
vectorizer = CountVectorizer(stop_words=["the", "is"])
# print(vectorizer)

# Defines train and test set
train_set = ("The sky is blue.", "The sun is bright.")
test_set = ("The sun in the sky is bright.",
    "We can see the shining sun, the bright sun.")

# Create vocabulary or feature
vectorizer.fit_transform(train_set)
# print feature index {'the': 5, 'sky': 3, 'is': 2, 'blue': 0, 'sun': 4, 'bright': 1}
print(vectorizer.vocabulary_)

# print features names only ['blue', 'bright', 'is', 'sky', 'sun', 'the']
print(vectorizer.get_feature_names())

# create Scipy sparse matrix
sparse_matrix = vectorizer.transform(test_set)
print(sparse_matrix)



