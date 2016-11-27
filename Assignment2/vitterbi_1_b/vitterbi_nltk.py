# Ref: https://gist.github.com/blumonkey/007955ec2f67119e0909

import nltk
from nltk.corpus import brown

# Train data - pretagged


TotalCorpusSent = brown.tagged_sents()

## Split into train and test data

size = int(0.9*len(TotalCorpusSent))
train_data = TotalCorpusSent[:size]
test_data = TotalCorpusSent[size:]

# print train_data[0]

# Import HMM module
from nltk.tag import hmm

# Setup a trainer with default(None) values
# And train with the data
trainer = hmm.HiddenMarkovModelTrainer()
tagger = trainer.train_supervised(train_data)

print tagger
# Prints the basic data about the tagger

total_count=0
correct_count=0
temp_count=0
for sent in test_data: 
	test_d=[x[0] for x in sent]
	predict_data=tagger.tag(test_d)
	if ((temp_count+1)%100 == 0):
		print "Review %d of %d\n" % ( temp_count+1, len(test_data) )
		print total_count
		print correct_count
	# print predict_data
	# print sent
	total_count+=len(sent)
	correct_count+=len([i for i, j in zip(predict_data, sent) if i == j])	
	temp_count=temp_count+1

# print tagger.tag(test_d)

# print sent
print float(correct_count)/total_count

#Accuracy= 64498/94749=0.68072486253 - 20 min
