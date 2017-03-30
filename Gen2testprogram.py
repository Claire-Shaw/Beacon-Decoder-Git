#Second Generation Beacon Decode Program
import csv

import Gen2secondgen as Gen2
import decodefunctions as Func1
import Gen2functions as Func2
import definitions

next_step = False

##BIT 1-20  Type Approval Certificate #
# Ask for the user input and store it in userInput
while next_step == False:
    userInput = raw_input('\nPlease enter TAC (0 to 1,048,575): ')
    try:
        tac = int(userInput)
    # Catch the exception if the input was not a number
    except ValueError:
        print 'Error: value must be an integer'
        tac = 0
    else:
        bits_tac = Func1.dec2bin(tac).zfill(20)
        if len(bits_tac) != 20:
            print 'Error: input too high.'
        else:
            break
print 'You entered: ' + str(Func2.bin2dec(bits_tac))


##BIT 21-30 Serial Number
while next_step == False:
    userInput = raw_input('\nPlease enter serial number (0 to 1023): ')
    try:
        serialnum = int(userInput)
    except ValueError:
        print 'Error: value must be an integer'
        serialnum = 0
    else:
        bits_serialnum = Func1.dec2bin(serialnum).zfill(10)
        if len(bits_serialnum) != 10:
            print 'Error: input too high.'
        else:
            break
print 'You entered: ' + str(Func2.bin2dec(bits_serialnum))


##BIT 31-40 Country code
while next_step == False:
    userInput = raw_input('\nPlease enter country code: ')
    try:
        countrycode = int(userInput)
    except ValueError:
        print 'Error: value must be an integer'
        countrycode = 0
    else:
        bits_countrycode = Func1.dec2bin(countrycode).zfill(10)
        if len(bits_countrycode) != 10:
            print 'Error: input too high.'
        else:
            break
print 'You entered: ' + str(countrycode) + ' ' +Func2.countryname(countrycode)


##BIT 41 Status of homing device
while next_step == False:
    print '\nPlease enter homing status: '
    print '0: Beacon is not equipped with any homing signals or they have been deliberately disabled.  If beacon has been activated, no homing device is functional or it has been deliberately disabled'
    print '1: Beacon is equipped with at least one homing signal. If beacon has been activated, at least one homing device is functional and transmitting'
    userInput = raw_input()
    try:
        status = int(userInput)
    except ValueError:
        print 'Error: value must be an integer'
        status = 0
    else:
        bits_status = str(status)
        if len(bits_status) != 1:
            print 'Error: input too long.'
        elif not Func2.isBinary(bits_status):
            print 'Error: inavlid input'
        else:
            break
print 'You entered: ' + Func2.homing(bits_status)


##BIT 42 Self-test function
while next_step == False:
    print '\nPlease enter self-test status: '
    print '0: Self-test transmission'
    print '1: Normal beacon operation (transmitting a distress)'
    userInput = raw_input()
    try:
        selftest = int(userInput)
    except ValueError:
        print 'Error: value must be an integer'
        selftest = 0
    else:
        bits_selftest = str(selftest)
        if len(bits_selftest) != 1:
            print 'Error: input too long.'
        elif not Func2.isBinary(bits_selftest):
            print 'Error: inavlid input'
        else:
            break
print 'You entered: ' + Func2.selfTest(bits_selftest)


##BIT 43 User cancellation
while next_step == False:
    print '\nPlease enter user cancellation status: '
    print '0: Normal beacon operation (transmitting a distress or self-test message)'
    print '1: User cancellation message'
    userInput = raw_input()
    try:
        cancel = int(userInput)
    except ValueError:
        print 'Error: value must be an integer'
        cancel = 0
    else:
        bits_cancel = str(cancel)
        if len(bits_cancel) != 1:
            print 'Error: input too long.'
        elif not Func2.isBinary(bits_cancel):
            print 'Error: inavlid input'
        else:
            break
print 'You entered: ' + str(bits_cancel)


