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
print 'You entered: ' + str(Func2.bin2dec(bits_tac))


##BIT 21-30 Serial Number
userInput = raw_input('Please enter serial number: ')
try:
    serialnum = int(userInput)
except ValueError:
    serialnum = 0
else:
    bits_serialnum = Func1.dec2bin(serialnum).zfill(10)
print 'You entered: ' + str(Func2.bin2dec(bits_serialnum))


##BIT 31-40 Country code
userInput = raw_input('Please enter country code: ')
try:
    countrycode = int(userInput)
except ValueError:
    countrycode = 0
else:
    bits_countrycode = Func1.dec2bin(countrycode).zfill(10)
print 'You entered: ' + str(countrycode) + ' ' +Func2.countryname(countrycode)


##BIT 41 Status of homing device
userInput = raw_input('Please enter homing status (1 or 0): ')
try:
    status = int(userInput)
except ValueError:
    status = 0
else:
    bits_status = str(status)
print 'You entered: ' + Func2.homingStatus(bits_status)


##BIT 42 Self-test function
userInput = raw_input('Please enter self-test status (1 or 0): ')
try:
    selftest = int(userInput)
except ValueError:
    selftest = 0
else:
    bits_selftest = str(selftest)
print 'You entered: ' + Func2.selfTest(bits_selftest)


##BIT 43 User cancellation
userInput = raw_input('Please enter user cancellation status (1 or 0): ')
try:
    cancel = int(userInput)
except ValueError:
    cancel = 0
else:
    bits_cancel = str(cancel)
print 'You entered: ' + str(bits_cancel)


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

print 'You entered: ' + Func2.getlatitude(bits_latitude)[0]


##BIT 67-90 Longitude
userInput = raw_input('Please enter E/W flag (0 for east or 1 for west): ')
try:
    ewflag = int(userInput)
except ValueError:
    neflag = 0
else:
    bits_longitude = str(ewflag)

userInput = raw_input('Please enter longitude in degrees: ')
try:
    lon_degrees = float(userInput)
except ValueError:
    lon_degrees = 0
else:
    bits_longitude = bits_longitude + Func2.encodeLongitude(lon_degrees)

print 'You entered: ' + Func2.getlongitude(bits_longitude)[0]



################################
#                              #
#  BIT 91-137 VESSEL ID FIELD  #
#                              #
################################
userInput = raw_input('Please enter a vessel ID between 0 and 7: ')
try:
    vesselID = int(userInput)
except ValueError:
    vesselID = 0
else:
    bits_vesselID = Func1.dec2bin(vesselID).zfill(3)


##############################################
# Vessel 0: No aircraft or maritime identity #
##############################################
if vesselID == 0:
    vessel_bits = bits_vesselID + ('0' * 44)


###########################
# Vessel 1: Maritime MMSI #
###########################
elif vesselID == 1:
    userInput = raw_input('Please enter the 6 digit unique vessel number: ')
    try:
        ship_ID = int(userInput)
    except ValueError:
        ship_ID = 0
    else:
        bits_vesselID = Func1.dec2bin(ship_ID + (countrycode * 100000)).zfill(30)

    userInput = raw_input('Please enter the 4 digit MMSI of the EPIRB-AIS system: ')
    try:
        mmsi = int(userInput)
    except ValueError:
        mmsi = 0
    else:
        bits_mmsi = Func1.dec2bin(mmsi).zfill(7)

#############################
# Vessel 2: Radio Call Sign #
#############################

#########################################################
# Vessel 3: Aricraft Registration Marking (Tail Number) #
#########################################################

##############################################
# Vessel 4: Aircraft Aviation 24 Bit Address #
##############################################

#################################################
# Vessel 5: Aircraft Operator and Serial Number #
#################################################

##########################
# Other Vessel IDs Spare #
##########################


##BIT 138-154 Spare bits [137-153]
bits_spare = '1' * 17

bits_maininfo = bits_tac + bits_serialnum + bits_countrycode + bits_status + bits_selftest + bits_cancel + bits_latitude + bits_longitude + vessel_bits + bits_spare

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

testbits = bits_maininfo + vesselid + rotatingfield

print testbits
print len(testbits)

testhex = Func2.bin2hex('00' + testbits)
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
