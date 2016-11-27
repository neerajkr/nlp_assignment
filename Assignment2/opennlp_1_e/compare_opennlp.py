TestAndTag=open("TestAndTag.txt","r");
TestAndTag=TestAndTag.read()

TestAndTag=TestAndTag.split()

PredictAndTag=open("PredictAndTag.txt","r");
PredictAndTag=PredictAndTag.read()

PredictAndTag=PredictAndTag.split()

print len(TestAndTag)
# print len(PredictAndTag)


count=0;
for i in range(0,len(TestAndTag)):
	if(TestAndTag[i]==PredictAndTag[i]):
		count=count+1;

print count

print float(count)/(len(TestAndTag))


# Accuracy- 0.95952515664 - 10 sec