##BIT 44-66 Latitude
while next_step == False:
    print '\nPlease enter N/S flag: '
    print '0: North'
    print '1: South'
    userInput = raw_input()
    try:
        nsflag = int(userInput)
    except ValueError:
        print 'Error: value must be an integer'
        neflag = 0
    else:
        bits_latitude = str(nsflag)
        if len(bits_latitude) != 1:
            print 'Error: input too long.'
        elif not Func2.isBinary(bits_latitude):
            print 'Error: inavlid input'
        else:
            break

while next_step == False:
    userInput = raw_input('\nPlease enter latitude in degrees: ')
    try:
        lat_degrees = float(userInput)
    except ValueError:
        print 'Error: value must be an integer'
        lat_degrees = 0
    else:
        bits_lat_degrees = Func2.encodeLatitude(lat_degrees)
        if len(bits_lat_degrees) != 22:
            print 'Error: input too long.'
        elif not Func2.isBinary(bits_lat_degrees):
            print 'Error: inavlid input'
        else:
            bits_latitude = bits_latitude + bits_lat_degrees
            break

print 'You entered: ' + Func2.getlatitude(bits_latitude)[0]


##BIT 67-90 Longitude
while next_step == False:
    print '\nPlease enter E/W flag: '
    print '0: East'
    print '1: West'
    userInput = raw_input()
    try:
        ewflag = int(userInput)
    except ValueError:
        print 'Error: value must be an integer'
        ewflag = 0
    else:
        bits_longitude = str(ewflag)
        if len(bits_longitude) != 1:
            print 'Error: input too long.'
        elif not Func2.isBinary(bits_longitude):
            print 'Error: inavlid input'
        else:
            break

while next_step == False:
    userInput = raw_input('\nPlease enter longitude in degrees: ')
    try:
        lon_degrees = float(userInput)
    except ValueError:
        print 'Error: value must be an integer'
        lon_degrees = 0
    else:
        bits_lon_degrees = Func2.encodeLongitude(lon_degrees)
        if len(bits_lon_degrees) != 23:
            print 'Error: input too long.'
        elif not Func2.isBinary(bits_lon_degrees):
            print 'Error: inavlid input'
        else:
            bits_longitude = bits_longitude + bits_lon_degrees
            break
print 'You entered: ' + Func2.getlongitude(bits_longitude)[0]



################################
#                              #
#  BIT 91-137 VESSEL ID FIELD  #
#                              #
################################

while next_step == False:
    print '\nPlease enter a vessel ID: '
    print '0: No aircraft or maritime identity'
    print '1: Maritime MMSI'
    print '2: Radio Call Sign'
    print '3: Aricraft Registration Marking (Tail Number)'
    print '4: Aircraft Aviation 24 Bit Address'
    print '5: Aircraft Operator and Serial Number'
    print '6-7: Spare'
    userInput = raw_input()
    try:
        vesselID = int(userInput)
    except ValueError:
        print 'Error: value must be an integer'
        vesselID = 0
    else:
        bits_vesselID = Func1.dec2bin(vesselID).zfill(3)
        if len(bits_vesselID) != 3:
            print 'Error: input too long.'
        elif not Func2.isBinary(bits_vesselID):
            print 'Error: inavlid input'
        else:
            break


##############################################
# Vessel 0: No aircraft or maritime identity #
##############################################
if vesselID == 0:
    print '\nVessel 0: No aircraft or maritime identity'

    vessel_bits = bits_vesselID + ('0' * 44)


###########################
# Vessel 1: Maritime MMSI #
###########################
elif vesselID == 1:
    print '\nVessel 1: Maritime MMSI'

    while next_step == False:
        userInput = raw_input('\nPlease enter the 6 digit unique vessel number. If there is no MMSI available, enter 111111: ')
        try:
            ship_ID = int(userInput)
        except ValueError:
            print 'Error: value must be an integer'
            ship_ID = 0
        else:
            if ship_ID == 111111:
                bits_shipID = Func1.dec2bin(ship_ID).zfill(30)
                break
            else:
                bits_shipID = Func1.dec2bin(ship_ID + (countrycode * 100000)).zfill(30)
                if len(bits_shipID) != 30:
                    print 'Error: input too long.'
                elif not Func2.isBinary(bits_shipID):
                    print 'Error: inavlid input'
                else:
                    break

    while next_step is False:
        userInput = raw_input('\nPlease enter the 4 digit MMSI of the EPIRB-AIS system. If there is no EPIRB-AIS system, enter 10922: ')
        try:
            mmsi = int(userInput)
        except ValueError:
            print 'Error: value must be an integer'
            mmsi = 0
        else:
            bits_mmsi = Func1.dec2bin(mmsi).zfill(14)
            if len(bits_mmsi) != 14:
                print 'Error: input too long.'
            elif not Func2.isBinary(bits_mmsi):
                print 'Error: inavlid input'
            else:
                break

    vessel_bits = bits_vesselID + bits_shipID + bits_mmsi


