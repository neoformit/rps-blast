import os
from rpsblast import fasta_chunks, rps_chunks
from rpsbproc import rpsbproc
from parseout import parse, combine

def domains(exp_id):
    """ Runs rps-blast over a whole proteome by iterating over chunks.
    Formats the output using rpsbproc and then parses the output into a
    single csv file ready for data import. Should process approximately
    15k sequences per core per hour. Expects a proteome <exp_id>.fa to
    be present in the rps-blast directory. """

    fname = exp_id + '.fa'

    # Should probably start by flushing out all the temp folders
    flush = ['temp/' + x for x in os.listdir(temp)]
            + ['rps_xml/' + x for x in os.listdir(rps_xml)]
            + ['out/' + x for x in os.listdir(out)]
            + ['csv/' + x for x in os.listdir(csv)]

    for fpath in flush:
        # if this fails would probably cross-contaminate data... BAD
        try:
            os.remove(fpath)
        except PermissionError:
            raise PermissionError("Failure flushing temp file %s" % fpath)

    # Break proteome into managable chunks
    chunk_num = fasta_chunks(fname)
    # RPS-BLAST over those chunks
    rpsblast_chunks()

    # If a temp (chunk) file remains then an error occurred  with that chunk
    #   - will need to debug if/when that happens...
    assert not os.listdir(temp),
            "Unprocessed temp files remain after rpsblast."
    # There should now be files in rps_xml directory
    assert os.listdir(rps_xml),
            "rpsblast finished without producing any output."
    rpsbproc()

    # Same again...
    assert not os.listdir(rps_xml),
            "Unprocessed .xml files remain after rpsbproc."
    assert os.listdir(out),
            "rpsbproc finished without producing any outfile output."
    parse()

    # And again...
    assert not os.listdir(out),
            "Unprocessed .out files remain after parsing."
    assert os.listdir(csv),
            "Outfile parsing finished without producing any csv output."
    combine(exp_id, chunk_num)

    # Check error log and report
    with open('error.log','r') as r:
        errors = r.read()
        assert not errors,
            # Could also notify admin at this point
            "RPS-BLAST finished with critical errors:\n" + errors

if __name__ == "__main__":
    domains('TRL')
