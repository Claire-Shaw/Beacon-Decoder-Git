#Second Generation Beacon Decode Program
import Gen2secondgen as Gen2
import csv
import Gen2functions as Func


bins = Func.hex2bin('99340039A3DC00000000001C60CE8C8A024BFFC0100C198096C')
print bins

newhex = Func.bin2hex('001001100100110100000000000011100110100011110111000000000000000000000000000000000000000000000111000110000011001110100011001000101000000010010010111111111111000000000100000000110000011001100000001001011011')
print newhex

#print newBeacon2.bits
#print len(newBeacon2.bits)
#print len(hex2)
#print newBeacon2.tablebin
#print newBeacon2.beaconHexID
#print len(newBeacon2.beaconHexID)

#with open('test_file.csv', 'w') as csvfile:
    #writer = csv.writer(csvfile)
    #[writer.writerow(r) for r in newBeacon1.tablebin]