#############################
# Vessel 2: Radio Call Sign #
#############################
elif vesselID == 2:
    print '\nVessel 2: Radio Call Sign'

    while next_step is False:
        callsign = raw_input('\nPlease enter the 7 character radio call sign: ')
        if len(callsign) != 7:
            print 'Error: call sign must be 7 characters'
        callsign_bits = Func2.str2baudot(callsign).zfill(42)
        if len(callsign_bits) != 42:
            print 'Error: input too long.'
        elif not Func2.isBinary(callsign_bits):
            print 'Error: inavlid input'
        else:
            break

    print 'You entered: ' + Func2.getCallsign(callsign_bits)

    vessel_bits = bits_vesselID + callsign_bits + '00'


#########################################################
# Vessel 3: Aricraft Registration Marking (Tail Number) #
#########################################################
elif vesselID == 3:
    print '\nVessel 3: Aricraft Registration Marking (Tail Number)'

    while next_step is False:
        tailnum = raw_input('\nPlease enter the 7 character tail number: ')
        if len(tailnum) != 7:
            print 'Error: tail number must be 7 characters'
        tailnum_bits = Func2.str2baudot(tailnum).zfill(42)
        if len(tailnum_bits) != 42:
            print 'Error: input too long.'
        elif not Func2.isBinary(tailnum_bits):
            print 'Error: inavlid input'
        else:
            break

    print 'You entered: ' + Func2.getTailNum(tailnum_bits)

    vessel_bits = bits_vesselID + tailnum_bits + '00'


##############################################
# Vessel 4: Aircraft Aviation 24 Bit Address #
##############################################
elif vesselID == 4:
    print '\nVessel 4: Aircraft Aviation 24 Bit Addres'

    while next_step is False:  
        userInput = raw_input('\nPlease enter the 24 bit aviation address in integer format: ')
        try:
            aviation_address = int(userInput)
        except ValueError:
            print 'Error: value must be an integer'
            aviation_address = 0
        else:
            bits_aviation_address = Func1.dec2bin(aviation_address).zfill(24)
            if len(bits_aviation_address) != 24:
                print 'Error: input too long.'
            elif not Func2.isBinary(bits_aviation_address):
                print 'Error: inavlid input'
            else:
                break

    print 'You entered: ' + str(Func1.bin2dec(bits_aviation_address))

    vessel_bits = bits_vesselID + bits_aviation_address + ('0' * 20)


#################################################
# Vessel 5: Aircraft Operator and Serial Number #
#################################################
elif vesselID == 5:
    print '\nVessel 5: Aircraft Operator and Serial Number'

    while next_step is False: 
        operator = raw_input('\nPlease enter 3-letter aircraft operator designator: ')
        if len(operator) != 3:
            print 'Error: aircraft operator designator must be 3 characters'
        else:
            operator_bits = Func2.str2baudot(operator).zfill(18)
            break
    print 'You entered: ' + Func2.baudot2str(operator_bits, 3)

    while next_step is False:
        userInput = raw_input('\nPlease enter the serial number (1 to 4095) as designated by the aircraft operator: ')
        try:
            aircraft_serialnum = int(userInput)
        except ValueError:
            print 'Error: value must be an integer'
            aircraft_serialnum = 0
        else:
            if aircraft_serialnum > 4095 or aircraft_serialnum < 1:
                print 'Error: invalid serial number'
            else:
                bits_aircraft_serialnum = Func1.dec2bin(aircraft_serialnum).zfill(12)
                break
    print 'You entered: ' + str(Func1.bin2dec(bits_aircraft_serialnum))

    vessel_bits = bits_vesselID + operator_bits + bits_aircraft_serialnum + ('1' * 14)


