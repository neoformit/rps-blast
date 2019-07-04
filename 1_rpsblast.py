# Bite 5000 seq chunks out of proteome and save as chunk(x).fas
# Make calls to rpsblast
# Iterate through chunks, logging time.

import os
import time
import math
import psutil
import datetime
import subprocess
from fasta import fasta_read, fasta_write

class TimeMe:

    """ Times a process and prints out a time/resource report.
    Takes the keyword error which will be printed in output if truthy. """

    def __init__(self, fname):

        self.LOGFILE = 'rps.log'

        self.t0 = time.time()
        self.fname = fname
        t = format(datetime.datetime.now(), "%H:%M:%S")
        self.log('\n\n\n')
        self.log(t)
        self.log('=============================================================\n')
        self.log('Running RPS-BLAST on %s...\n' % fname)
        self.log('-------------------------------------------------------------\n')

    def end(self, error=False):
        td = self.HMS(time.time() - self.t0)
        time.sleep(2)
        mem = psutil.virtual_memory()
        ram = str(mem.percent) + '%'
        cpu = str(psutil.cpu_percent()) + '%'
        if error:
            self.log('Chunk %s failed after %s Hrs' % (self.fname, td))
            self.log('\nCPU: %s    RAM: %s' % (cpu, ram))
            self.log('Error message:\n%s' % error)
        else:
            self.log('Chunk %s processed in %s Hrs' % (self.fname, td))
            self.log('\nCPU: %s    RAM: %s' % (cpu, ram))
        self.log('=============================================================\n')

    def HMS(self,ts):
        sec = round(ts,2)
        return format(datetime.timedelta(seconds=sec),"%H:%M:%S")
    
    def log(self,msg):
        with open(self.LOGFILE, 'a+') as f:
            f.write('\n' + msg)


def log(msg):
    LOGFILE = 'rps.log'
    with open(LOGFILE, 'a+') as f:
        f.write('\n' + msg)


def fasta_chunks(fname, chunk_size=5000):
    """ Split fasta into chunks and save (free up ram during run) """
    fas = fasta_read(fname)
    no_chunks = math.ceil(len(fas) / chunk_size)
    # Iterate over chunk numbers
    for i in range(no_chunks):
        i+=1
        if len(fas) > chunk_size:
            # Take first 5k elements
            chunk = dict(list(fas.items())[:chunk_size])
            fas = dict(list(fas.items())[chunk_size:])
        else:
            # Else take all elements
            chunk = fas
        fasta_write(chunk,"temp/chunk_%s.fas" % i)
        self.log("Chunk %s written to /temp" % i)


# Run chunks
#%%============================================================================
# Should take about 23:30 min per 5000 seq chunk(approx 20 hours for 50 chunks)

def rpsblast_chunks():
    """ Iterates over files in chunks/ and tries to rpsblast them. If
    successful the chunkfile is removed. Otherwise file will remain to be
    re-chunked and run again. """
    chunk_files = os.listdir('temp')
    chunk_files.sort()
    for fname in chunk_files:
        fpath = 'temp/' + fname
        outfile = 'rps_xml/' + fname.replace('.fas','.xml')
        t = TimeMe(fname)

        args = [
                "./rps-kit/rpsblast",
                "-query", fpath,
                "-evalue", "0.01",
                "-seg", "no",
                "-outfmt", '5',
                "-db", "rps-kit/db/Cdd",
                "-out", outfile
        ]

        rps = subprocess.run(args, stderr=subprocess.PIPE)
        t.end(rps.returncode)

        if not rps.returncode:
            # Make sure python has finished closing to avoid PermissionError
            time.sleep(2)
            try:
                os.remove(fpath)
            except PermissionError:
                print('!!! PermissionError removing %s' % fname)

# Process error chunks??

if __name__ == '__main__':

    fname = 'TRL.fa'
    if fname:
        rpsblast_chunks()
