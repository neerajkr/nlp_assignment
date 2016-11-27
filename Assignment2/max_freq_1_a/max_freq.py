from nltk.corpus import brown
import operator
import nltk

data=brown.tagged_words()

train_corpus= data[:int(len(data)*.9)]
test_corpus=data[int(len(data)*.9):]

cdf1 = nltk.ConditionalFreqDist(train_corpus)
i=0
for word,tag in test_corpus:
	stats=cdf1[word]     #http://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
	try:
		predicted=(max(stats.iteritems(), key=operator.itemgetter(1))[0])

		if (predicted.encode('utf8')==tag.encode('utf8')):
			i=i+1
	except:
		if(tag.encode('utf8')=='NN'):
	 		i=i+1
			
print "Accuracy: "
print((float(i)/len(test_corpus)))

# Accuracy= 88.9846 - 1 min