##########################
# Other Vessel IDs Spare #
##########################
else:
    print '\nOther Vessel IDs Spare'

    vessel_bits = bits_vesselID + ('0' * 44)


##BIT 138-154 Spare bits [137-153]
bits_spare = '1' * 17



#48 BIT ROTATING FIELD
while next_step is False:
    print '\nPlease enter a rotating ID: '
    print '0: C/S G.008 Objective Requirements'
    print '1: Inflight Emergency'
    print '2: RLS'
    print '3: National Use'
    print '4-14: Spare'
    print '15: Cancellation Message'
    userInput = raw_input()
    try:
        rotatingID = int(userInput)
    except ValueError:
        print 'Error: value must be an integer'
        rotatingID = 0
    else:
        if rotatingID > 15 or rotatingID < 0:
            print 'Error: Invalid rotating ID'
        else:
            bits_rotatingID = Func1.dec2bin(rotatingID).zfill(4)
            break


##############################################################
# Rotating Field Type: C/S G.008 Objective Requirements (#0) #
##############################################################
if rotatingID == 0:
    print '\nRotating Field Type: C/S G.008 Objective Requirements (#0)'
    bits_rotating0 = bits_rotatingID

    ##BIT 5-10 (159-164) Elapsed time since activation (0 to 63 hours in 1 hour steps)
    while next_step is False:
        userInput = raw_input('\nPlease enter elapsed time since activation (0 to 63 hours): ')
        try:
            elapsed_time = int(userInput)
        except ValueError:
            print 'Error: value must be an integer'
            elapsed_time = 0
        else:
            if elapsed_time > 63 or elapsed_time < 0:
                print 'Error: invalid time'
            else:
                bits_elapsed_time = Func1.dec2bin(elapsed_time).zfill(6)
                break
    print 'You entered: ' + str(Func1.bin2dec(bits_elapsed_time)) + ' hours'

    bits_rotating0 += bits_elapsed_time

    ##BIT 11-21 (165-175) Time from last encoded location (0 to 2047 minutes in 1 minute steps)
    while next_step is False:
        userInput = raw_input('\nPlease enter time from last encoded location (0 to 2047 minutes): ')
        try:
            last_encoded_loc = int(userInput)
        except ValueError:
            print 'Error: value must be an integer'
            last_encoded_loc = 0
        else:
            if last_encoded_loc < 0 or last_encoded_loc > 2047:
                print 'Error: invalid time'
            else:
                bits_last_encoded_loc = Func1.dec2bin(last_encoded_loc).zfill(11)
                break
    print 'You entered: ' + str(Func1.bin2dec(bits_last_encoded_loc)) + ' minutes'

    bits_rotating0 += bits_last_encoded_loc


    ##BIT 22-31 (176-185) Altitude of encoded location
    while next_step is False:
        userInput = raw_input('\nPlease enter altitude in metres: ')
        try:
            altitude = int(userInput)
        except ValueError:
            print 'Error: value must be an integer'
            altitude = 0
        else:
            bits_altitude = Func1.dec2bin(int((altitude + 400)/16)).zfill(10)
            if len(bits_altitude) != 10:
                print 'Error: input too long.'
            elif not Func2.isBinary(bits_altitude):
                print 'Error: inavlid input'
            else:
                break
    print 'You entered: ' + str(Func2.getaltitude(bits_altitude))

    bits_rotating0 += bits_altitude


    ##BIT 32-39 (186-193) Dilution of precision
    while next_step is False:
        userInput = raw_input('\nPlease enter Horizontal Dilution of Precision. If HDOP not available, enter 1111: ')
        try:
            hdop = int(userInput)
        except ValueError:
            print 'Error: value must be an integer'
            hdop = 1111
        else:
            if hdop == 1111:
                bits_hdop = '1111'
            elif hdop <= 1:
                bits_hdop = '0000'
            elif hdop > 1 and hdop <= 2:
                bits_hdop = '0001'
            elif hdop > 2 and hdop <= 3:
                bits_hdop = '0010'
            elif hdop > 3 and hdop <= 4:
                bits_hdop = '0011'
            elif hdop > 4 and hdop <= 5:
                bits_hdop = '0100'
            elif hdop > 5 and hdop <= 6:
                bits_hdop = '0101'
            elif hdop > 6 and hdop <= 7:
                bits_hdop = '0110'
            elif hdop > 7 and hdop <= 8:
                bits_hdop = '0111'
            elif hdop > 8 and hdop <= 10:
                bits_hdop = '1000'
            elif hdop > 10 and hdop <= 12:
                bits_hdop = '1001'
            elif hdop > 12 and hdop <= 15:
                bits_hdop = '1010'
            elif hdop > 15 and hdop <= 20:
                bits_hdop = '1011'
            elif hdop > 20 and hdop <= 30:
                bits_hdop = '1100'
            elif hdop > 30 and hdop <= 50:
                bits_hdop = '1101'
            else:
                bits_hdop = '1110'
            break
    print 'You entered: H' + Func2.getDOP(bits_hdop)

    bits_rotating0 += bits_hdop

    while next_step is False:
        userInput = raw_input('\nPlease enter Vertical Dilution of Precision. If VDOP not available, enter 1111: ')
        try:
            vdop = int(userInput)
        except ValueError:
            print 'Error: value must be an integer'
            vdop = 1111
        else:
            if vdop == 1111:
                bits_vdop = '1111'
            elif vdop <= 1:
                bits_vdop = '0000'
            elif vdop > 1 and vdop <= 2:
                bits_vdop = '0001'
            elif vdop > 2 and vdop <= 3:
                bits_vdop = '0010'
            elif vdop > 3 and vdop <= 4:
                bits_vdop = '0011'
            elif vdop > 4 and vdop <= 5:
                bits_vdop = '0100'
            elif vdop > 5 and vdop <= 6:
                bits_vdop = '0101'
            elif vdop > 6 and vdop <= 7:
                bits_vdop = '0110'
            elif vdop > 7 and vdop <= 8:
                bits_vdop = '0111'
            elif vdop > 8 and vdop <= 10:
                bits_vdop = '1000'
            elif vdop > 10 and vdop <= 12:
                bits_vdop = '1001'
            elif vdop > 12 and vdop <= 15:
                bits_vdop = '1010'
            elif vdop > 15 and vdop <= 20:
                bits_vdop = '1011'
            elif vdop > 20 and vdop <= 30:
                bits_vdop = '1100'
            elif vdop > 30 and vdop <= 50:
                bits_vdop = '1101'
            else:
                bits_vdop = '1110'
            break
    print 'You entered: V' + Func2.getDOP(bits_vdop)

    bits_rotating0 += bits_vdop


    ##BIT 40-41 (194-195) Automated/manual activation notification
    while next_step is False:
        print '\nPlease select activation method:'
        for x in definitions.activation_note:
            print (x) + ': ' + definitions.activation_note[x]
        bits_activation = raw_input()
        try:
            definitions.activation_note[bits_activation]
        except KeyError:
            print 'Error: invalid input'
        else:
            break
    print 'You entered: ' + definitions.activation_note[bits_activation]

    bits_rotating0 += bits_activation

    ##BIT 42-44 (196-198) Remaining battery capacity
    while next_step is False:
        userInput = raw_input('\nPlease enter remaining batter capacity (%). If unavailable, enter 111: ')
        try:
            battery = int(userInput)
        except ValueError:
            print 'Error: value must be an integer'
            battery = 111
        else:
            if battery <= 5:
                bits_battery = '000'
            elif battery > 5 and battery <= 10:
                bits_battery = '001'
            elif battery > 10 and battery <= 25:
                bits_battery = '010'
            elif battery > 25 and battery <= 50:
                bits_battery = '011'
            elif battery > 50 and battery <= 75:
                bits_battery = '100'
            elif battery > 75 and battery <= 100:
                bits_battery = '101'
            else:
                bits_battery = '111'
            break
    print 'You entered: ' + definitions.battery[bits_battery]

    bits_rotating0 += bits_battery

    ##BIT 45-46 (199-200) GNSS status
    while next_step is False:
        print '\nPlease select GNSS status:'
        for x in definitions.gnss_status:
            print (x) + ': ' + definitions.gnss_status[x]
        bits_gnss = raw_input()
        try:
            definitions.gnss_status[bits_gnss]
        except KeyError:
            print 'Error: invalid input'
        else:
            break
    print 'You entered: ' + definitions.gnss_status[bits_gnss]

    bits_rotating0 += bits_gnss

    ##BIT 47-48 (201-202) Spare
    bits_rotating0 += '00'

    rotatingfield = bits_rotating0


