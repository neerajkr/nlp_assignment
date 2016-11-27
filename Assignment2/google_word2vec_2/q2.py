
import numpy as np
from matplotlib import pyplot as plt
import string
from collections import Counter
from gensim.models import Word2Vec
from scipy import spatial
from nltk.corpus import brown
from math import* 
def CosineSimilarity(x,y): 
	numerator = sum(a*b for a,b in zip(x,y))
	denominator = round(sqrt(sum([a*a for a in x])),3)*round(sqrt(sum([a*a for a in y])),3)
	return round(numerator/float(denominator),3) 
GoogleWord2Vec = Word2Vec.load_word2vec_format('./GoogleNews-vectors-negative300.bin',binary=True)
BrownWord2Vec = Word2Vec.load("300features_40minwords_10context_brown")
words = brown.words()
words = [word.lower() for word in words if word not in string.punctuation]
vocab = Counter(words)
SimilarityValue = []
for word,count in vocab.items():
	try:
		b = GoogleWord2Vec[word]
		a = BrownWord2Vec[word]
		result = CosineSimilarity(a, b)
		SimilarityValue.append(result)
	except:
		continue
bins = np.linspace(min(SimilarityValue), max(SimilarityValue), 11)
plt.xlim([min(SimilarityValue)-1, max(SimilarityValue)+1])
plt.hist(SimilarityValue,bins=bins)
plt.show()