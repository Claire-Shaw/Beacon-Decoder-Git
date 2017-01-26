#Second Generation Beacon Decode Program
import secondgen as Gen2
import csv

hex1 = '1D2B422EE72CA23DFFD502B96C11BB3465EA99784BC8243D123'
hex2 = '4CCA439EAEDDD1CACC4333E82F953824C991E5912128BD43DDA'

newBeacon1 = Gen2.SecondGen(hex1)

newBeacon1.processHex()

newBeacon2 = Gen2.SecondGen(hex2)

newBeacon2.processHex()

print newBeacon1.bits
print len(newBeacon1.bits)
print len(hex1)

print newBeacon2.bits
print len(newBeacon2.bits)
print len(hex2)

with open('test_file.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    [writer.writerow(r) for r in newBeacon2.tablebin]
