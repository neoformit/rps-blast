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

cwd = os.getcwd()
bat = '"' + cwd + '\\temp\\rpsblast.bat"'

file = '"downregulated.fa"'
out = file.replace('.fa','.xml')
Tc = time.ctime().split(' ')[-2]
print('\nProcessing started at ' + Tc + '...')
T = time.time()

batch = ('cd "C:\\Users\\Public\\Documents\\Google Drive\\Python\\Standalone RPS-blast"' +
        '\nrpsblast -query ' + file + ' -evalue 0.01' +
        ' -seg no -outfmt 5 -db db\\Cdd -out ' + out)
with open('temp\\rpsblast.bat','w') as b:
    b.write(batch)
    b.close()
os.system(bat)

Tp = HMS(time.time() - T)
time.sleep(1)
m = psutil.virtual_memory()
ram = str(m.percent) + '%'
cpu = str(psutil.cpu_percent()) + '%'


print('\nProcessed in ' + Tp + ' Hrs')
print('\nCPU: ' + cpu + '    RAM: ' + ram)
print('------------------------------------------------------------------')