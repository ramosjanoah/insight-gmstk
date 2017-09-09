import os, json
from sklearn.feature_extraction.text import TfidfVectorizer
file_list = os.listdir('corpus')

users = []
corpus = []

for file in file_list:
    try:
        fin = open('corpus/'+file, 'r')
        stream = fin.read()
        users.append(file)
        corpus.append(stream)
    except IOError:
        print (file + " not found")


tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(corpus)
feature_names = tfidf.get_feature_names()
dense = tfidf_matrix.todense()

for idx in range(0, len(file_list)-1):
    d = dense[idx].tolist()[0]
    pair = []
    for idx, val in enumerate(d):
        if val > 0:
            pair.append((val, idx))

    spair = sorted(pair, reverse=True)
    stopic = []
    for (val, idx) in spair[:5]:
        stopic.append(feature_names[idx])


data = {}
for i in range(0, len(file_list)-1):
    d = dense[i].tolist()[0]
    pair = []
    for idx, val in enumerate(d):
        if val > 0:
            pair.append((val, idx))
    spair = sorted(pair, reverse=True)
    stopic = []
    for (val, idx) in spair[:5]:
        stopic.append(feature_names[idx])
    data[file_list[i]] = stopic


with open('tfidf_result.json', 'w') as fout:
    json.dump(data, fout)
