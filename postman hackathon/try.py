import linecache
assembly_num = linecache.getline('ECI _ Voter Information.html', 213).replace('<', '>').split('>')[2]
sn = linecache.getline('ECI _ Voter Information.html', 287).replace('<', '>').split('>')[2]
pn = int(linecache.getline('ECI _ Voter Information.html', 272).replace('<', '>').split('>')[2])

print(assembly_num)
print(sn)
print(''.join(assembly_num.split(' ')[: : -1]).strip())