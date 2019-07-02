import os
import time
from os import walk

wd = 'C:\\Users\\Public\\Documents\\Google Drive\\Python\\Standalone RPS-blast\\rps_xml'
fnames = []

for root, dirs, files in walk(wd):
    for file in files:
        if '.xml' in file:
            fnames.append(file)

cwd = os.getcwd()
bat = '"' + cwd + '\\rps_xml\\rpsbproc.bat"'

for file in fnames:
    Tc = time.ctime().split(' ')[3]
    print('\n================================================================')
    print('\nProcessing ' + file + ' at ' + Tc + '...')
    fpath = 'rps_xml\\' + file
    out = fpath.replace('.xml','.out')
    batch = ('cd "C:\\Users\\Public\\Documents\\Google Drive\\Python\\Standalone RPS-blast"' +
            '\nrpsbproc -q -i ' + fpath + ' -o ' + out)
    with open('rps_xml\\rpsbproc.bat','w') as b:
        b.write(batch)
        b.close()
    os.system(bat)