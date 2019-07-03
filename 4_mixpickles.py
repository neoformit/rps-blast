import pickle
from os import walk

wd = 'C:\\Users\\Public\\Documents\\Google Drive\\Python\\Standalone RPS-blast\\pickles'
fnames = []

for root, dirs, files in walk(wd):
    for file in files:
        if '.pkl' in file:
            fnames.append('pickles\\' + file)

cdData = {}
ow_chunks = []
ow = []

i=0
k=0

for fname in fnames:
    with open(fname, 'rb') as p:
        data = pickle.load(p)
        p.close()
    for key, value in data.items():
        if key in cdData:
            chunk = fname.replace('pickles\\','')
            chunk = chunk.replace('.pkl','')
            ow.append(chunk + ', ' + key)
            if chunk not in ow_chunks:
                ow_chunks.append(chunk)
        cdData[key] = value
        i+=1
    k+=1

print(str(i) + ' keys copied from ' + str(k) + ' pickles')

with open('Monodon domains.pkl','wb') as p:
    pickle.dump(cdData,p)
    p.close()

with open('duplicates.txt','w') as w:
    w.write('\n'.join(ow))
    w.close()