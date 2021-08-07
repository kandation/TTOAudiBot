
import json
import os

with open('song_entry.json', mode='r') as fo:
    data = json.loads(fo.read())


for i,s in enumerate(data):
    name = str(s.get('name')).lower().replace(' ','_').replace('\'','')
    index = str(i+1).zfill(2)
    file_name =f'./notes/{index}_{name}.txt'


    if not os.path.isfile(file_name) :
        print(f'GENERATE: {file_name}')
        with open(file_name, mode='w') as  fo:
            fo.write('')
    else:
        print(f'IS_ESIST: {file_name}')