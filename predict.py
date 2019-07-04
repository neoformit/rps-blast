import os
from 1_rpsblast import fasta_chunks, rps_chunks


def log(msg):
    with open('predict.log') as f:
        f.write('\n' + msg)


def domains(fname):

    if not os.listdir(temp):
        fasta_chunks(fname)

    rpsblast_chunks()

    # Check if chunks remain - indicates error
    # This needs to be incorporated into 1_rpsblast
    chunks_remain = os.listdir(temp)

    if chunks_remain:
        log("Some chunks failed to process:")
        log("\n".join(chunks_remain))

    # Rpsbproc 

    # Parse

    # Combine

if __name__ == "__main__":
    domains('TRL.fas')
