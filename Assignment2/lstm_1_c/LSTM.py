
import numpy as np
from keras.preprocessing import sequence
from keras.models import Model, Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Input, TimeDistributed, Activation
from nltk.corpus import brown
import numpy as np
from collections import Counter

BrownText = brown.tagged_sents()
WordsAppendedOnly = []
TagsAppendedOnly = []
AllTags = []
for sent in BrownText:
		OnlyWords = [word for (word,tag) in sent ]
		OnlyTags = [tag[:2] for (word,tag) in sent]
		WordsAppendedOnly.append(OnlyWords)
		TagsAppendedOnly.append(OnlyTags)
		AllTags.extend(tag[:2] for (word,tag) in sent)

DictTag = {}
i = 1
AllTagsCounter = Counter(AllTags)
NumberOfTags = len(AllTagsCounter.items())
for tag,count in AllTagsCounter.items():
	DictTag[tag] = i
	i=i+1

word_dict = {}
SentenMaxLength = 30
tags_matrix = np.zeros((len(BrownText),SentenMaxLength))

for sent_nb, sent in enumerate(BrownText):
	for word_nb,wt in enumerate(sent):           ## count starts from 0
			word = wt[0].lower()
			word_dict[word] = 1 
			# testnum=testnum+1
			if word_nb < SentenMaxLength:
				tags_matrix[sent_nb][word_nb] = DictTag[wt[1][:2]]
			else:
				break

word_key = 1
for word in word_dict.keys():
	word_dict[word] = word_key
	word_key += 1

VocabLen = word_key - 1


InputWordMatrices = np.zeros((len(BrownText),SentenMaxLength))
for sent_nb, sent in enumerate(BrownText):
	for word_nb, wt in enumerate(sent):
		word = wt[0].lower()
		if word_nb < SentenMaxLength:
			InputWordMatrices[sent_nb][word_nb] = word_dict[word]
		else:
			break

OutputHotVectors = []
for sent in tags_matrix:
	a = sent.astype(int)
	b = np.zeros((SentenMaxLength, NumberOfTags+1))
	b[np.arange(SentenMaxLength),a] = 1
	OutputHotVectors.append(b)

InputWordMatrices = InputWordMatrices.astype(int)
OutputHotVectors = np.array(OutputHotVectors)

VocabLen=VocabLen+1
NumberOfTags=NumberOfTags+1

# print InputWordMatrices
# print len(InputWordMatrices)

# print OutputHotVectors
# print len(OutputHotVectors)

# print NumberOfTags
# # print len(NumberOfTags)

# print SentenMaxLength
# # print len(SentenMaxLength)

# print VocabLen
# # print len(VocabLen)


np.random.seed(2200)  # for reproducibility
max_features = VocabLen
batch_size = 16

size = int(0.8*len(InputWordMatrices))

print('Loading data...')

X_train = InputWordMatrices[:size]
y_train = OutputHotVectors[:size]
X_test = InputWordMatrices[size:]
y_test = OutputHotVectors[size:]

print(len(X_train), 'train sequences')
print('X_train shape:', X_train.shape)
print('y_train shape:', y_train.shape)
print('X_test shape:', X_test.shape)
print('y_test shape:',y_test.shape)

print('Build model...')
model = Sequential()
model.add(Embedding(max_features, 128, input_length=SentenMaxLength))

model.add(LSTM(128,return_sequences=True))  
model.add(Dropout(0.5))
model.add(TimeDistributed(Dense(NumberOfTags)))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',metrics=['accuracy'], optimizer='adam', class_mode="binary")


print(model.summary())
print("Train...")
model.fit(X_train, y_train, batch_size=batch_size,
			 nb_epoch=1, validation_split=0.2, show_accuracy=True, shuffle=True)
score, acc = model.evaluate(X_test, y_test, batch_size=batch_size, show_accuracy=True)
print('Test score:', score)
print('Test accuracy:', acc)

# Accuracy- ('Test accuracy:', 0.99647709491321923)- 5 min