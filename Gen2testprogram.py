#Second Generation Beacon Decode Program
import Gen2secondgen as Gen2
import csv
import decodefunctions as Func1
import Gen2functions as Func2


bins = Func2.hex2bin('99340039A3DC00000000001C60CE8C8A024BFFC0100C198096C')
print bins

newhex = Func2.bin2hex('001001100100110100000000000011100110100011110111000000000000000000000000000000000000000000000111000110000011001110100011001000101000000010010010111111111111000000000100000000110000011001100000001001011011')
print newhex


# Ask for the number and store it in userInput
userInput = raw_input('Please enter TAC: ')

try:
    tac = int(userInput)
# Catch the exception if the input was not a number
except ValueError:
    tac = 0
else:
    bits_tac = Func1.dec2bin(tac).zfill(20)


print tac


serialnum = Func1.dec2bin(573).zfill(10)
countrycode = Func1.dec2bin(201).zfill(10)
status = '1'
selftest = '1'
cancel = '0'
#lat = '0' + Func1.dec2bin(35).zfill(7) + Func1.dec2bin(77158).zfill(15)
#print Func2.getlatitude(lat)
lat = '00110000011001110100011'
lon = '001000101000000010010010'

maininfo = bits_tac + serialnum + countrycode + status + selftest + cancel + lat + lon

print len(maininfo)

vesselid = '0' * 64

print len(vesselid)

rotatingid = '0000'
elapsedtime = '000001'
timefromlastloc = '00000000110'
altitude = '0000110011'
dop = '00000001'
automated = '00'
battery = '101'
gnss = '10'
spare = '00'

rotatingfield = rotatingid + elapsedtime + timefromlastloc + altitude + dop + automated + battery + gnss + spare
print len(rotatingfield)

testbits = '00' + maininfo + vesselid + rotatingfield

print testbits
print len(testbits)

testhex = Func2.bin2hex(testbits)
print testhex
print len(testhex)
#print newBeacon2.bits
#print len(newBeacon2.bits)
#print len(hex2)
#print newBeacon2.tablebin
#print newBeacon2.beaconHexID
#print len(newBeacon2.beaconHexID)

#with open('test_file.csv', 'w') as csvfile:
    #writer = csv.writer(csvfile)
    #[writer.writerow(r) for r in newBeacon1.tablebin]
