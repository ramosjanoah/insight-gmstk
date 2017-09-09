import os
a_list = []
file_list = os.listdir('media')
import json
from pprint import pprint
folder = file_list[0]
file = os.listdir('media/' + folder)
f = open('media/' + folder + '/' + file[0], 'r')
data = json.load(f)
for post in data:
	a_list.append(post['caption']['text'])

data[0]['caption']['text']