################################################
# Rotating Field Type: Inflight Emergency (#1) #
################################################
elif rotatingID == 1:
    print '\nRotating Field Type: Inflight Emergency (#1)'
    bits_rotating1 = bits_rotatingID

    ##BIT 5-21 (159-175) Time of last encoded location
    while next_step is False:
        encoded_loc_time = raw_input('Please enter time of last encoded location in the following format hh:mm:ss : ')
        try:
            encoded_loc_sec = int(encoded_loc_time[0:2]) * 3600 + int(encoded_loc_time[3:5]) * 60 + int(encoded_loc_time[6:])
        except ValueError:
            print 'Error: invalid input'
        else:
            bits_encoded_loc_time = Func1.dec2bin(encoded_loc_sec).zfill(17)
            break
    print 'You entered: ' + Func2.sec2utc(bits_encoded_loc_time)

    bits_rotating1 += bits_encoded_loc_time


    ##BIT 22-31 (176-185) Altitude of encoded location
    while next_step is False:
        userInput = raw_input('\nPlease enter altitude in metres: ')
        try:
            altitude = int(userInput)
        except ValueError:
            print 'Error: value must be an integer'
            altitude = 0
        else:
            bits_altitude = Func1.dec2bin(int((altitude + 400)/16)).zfill(10)
            if len(bits_altitude) != 10:
                print 'Error: input too long.'
            elif not Func2.isBinary(bits_altitude):
                print 'Error: inavlid input'
            else:
                break
    print 'You entered: ' + str(Func2.getaltitude(bits_altitude))

    bits_rotating1 += bits_altitude


    ##BIT 32-35 (186-189) Triggering event
    while next_step is False:
        print '\nPlease select triggering event:'
        for x in definitions.triggering_event:
            print (x) + ': ' + definitions.triggering_event[x]
        bits_trigger = raw_input()
        try:
            definitions.triggering_event[bits_trigger]
        except KeyError:
            print 'Error: invalid input'
        else:
            break
    print 'You entered: ' + definitions.triggering_event[bits_trigger]

    bits_rotating1 += bits_trigger


    ##BIT 36-37 (190-191) GNSS Status
    while next_step is False:
        print '\nPlease select GNSS status:'
        for x in definitions.gnss_status:
            print (x) + ': ' + definitions.gnss_status[x]
        bits_gnss = raw_input()
        try:
            definitions.gnss_status[bits_gnss]
        except KeyError:
            print 'Error: invalid input'
        else:
            break
    print 'You entered: ' + definitions.gnss_status[bits_gnss]

    bits_rotating1 += bits_gnss


    ##BIT 38-39 (192-193) Remaining battery capacity
    while next_step is False:
        print '\nPlease select remaining battery capacity:'
        for x in definitions.inflight_battery:
            print (x) + ': ' + definitions.inflight_battery[x]
        bits_inflight_battery = raw_input()
        try:
            definitions.inflight_battery[bits_inflight_battery]
        except KeyError:
            print 'Error: invalid input'
        else:
            break
    print 'You entered: ' + definitions.inflight_battery[bits_inflight_battery]

    bits_rotating1 += bits_inflight_battery

    ##BIT 40-48 (194-202) Spare
    bits_rotating1 += (9 * '0')

    rotatingfield = bits_rotating1


