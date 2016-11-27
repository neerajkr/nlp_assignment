from nltk.corpus import brown
from nltk.tag import tnt


data=brown.tagged_sents()
size=len(data)

partition=int(size*0.9)

train_data =brown.tagged_sents()[:int(size*0.9)]
test_data=brown.tagged_sents()[int(size*0.9):int(size*0.9)+1000]

print len(train_data)
print len(test_data)


tnt_pos_tagger = tnt.TnT()

tnt_pos_tagger.train(train_data)

print "Training Done!!"
print tnt_pos_tagger.evaluate(test_data)

# Accuracy- 0.927815262913 - 15 min
