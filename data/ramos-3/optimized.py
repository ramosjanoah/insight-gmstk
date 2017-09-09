import os, json, re, io
file_list = os.listdir('media')

from pprint import pprint
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

stoplist = []
with open('stopwords_indo', 'r') as f:
    stoplist = f.readlines()

stoplist = [x.strip() for x in stoplist]
stoplist = stoplist + stopwords.words('english')

ep = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "]+", flags=re.UNICODE)

factory = StemmerFactory()
stemmer = factory.create_stemmer()
snowball = SnowballStemmer('english')

try:
    os.makedirs('corpus')
except OSError:
    print ("directory exist")

ib = int(input("Begin index: "))
ie = int(input("End index: "))

for folder in file_list[ib:ie]:
    print ("Processing: " + folder)
    if os.path.isfile('corpus/'+folder):
        print (folder + " already processed")
    else:
        try:
            fin = io.open('media/'+folder+'/'+folder+'.json', 'r', encoding='utf-8')
            data = json.load(fin)
            captions = []
            for post in data:
                if post['caption'] is not None:
                    captions.append(snowball.stem(ep.sub(r'', post['caption']['text'])))
                    captions = [stemmer.stem(caption) for caption in captions]
            if captions:
                user = str(folder)
                fout = open('corpus/'+user, 'w')
                words = []
                for caption in captions:
                    words = words + word_tokenize(caption)
                words = [word for word in words if word not in stoplist and not word.isdigit() and len(word)>1]
                s = " "
                stream = s.join(words)
                fout.write(stream)
                fout.close()
                print ("Done: " + folder)
        except IOError:
            print (folder + " is private")
