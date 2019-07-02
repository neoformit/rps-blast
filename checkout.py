def find_dupes(L):
    L.sort()
    dupes = []
    lastitem=''
    for item in L:
        if lastitem == item:
            dupes.append(item)
        lastitem = item
    return dupes

i=0

names = []

while True:
    i+=1
    try:
        r = open('temp\\temp(' + str(i) + ').fasta','r')
    except FileNotFoundError:
        break
    for line in r:
        if line[0] == '>':
            name = line[1:].replace('\n','')
            names.append(name)
    r.close()

duplicates = find_dupes(names)