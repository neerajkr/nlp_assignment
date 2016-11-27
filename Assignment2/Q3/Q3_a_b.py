import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import re

from sklearn.feature_extraction.text import TfidfTransformer

################################# Training Data #####################################
TrainingData=[]
for (root, dirs, files) in os.walk("train/neg"):
    for filename in files:
    	with open(os.path.join(root,filename)) as data:
			TrainingData.append(data.read())

for (root, dirs, files) in os.walk("train/pos"):
    for filename in files:
    	with open(os.path.join(root,filename)) as data:
			TrainingData.append(data.read())

TrainingLabel=[0]*12500+[1]*12500;

vectorizer = CountVectorizer(analyzer="word",binary=True,   tokenizer=None,    preprocessor=None, 
                          stop_words=None, max_features=5000)
train_data_features = vectorizer.fit_transform(TrainingData)

transformer = TfidfTransformer(norm=u'l2', use_idf=True, smooth_idf=True, sublinear_tf=True)
# train_data_features = transformer.fit_transform(train_data_features)

# print (train_data_features)

forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit(train_data_features,TrainingLabel)


######################################## Testing Data      #######################

TestingData=[]
for (root, dirs, files) in os.walk("test/pos"):
    for filename in files:
    	with open(os.path.join(root,filename)) as data:
			TestingData.append(data.read())

for (root, dirs, files) in os.walk("test/neg"):
    for filename in files:
    	with open(os.path.join(root,filename)) as data:
			TestingData.append(data.read())

TestingLabel=[1]*12500+[0]*12500;

test_data_features = vectorizer.fit_transform(TestingData)
# test_data_features = transformer.fit_transform(test_data_features)

print (test_data_features)

score= forest.score(test_data_features,TestingLabel)
print score


# Accuracy=   51.98 (binary count 3(a)) -5 min
# Accuracy=   50.736 (tfidf 3(b)) - 5 min




    