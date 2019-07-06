import os
import time
import subprocess
from rpsblast import TimeMe, log

def rpsbproc():
    xmls = os.listdir('rps_xml')

    for xml in xmls:
        t = TimeMe(xml, process="rpsbproc")
        fpath = 'xml/' + xml
        out = 'out/' + xml.replace('.xml','.out')
        args = [
                "./rps-kit/rpsbproc",
                "-q",
                "-i", fpath,
                "-o", out
        ]
        run = subprocess.run(args, stderr=subprocess.PIPE)
        t.end(run.returncode)

        if not run.returncode:
            # Make sure python has finished closing to avoid PermissionError
            time.sleep(2)
            try:
                os.remove(fpath)
            except PermissionError:
                log('!!! PermissionError removing %s' % xml)

if __name__ == '__main__':
    rpsbproc()
