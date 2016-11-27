from nltk.corpus import brown
import numpy as np
from collections import Counter


text = brown.tagged_sents()

text_sequences = []
tag_sequences = []
text_tag=[]
all_tags = []
for sent in text:
		words_only = [word for (word,tag) in sent ]
		text_and_tag=[word+"_"+tag for (word,tag) in sent ]


		tags_only = [tag[:2] for (word,tag) in sent]
		text_sequences.append(words_only)
		tag_sequences.append(tags_only)
		text_tag.append(text_and_tag)
		all_tags.extend(tag[:2] for (word,tag) in sent)


# print text_sequences
# print tag_sequences
# # print all_tags

# print len(text_sequences)

# print len(tag_sequences)

# print len(all_tags)

# print len(text)
# print text[0]

# print text_tag[0]

# text_file = open("Output2.txt", "a")


# with open('output.txt', 'a') as file:
# for i in range(0,len(text_sequences)):
# 	line_data=" ".join(text_sequences[i])
# 	text_file.writelines(line_data+"\n")


text_file = open("TestAndTag.txt", "a")
text_file1 = open("TestNoTag.txt", "a")
# training=open("TrainAndTag.txt", "a")


# with open('TextAndTag.txt.txt', 'a') as file:
for i in range(int(len(text_tag)*.9),int(len(text_tag))):
	line_data1=" ".join(text_sequences[i])
	line_data=" ".join(text_tag[i])
	text_file.writelines(line_data+"\n")
	text_file1.writelines(line_data1+"\n")
	# training.writelines(line_data+"\n")

text_file.close()
text_file1.close()

# training.close()