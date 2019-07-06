import os

csvs = os.listdir('csv')

for csv in csvs:
    csv = 'csv/' + csv
    new = open("1_%s" % csv,'w')
    with open(csv) as r:
        for line in r.read().splitlines():
            split = line.split(',')
            if len(split) > 8:
                n = len(split) - 8
                cid = [split[0]]
                data = split[n+1:]
                new.write(','.join(cid + data) + '\n')
            else:
                new.write(line + '\n')
    new.close()
