#Second Generation Beacon Decode Program
import Gen2secondgen as Gen2
import csv
import decodefunctions as Func1
import Gen2functions as Func2


##BIT 1-20  Type Approval Certificate #
# Ask for the user input and store it in userInput
userInput = raw_input('Please enter TAC: ')
try:
    tac = int(userInput)
# Catch the exception if the input was not a number
except ValueError:
    tac = 0
else:
    bits_tac = Func1.dec2bin(tac).zfill(20)
print 'You entered ' + str(Func2.bin2dec(bits_tac))


##BIT 21-30 Serial Number
userInput = raw_input('Please enter serial number: ')
try:
    serialnum = int(userInput)
except ValueError:
    serialnum = 0
else:
    bits_serialnum = Func1.dec2bin(serialnum).zfill(10)
print 'You entered ' + str(Func2.bin2dec(bits_serialnum))


##BIT 31-40 Country code
userInput = raw_input('Please enter country code: ')
try:
    countrycode = int(userInput)
except ValueError:
    countrycode = 0
else:
    bits_countrycode = Func1.dec2bin(countrycode).zfill(10)
print 'You entered ' + str(countrycode) + ' ' +Func2.countryname(countrycode)


##BIT 41 Status of homing device
userInput = raw_input('Please enter homing status (1 or 0): ')
try:
    status = int(userInput)
except ValueError:
    status = 0
else:
    bits_status = str(status)
print 'You entered ' + str(bits_status)


##BIT 42 Self-test function
userInput = raw_input('Please enter self-test status (1 or 0): ')
try:
    selftest = int(userInput)
except ValueError:
    selftest = 0
else:
    bits_selftest = str(selftest)
print 'You entered ' + str(bits_selftest)


##BIT 43 User cancellation
userInput = raw_input('Please enter user cancellation status (1 or 0): ')
try:
    cancel = int(userInput)
except ValueError:
    cancel = 0
else:
    bits_cancel = str(cancel)
print 'You entered ' + str(bits_cancel)


##BIT 44-66 Latitude
userInput = raw_input('Please enter N/S flag (0 for north or 1 for south): ')
try:
    nsflag = int(userInput)
except ValueError:
    neflag = 0
else:
    bits_latitude = str(nsflag)

userInput = raw_input('Please enter latitude in degrees: ')
try:
    lat_degrees = float(userInput)
except ValueError:
    lat_degrees = 0
else:
    bits_latitude = bits_latitude + Func2.encodeLatitude(lat_degrees)

print 'You entered ' + Func2.getlatitude(bits_latitude)[0]


##BIT 67-90 Longitude
lon = '001000101000000010010010'

maininfo = bits_tac + bits_serialnum + bits_countrycode + bits_status + bits_selftest + bits_cancel + bits_latitude + lon

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
