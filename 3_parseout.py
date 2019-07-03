from os import walk
import pickle

wd = 'C:\\Users\\Public\\Documents\\Google Drive\\Python\\Standalone RPS-blast\\rps_xml'
fnames = []

for root, dirs, files in walk(wd):
    for file in files:
        if '.out' in file:
            fnames.append(file)

for fname in fnames:
    
    copy = False
    
    file = fname.replace('.out','')
    
    r = open('rps_xml\\' + fname ,'r')
    w = open('pickles\\' + file + '.csv','w')
    p = open('pickles\\' + file + '.pkl','wb')
    
    cdData = {}
    
    for line in r:
        if line[0] == '#':
            continue
        line = line.replace('\n','')
        line = line.split('\t')
        line[:-1].append(line[-1].replace('\n',''))
        
        if line[0] == 'QUERY':
            query = line[4]
        
        if line[0] == 'DOMAINS':
            copy = True
        elif line[0] == 'ENDDOMAINS':
            copy = False
        
        if copy is True:
            if line[0] == '1':
                if query not in cdData.keys():
                    cdData[query] = []
                
                domain = line[9]
                start = line[4]
                stop = line[5]
                e = line[6]
                bits = line[7]
                accession = line[8]
                trunc = line[10]
                
                data = [domain,start,stop,e,bits,trunc,accession]
                
                cdData[query].append(data)
    
    pickle.dump(cdData,p)
    
    w.write('Transcript,' + ','.join([
            'domain','start','stop','e-value','bits','trunc','accession']) + '\n')
    
    for key in cdData:
        for item in cdData[key]:
            w.write(key + ',')
            for i in item:
                w.write(i + ',')
            w.write('\n')
    
    r.close()
    w.close()
    p.close()    