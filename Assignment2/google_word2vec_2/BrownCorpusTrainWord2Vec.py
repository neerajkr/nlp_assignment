import numpy as np
import string
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn import metrics
import nltk.data
from nltk.corpus import brown
import logging
from gensim.models import word2vec
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
TaggedSentences = brown.tagged_sents()


SentencesOnly = []
for sent in TaggedSentences:
	words = [word.lower() for (word,tag) in sent if word not in string.punctuation]
	SentencesOnly.append(words)

NumFeatures = 300
MinWordCount = 40
ContextWindow = 10

model = word2vec.Word2Vec(SentencesOnly, workers=4, size=NumFeatures, min_count = MinWordCount, window = ContextWindow, sample = 1e-3)
model.init_sims(replace=True)
model_name = "300features_40minwords_10context_brown"
model.save(model_name)