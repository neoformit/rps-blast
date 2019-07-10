import os
import datetime
from .rpsblast import fasta_chunks, rpsblast_chunks
from .rpsbproc import rpsbproc
from .parseout import parse, combine

def domains(exp_id):
    """ Runs rps-blast over a whole proteome by iterating over chunks.
    Formats the output using rpsbproc and then parses the output into a
    single csv file ready for data import. Should process approximately
    15k sequences per core per hour. Expects a proteome <exp_id>.fa to
    be present in the rps-blast directory. """

    fname = exp_id + '.fa'

    # Should probably start by flushing out all the temp folders
    flush = (
            ['temp/' + x for x in os.listdir('temp')]
            + ['xml/' + x for x in os.listdir('xml')]
            + ['out/' + x for x in os.listdir('out')]
            + ['csv/' + x for x in os.listdir('csv')]
    )

    # And also log files
    logfiles = [x for x in os.listdir() if x[-4:] == '.log']
    flush += logfiles

    for fpath in flush:
        # if this fails would probably cross-contaminate data... BAD
        try:
            os.remove(fpath)
        except PermissionError:
            raise PermissionError("Failure flushing temp file %s" % fpath)

    # Break proteome into managable chunks
    chunk_num = fasta_chunks(fname, chunk_size=50)
    # RPS-BLAST over those chunks
    rpsblast_chunks()

    # If a temp (chunk) file remains then an error occurred  with that chunk
    #   - will need to debug if/when that happens...
    assert not os.listdir('temp'), (
            "Unprocessed temp files remain after rpsblast.")
    # There should now be files in rps_xml directory
    assert os.listdir('xml'), (
            "rpsblast finished without producing any output.")
    rpsbproc()

    # Same again...
    assert not os.listdir('xml'), (
            "Unprocessed .xml files remain after rpsbproc.")
    assert os.listdir('out'), (
            "rpsbproc finished without producing any outfile output.")
    parse()

    # And again...
    assert not os.listdir('out'), (
            "Unprocessed .out files remain after parsing.")
    assert os.listdir('csv'), (
            "Outfile parsing finished without producing any csv output.")
    combine(exp_id, chunk_num)

    # Check error log and report
    try:
        with open('error.log','r') as r:
            errors = r.read()
            assert not errors, (
                # Should also notify admin at this point
                "RPS-BLAST finished with critical errors:\n" + errors)
    except FileNotFoundError:
        pass

    with open('rps.log') as l:
        l.write('Domain prediction complete at %s' % format(datetime.datetime.now(),'%H:%M:%S'))


if __name__ == "__main__":
    exp_id = "TRL_500"
    domains(exp_id)
