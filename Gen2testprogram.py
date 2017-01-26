#Second Generation Beacon Decode Program
import Gen2secondgen as Gen2
import csv
import Gen2functions as Func


print Func.getlatitude('00110000011001110100011')
print Func.getlongitude('001000101000000010010010')
print Func.getlatitude('00100011110001011000011')

#print newBeacon2.bits
#print len(newBeacon2.bits)
#print len(hex2)
#print newBeacon2.tablebin
#print newBeacon2.beaconHexID
#print len(newBeacon2.beaconHexID)

#with open('test_file.csv', 'w') as csvfile:
    #writer = csv.writer(csvfile)
    #[writer.writerow(r) for r in newBeacon1.tablebin]