#################################
# Rotating Field Type: RLS (#2) #
#################################
elif rotatingID == 2:
    print '\nRotating Field Type: RLS (#2)'
    bits_rotating2 = bits_rotatingID


    ##BIT 5-6 (159-160) Beacon Type
    while next_step is False:
        print '\nPlease select beacon type:'
        for x in definitions.beacon_type:
            print (x) + ': ' + definitions.beacon_type[x]
        bits_beacon_type = raw_input()
        try:
            definitions.beacon_type[bits_beacon_type]
        except KeyError:
            print 'Error: invalid input'
        else:
            break
    print 'You entered: ' + definitions.beacon_type[bits_beacon_type]

    rotating2 += bits_beacon_type


    ##BIT 7-12 (161-166) Beacon RLS Capability
    while next_step is False:
        print '\nPlease select beacon type:'
        for x in definitions.beacon_type:
            print (x) + ': ' + definitions.beacon_type[x]
        bits_beacon_type = raw_input()
        try:
            definitions.beacon_type[bits_beacon_type]
        except KeyError:
            print 'Error: invalid input'
        else:
            break
    print 'You entered: ' + definitions.beacon_type[bits_beacon_type]

    rotatingfield = bits_rotating2

##########################################
# Rotating Field Type: National Use (#3) #
##########################################
elif rotatingID == 3:
    print '\nRotating Field Type: National Use (#3)'
    bits_rotating3 = bits_rotatingID + ('0' * 44)


    rotatingfield = bits_rotating3

