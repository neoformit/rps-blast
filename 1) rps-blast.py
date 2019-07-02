# Maybe try threading to see if speeds up?
# Bite 2000 seq chunks out of proteome and save as temp(x).fa
# Make call to rpsblast through batch file
# Iterate through chunks, logging time.

import os
import time
import psutil
import datetime

def HMS(Ts):
    sec = round(Ts,2)
    tStr = str(datetime.timedelta(seconds=sec))
    if '.' in tStr:
        t = tStr.split('.')
        tStr = t[0] + '.' + t[1][:2]
        return tStr
    else:
        return tStr

r = open('BBLC.fa','r')
fnames = []
copy = ''
copyStr = ''
i=0
k=1

for line in r:
    if line[0]=='>':
        lastAA = ''.join(copy.split('\n')[1:-1])
        if len(lastAA) >= 4:
            copyStr += copy
        if i==2000:
            i=0
            k+=1
            fname = 'temp\\temp('+str(k)+').fasta'
            fnames.append(fname)
            with open(fname,'w') as w:
                w.write(copyStr)
                w.close()
            copyStr = ''
        copy = ''
        i+=1
    copy += line
r.close()

fname = 'temp\\temp('+str(k)+').fasta'
fnames.append(fname)
with open(fname,'w') as w:
    w.write(copyStr)
    w.close()
print('\n' + str(k) + ' chunks saved.')

path = "C:\\Users\\Public\\Documents\\Google Drive\\Python\\Standalone RPS-blast\\temp"


#%%============================================================================
# Should take about 23:30 mins per 5000 seq chunk
# (approx 22 hours for 58 chunks)

print('\n====================================================================')
cwd = os.getcwd()
bat = '"' + cwd + '\\temp\\rpsblast.bat"'

start = 1
end = k+1
for i in range(start,end):
    file = "temp\\temp(" + str(i) + ").fasta"
    Tc = time.ctime().split(' ')[-2]
    print('\nProcessing chunk ' + str(i) + ' at ' + Tc + '...')
    T = time.time()
    out = file.replace('.fasta','.xml')
    
    batch = ('cd "C:\\Users\\Public\\Documents\\Google Drive\\Python\\Standalone RPS-blast"' +
            '\nrpsblast -query ' + file + ' -evalue 0.01' +
            ' -seg no -outfmt 5 -db db\\Cdd -out ' + out)
    with open('temp\\rpsblast.bat','w') as b:
        b.write(batch)
        b.close()
    os.system(bat)
    
    Tp = HMS(time.time() - T)
    time.sleep(5)
    m = psutil.virtual_memory()
    ram = str(m.percent) + '%'
    cpu = str(psutil.cpu_percent()) + '%'
    
    
    print('\nChunk ' + str(i) + ' processed in ' + Tp + ' Hrs')
    print('\nCPU: ' + cpu + '    RAM: ' + ram)
    print('------------------------------------------------------------------')

#%%============================================================================
# Use this cell to process remaining/failed chunks:
raise SystemExit(0)

fnames = ["temp(1).fasta"]

print('\n====================================================================')
cwd = os.getcwd()
bat = '"' + cwd + '\\temp\\rpsblast.bat"'

for file in fnames:
    Tc = time.ctime().split(' ')[3]
    print('\nProcessing ' + file + ' at ' + Tc + '...')
    fname = "temp\\" + file
    T = time.time()
    out = fname.replace('.fasta','.xml')
    
    batch = ('cd "C:\\Users\\Public\\Documents\\Google Drive\\Python\\Standalone RPS-blast"' +
            '\nrpsblast -query ' + fname + ' -evalue 0.01' +
            ' -seg no -outfmt 5 -db db\\Cdd -out ' + out)
    with open('temp\\rpsblast.bat','w') as b:
        b.write(batch)
        b.close()
    os.system(bat)
    
    Tp = HMS(time.time() - T)
    time.sleep(5)
    m = psutil.virtual_memory()
    ram = str(m.percent) + '%'
    cpu = str(psutil.cpu_percent()) + '%'
    
    
    print('\n' + file + ' processed in ' + Tp + ' Hrs')
    print('\nCPU: ' + cpu + '    RAM: ' + ram)
    print('------------------------------------------------------------------')