import os
import time
import math
import psutil
import datetime
import subprocess
from fasta import fasta_read, fasta_write

class TimeMe:

    """ Times a process and prints out a time/resource report.
    Takes kwarg 'error' which is logged if truthy. """

    def __init__(self, fname, process='RPS-BLAST'):

        self.LOGFILE = 'rps.log'

        self.t0 = time.time()
        self.fname = fname
        t = format(datetime.datetime.now(), "%H:%M:%S")
        self.log('\n\n\n')
        self.log(t)
        self.log('=============================================================\n')
        self.log('Running %s on %s...\n' % (process,fname))
        self.log('-------------------------------------------------------------\n')

    def end(self, error=False):
        td = self.HMS(time.time() - self.t0)
        time.sleep(2)
        mem = psutil.virtual_memory()
        ram = str(mem.percent) + '%'
        cpu = str(psutil.cpu_percent()) + '%'
        if error:
            self.log('Chunk %s failed after %s Hrs' %
                    (self.fname, td), error=True)
            self.log('\nCPU: %s    RAM: %s' % (cpu, ram), error=True)
            self.log('Error message:\n%s' % error, error=True)
        else:
            self.log('Chunk %s processed in %s Hrs' % (self.fname, td))
            self.log('\nCPU: %s    RAM: %s' % (cpu, ram))
        self.log('=============================================================\n')

    def HMS(self,ts):
        sec = round(ts,2)
        return str(datetime.timedelta(seconds=sec))

    def log(self,msg, error=False):
        with open(self.LOGFILE, 'a+') as f:
            f.write('\n' + msg)


def log(msg, error=False):
    LOGFILE = 'rps.log'
    ERRORFILE = 'error.log'
    with open(LOGFILE, 'a+') as f:
        f.write(msg + '\n')
    if error:
        with open(ERRORFILE, 'a+') as f:
            f.write(msg + '\n')


def fasta_chunks(fname, chunk_size=5000):
    """ Split fasta into chunks and save (free up ram during run). For
    continuity, a list of contig_ids and chunk numbers are pickled for
    back-checking at the end of the process with checkout.py. """
    fas = fasta_read(fname)
    chunk_num = math.ceil(len(fas) / chunk_size)

    # Iterate over chunk numbers
    for i in range(chunk_num):
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

    return chunk_num


def rpsblast_chunks():
    """ Iterates over files in chunks/ and tries to rpsblast them. If
    successful the chunkfile is removed. Otherwise file will remain to be
    re-chunked and run again. """
    chunk_files = os.listdir('temp')
    chunk_files.sort()

    for fname in chunk_files:
        fpath = 'temp/' + fname
        outfile = 'xml/' + fname.replace('.fas','.xml')
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
            # Ensure python has finished closing to avoid PermissionError
            time.sleep(2)
            try:
                os.remove(fpath)
            except PermissionError:
                log('!!! PermissionError removing %s' % fname, error=True)


# In future add function here to re-process error chunks.
# Need errors to actually occur before that can be figured out!


if __name__ == '__main__':

    fname = 'TRL.fa'
    if fname:
        # fasta_chunks(fname)
        rpsblast_chunks()
