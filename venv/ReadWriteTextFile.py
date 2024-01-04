import spacy
nlp = spacy.load('en')
doc = nlp(u'Hi Dave, I’d like to invest $10,000 with Microsoft and another $15,000 with Amazon. Thanks, Tom.')

# save spaCy data to a text file
f = open('demo.txt', mode='wt', encoding='utf-8')

for token in doc:
	f.write(token.text + "," + token.pos_ + "," + token.tag_ + "," + token.dep_ + "," + str(spacy.explain(token.dep_)) + '\n')

f.close()

# read spaCy data from a text file
f = open('demo.txt', mode='r', encoding='utf-8')
for line in f:
	line = line.strip('\n')
	print(line)

f.close()