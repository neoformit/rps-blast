import os
import pandas as pd
from rpsblast import log

def parse():
    """ Parse rpsbproc outfile to csv """
    outfiles = os.listdir('out')

    for fname in outfiles:
        copy = False
        base = fname.replace('.out','')
        fpath = 'out/' + fname

        r = open(fpath ,'r')
        w = open('csv/' + base + '.csv','w')

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
                    domain = line[9].split(',')[0]
                    start = line[4]
                    stop = line[5]
                    e = line[6]
                    bits = line[7]
                    accession = line[8]
                    trunc = line[10]

                    data = [domain,start,stop,e,bits,trunc,accession]
                    cdData[query].append(data)

        w.write(','.join([
                'contig_id','name','start','stop',
                'evalue','bitscore','truncated','accession'
                ]) + '\n'
        )

        for key, doms in cdData.items():
            for d in doms:
                w.write(",".join([key] + d) + '\n')

        r.close()
        w.close()
        try:
            os.remove(fpath)
        except PermissionError:
            log('!!! PermissionError removing %s' % fname, error=True)


def combine(exp_id, chunk_num):
    """ Combine all csvs into one. """

    # Check final csv count matches original chunk count (avoid oopsies...)
    csvs = os.listdir('csv')
    assert chunk_num == len(csvs), "Final chunk number does not equal initial"
    cols = ['contig_id','name','start','stop',
            'evalue','bitscore','truncated','accession']
    dfm = pd.DataFrame(columns=cols)

    for c in csvs:
        print('Reading in %s' % c)
        cpath = 'csv/' + c
        df = pd.read_csv(cpath)
        dfm = dfm.append(df)
        try:
            print('written successfully') # os.remove(cpath)
        except PermissionError:
            log('!!! PermissionError removing %s' % c, error=True)


    fname = exp_id + '.csv'
    dfm.to_csv(fname, index=False)
    return locals()
