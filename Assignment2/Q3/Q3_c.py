from os import listdir
from os.path import isfile, join
import numpy as np
import re
import nltk.data
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier
from sklearn import metrics
from gensim.models import Word2Vec


def AvgFeatureVec(reviews, model, NumFeatures):
    counter = 0.
    FeatureVec = np.zeros((len(reviews),NumFeatures),dtype="float32")
    for words in reviews:
        if counter%1000. == 0.:
           print "FeatureVectorProcessed %d of %d" % (counter, len(reviews))
           
        featureVec = np.zeros((NumFeatures,),dtype="float32")
        NumberWords = 0
        Index2WordSet = set(model.index2word) # set consisiting of all words in model

        for word in words:
            if word in Index2WordSet: 
                NumberWords = NumberWords + 1.
                featureVec = np.add(featureVec,model[word])

        if NumberWords > 0:
            FeatureVec[counter] = np.divide(featureVec,NumberWords)

        counter = counter + 1.
    return FeatureVec

def ReadData(Path):
    files=[]
    for filename in listdir(Path):
        file_path = join(Path, filename)
        data=open(file_path).read()
        files.append(data)        
    return files 

model = Word2Vec.load("300features_40minwords_10context")
NumFeatures = 300

#################################### Train Data #######################################

TrainNegData = (ReadData('./aclImdb/train/neg/'))
TrainPosData = (ReadData('./aclImdb/train/pos/'))

TrainReviews = TrainNegData + TrainPosData
TrainLabel = []
for index in xrange(0,len(TrainReviews)):
	if index < len(TrainNegData):
		TrainLabel.append('negative')
	else:
		TrainLabel.append('positive')

print "Training Data"

TrainAvgVec = AvgFeatureVec( TrainReviews, model, NumFeatures )

TrainLabel = np.asarray(TrainLabel)

################################### Test Data #################################

TestNegData = (ReadData('./aclImdb/test/neg/'))
TestPosData = (ReadData('./aclImdb/test/pos/'))
TestReviews = TestNegData + TestPosData

TestLabel = []
for index in xrange(0,len(TestReviews)):
    if index < len(TestNegData):
        TestLabel.append('negative')
    else:
        TestLabel.append('positive')

print "Test Data"

TestLabel = np.asarray(TestLabel)
TestAvgVec = AvgFeatureVec(TestReviews, model, NumFeatures )


################################### Classifiers ################################
print "Classifier is Running"
forest=AdaBoostClassifier()
forest = forest.fit( TrainAvgVec, TrainLabel )
PredictedLabel = forest.predict( TestAvgVec )
Accuracy = metrics.accuracy_score(PredictedLabel,TestLabel)
print Accuracy

#Accuracy= 60.988 - 10 min