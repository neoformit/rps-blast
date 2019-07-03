# Maybe try threading to see if speeds up?
# Bite 2000 seq chunks out of proteome and save as temp(x).fa
# Make call to rpsblast through batch file
# Iterate through chunks, logging time.

import os
import time
import math
import psutil
import datetime
from fasta import fasta_read, fasta_write

Class TimeMe(self):
    """ Times a process and prints out a time/resource report.
    Takes the keyword error which will be printed in output if truthy. """
    def __init__(self, fname):
        self.t0 = time.time()
        self.fname = fname
        print('\n\n\n')
        print('=============================================================\n')
        print('Processing file %s...\n')
        print('-------------------------------------------------------------\n')

    def end(self, error=False):
        td = self.HMS(time.time() - self.t0)
        time.sleep(2)
        mem = psutil.virtual_memory()
        ram = str(mem.percent) + '%'
        cpu = str(psutil.cpu_percent()) + '%'
        if error:
            print('Chunk %s failed after %s Hrs' % (self.fname, td))
            print('\nCPU: %s    RAM: %s' % (cpu, ram))
            print('Error message:\n%s' % error)
        else:
            print('Chunk %s processed in %s Hrs' % (fname, td))
            print('\nCPU: %s    RAM: %s' % (cpu, ram))
        print('=============================================================\n')

    def HMS(self,ts):
        sec = round(ts,2)
        tStr = str(datetime.timedelta(seconds=sec))
        if '.' in tStr:
            t = tStr.split('.')
            tStr = t[0] + '.' + t[1][:2]
            return tStr
        else:
            return tStr


def fasta_chunks(fname, chunk_size=5000):
    """ Split fasta into chunks and save (free up ram during run) """
    fas = fasta_read(fname)
    no_chunks = math.ceil(len(fas) / chunk_size)
    # Iterate over chunk numbers
    for i in range(no_chunks):
        i+=1
        if len(fas) >= chunk_size:
            # Take first 5k elements
            chunk = dict(list(fas.items())[:chunk_size])
        else:
            # Else take all elements
            chunk = fas
        fasta_write(chunk,"temp/chunk_%s" % i)
        print("Chunk %s written to /temp" % i)


# Run chunks
#%%============================================================================
# Should take about 23:30 min per 5000 seq chunk(approx 20 hours for 50 chunks)

def rpsblast_chunks():
    """ Iterates over files in chunks/ and tries to rpsblast them. If
    successful the chunkfile is removed. Otherwise file will remain to be
    re-chunked and run again. """
    chunk_files = os.listdir('temp')
    for fname in chunk_files:
        outfile = 'rps_xml/' + fname.replace('.fasta','.xml')
        t = TimeMe(fname)

        args = [
                "./rps-kit/rpsblast",
                "-query", fname,
                "-evalue", "0.01",
                "-seg", "no",
                "-outfmt", 5,
                "-db", "db/Cdd",
                "-out", outfile
        ]

        rps = subprocess.run(args, stderr=subprocess.PIPE)
        t.end(rps)

        if not rps:
            # Make sure python has finished closing to avoid PermissionError
            time.sleep(2)
            try:
                os.remove(fname)
            except PermissionError:
                print('!!! PermissionError removing %s' % fname)

# Process error chunks??

if __name__ == '__main__':

    fas = input('Enter name of fasta file: ')
    fasta_chunks(fname)
    rpsblast_chunks()