###################################################
# Rotating Field Type: Cancellation Message (#15) #
###################################################
elif rotatingID == 15:
    print '\nRotating Field Type: Cancellation Message (#15)'

    bits_rotating15 = bits_rotatingID + ('1' * 42)

    while next_step is False:
        print '\nPlease select method of deactivation:'
        for x in definitions.deactivation:
            print (x) + ': ' + definitions.deactivation[x]
        bits_deactivation = raw_input()
        try:
            definitions.deactivation[bits_deactivation]
        except KeyError:
            print 'Error: invalid input'
        else:
            break
    print 'You entered: ' + definitions.deactivation[bits_deactivation]

    bits_rotating15 += bits_deactivation

    rotatingfield = bits_rotating15


####################################
# All other rotating fields: SPARE #
####################################
else:
    print '\nRotating Field Type: Spare'
    bits_rotating4 = bits_rotatingID + ('0' * 44)


    rotatingfield = bits_rotating4



bits_maininfo = bits_tac + bits_serialnum + bits_countrycode + bits_status + bits_selftest + bits_cancel + bits_latitude + bits_longitude + vessel_bits + bits_spare




testbits = bits_maininfo + rotatingfield
BCH = Func2.calcBCH(testbits, 0, 202, 250)

testbits = testbits + BCH



testhex = Func2.bin2hex('00' + testbits)
print '\nYour beacon message is: ' + testhex


newBeacon1 = Gen2.SecondGen(testhex)
newBeacon1.processHex(testhex)

##Add BCH to export file
newBeacon1.tablebin.append(['203-250',
                            newBeacon1.bits[203:],
                            'BCH',
                            ''])

##Add Hex message to export file
newBeacon1.tablebin.append(['',
                            '',
                            'Beacon message:',
                            testhex])


with open('my_beacon.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Bit Range', 'Bit Value', 'Field Name', 'Field Value'])
    [writer.writerow(r) for r in newBeacon1.tablebin]

index = 0
while index < len(newBeacon1.tablebin):
    newBeacon1.tablebin[index] = [newBeacon1.tablebin[index][0],
                                  '\'' + newBeacon1.tablebin[index][1],
                                  len(newBeacon1.tablebin[index][1]),
                                  newBeacon1.tablebin[index][2],
                                  newBeacon1.tablebin[index][3]]
    index += 1


with open('my_beacon_excel.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Bit Range', 'Bit Value', 'Number of Bits', 'Field Name', 'Field Value'])
    [writer.writerow(r) for r in newBeacon1.tablebin]
