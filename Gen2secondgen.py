###########################################
# Second Generation Beacon Decode Program #
###########################################

import Gen2functions as Func
import Gen2rotating as rotating


class Gen2Error(Exception):
    def __init__(self, value, message):
        self.value = value
        self.message = message

    def __str__(self):
        return repr(self.value, self.message)


class SecondGen(Gen2Error):

    def __init__(self, hexCode=None):
        self.bits = '0' * 250

    def processHex(self, strhex):

        ##All second generation beacon messages must be EXACTLY 250 bits
        ##in length for the program to function properly.
        self.bits = Func.hex2bin(strhex)


        if len(self.bits) == 250 or len(self.bits) == 202:
            self.tablebin = []
            self.rotatingbin = []

            ##Add an additional bit to ensure that bits in array line up with bits in documentation
            self.bits = "0" + self.bits

            ##BIT 1-20  Type Approval Certificate #
            self.tac = Func.bin2dec(self.bits[1:21])
            self.tablebin.append(['1-20',
                                  self.bits[1:21],
                                  'Type Approval Certificate #:',
                                  str(self.tac)])

            ##BIT 21-30 Serial Number
            self.serialNum = Func.bin2dec(self.bits[21:31])
            self.tablebin.append(['21-30',
                                  self.bits[21:31],
                                  'Serial Number:',
                                  str(self.serialNum)])

            ##BIT 31-40 Country code
            self.countryCode = Func.bin2dec(self.bits[31:41])
            self.countryName = Func.countryname(self.countryCode)
            self.tablebin.append(['31-40',
                                  self.bits[31:41],
                                  'Country code:',
                                  str(self.countryCode)+' '+str(self.countryName)])

            ##BIT 41 Status of homing device
            self.status = Func.homing(self.bits[41])
            self.tablebin.append(['41',
                                  self.bits[41],
                                  'Status of homing device:',
                                  self.status])

            ##BIT 42 Self-test function
            self.selfTestStatus = Func.selfTest(self.bits[42])
            self.tablebin.append(['42',
                                  self.bits[42],
                                  'Self-test function:',
                                  self.selfTestStatus])

            ##BIT 43 User cancellation
            self.cancel = Func.cancellation(self.bits[43])
            self.tablebin.append(['43',
                                  self.bits[43],
                                  'User cancellation:',
                                  self.cancel])

            ##BIT 44-90 Encoded GNSS location
            self.latitude = Func.getlatitude(self.bits[44:67])
            self.tablebin.append(['44-66',
                                  self.bits[44:67],
                                  'Latitude:',
                                  self.latitude[0]])

            self.longitude = Func.getlongitude(self.bits[67:91])
            self.tablebin.append(['67-90',
                                  self.bits[67:91],
                                  'Longitude:',
                                  self.longitude[0]])
            self.location = (self.latitude[1], self.longitude[1])



            ################################
            #                              #
            #  BIT 91-137 VESSEL ID FIELD  #
            #                              #
            ################################

            self.vesselID = self.bits[91:94]


            ##############################################
            # Vessel 0: No aircraft or maritime identity #
            ##############################################

            if self.vesselID == '000':
                self.tablebin.append(['91-93',
                                      self.bits[91:94],
                                      'Vessel ID:',
                                      'No aircraft or maritime identity'])

                if Func.checkzeros(self.bits[94:138]):
                    self.tablebin.append(['94-137',
                                          self.bits[94:138],
                                          'Spare:',
                                          'All 0 - OK'])
                else:
                    self.tablebin.append(['94-137',
                                          self.bits[94:138],
                                          'Spare:',
                                          'ERROR: Bits 94-137 should be 0'])


            ###########################
            # Vessel 1: Maritime MMSI #
            ###########################

            elif self.vesselID == '001':
                self.tablebin.append(['91-93',
                                      self.bits[91:94],
                                      'Vessel ID:',
                                      'MMSI'])

                self.mmsi = Func.bin2dec(self.bits[94:124])

                if self.mmsi == 111111:
                    self.tablebin.append(['94-123',
                                          self.bits[94:124],
                                          'MMSI:',
                                          'No MMSI available'])
                else:
                    self.mmsi_string = str(self.mmsi).zfill(9)

                    self.tablebin.append(['94-123',
                                          self.bits[94:124],
                                          'Unique ship station identity M1I2D3X4X5X6X7X8X9:',
                                          self.mmsi_string])
                    self.mmsi_country = Func.countryname(int(self.mmsi_string[0:3]))
                    self.tablebin.append(['',
                                          '',
                                          'Flag state of vessel:',
                                          self.mmsi_string[0:3] + ' ' + self.mmsi_country])
                    self.tablebin.append(['',
                                          '',
                                          'Unique vessel number:',
                                          self.mmsi_string[3:]])

                self.epirb_ais = Func.bin2dec(self.bits[124:138])

                if self.epirb_ais == 10922:
                    self.tablebin.append(['124-137',
                                          self.bits[124:138],
                                          'EPIRB-AIS System Identity:',
                                          'No EPIRB-AIS System'])
                else:
                    self.epirb_ais_str = str(self.epirb_ais).zfill(4)

                    self.epirb_ais_str = '974' + self.mmsi_string[3:5] + self.epirb_ais_str
                    self.tablebin.append(['124-137',
                                          self.bits[123:137],
                                          'EPIRB-AIS System Identity:',
                                          self.epirb_ais_str])


            #############################
            # Vessel 2: Radio Call Sign #
            #############################

            elif self.vesselID == '010':
                self.tablebin.append(['91-93',
                                      self.bits[91:94],
                                      'Vessel ID:',
                                      'Radio Call Sign'])

                self.callsign = Func.getCallsign(self.bits[94:136])

                self.tablebin.append(['94-135',
                                      self.bits[94:136],
                                      'Radio Callsign:',
                                      self.callsign])

                if Func.checkzeros(self.bits[136:138]):
                    self.tablebin.append(['136-137',
                                          self.bits[136:138],
                                          'Spare:',
                                          'All 0 - OK'])
                else:
                    self.tablebin.append(['136-137',
                                          self.bits[136:138],
                                          'Spare:',
                                          'ERROR: Bits 136-137 should be all 0s'])


            #########################################################
            # Vessel 3: Aricraft Registration Marking (Tail Number) #
            #########################################################

            elif self.vesselID == '011':
                self.tablebin.append(['91-93',
                                      self.bits[91:94],
                                      'Vessel ID:',
                                      'Aircraft Registration Marking (Tail Number)'])

                self.tailnum = Func.getTailNum(self.bits[94:136])

                self.tablebin.append(['94-135',
                                      self.bits[94:136],
                                      'Aircraft Registration Marking:',
                                      self.tailnum])

                if Func.checkzeros(self.bits[135:137]):
                    self.tablebin.append(['136-137',
                                          self.bits[136:138],
                                          'Spare:',
                                          'OK'])
                else:
                    self.tablebin.append(['136-137',
                                          self.bits[136:138],
                                          'Spare:',
                                          'ERROR: Bits 136-137 should be all 0s'])


            ##############################################
            # Vessel 4: Aircraft Aviation 24 Bit Address #
            ##############################################

            elif self.vesselID == '100':
                self.tablebin.append(['91-93',
                                      self.bits[91:94],
                                      'Vessel ID:',
                                      'Aircraft Aviation 24 Bit Address'])

                self.aviationBitAddress = Func.bin2dec(self.bits[93:117])
                self.tablebin.append(['94-117',
                                      self.bits[94:118],
                                      'Aviation 24 bit address:',
                                      str(self.aviationBitAddress)])

                if Func.checkzeros(self.bits[117:137]):
                    self.tablebin.append(['118-137',
                                          self.bits[118:138],
                                          'Spare:',
                                          'OK'])
                else:
                    self.tablebin.append(['118-137',
                                          self.bits[118:138],
                                          'Spare:',
                                          'ERROR: Bits 118-137 following aviation 24 bit address should be 0'])


            #################################################
            # Vessel 5: Aircraft Operator and Serial Number #
            #################################################

            elif self.vesselID == '101':
                self.tablebin.append(['91-93',
                                      self.bits[91:94],
                                      'Vessel ID:',
                                      'Aircraft Operator and Serial Number'])

                self.operator = Func.baudot2str(self.bits[94:112], 3)
                self.serialnum = Func.bin2dec(self.bits[112:124])
                self.tablebin.append(['94-111',
                                      self.bits[94:112],
                                      'Aircraft operator:',
                                      self.operator])
                self.tablebin.append(['112-123',
                                      self.bits[112:124],
                                      'Serial number:',
                                      str(self.serialnum)])


                if Func.checkones(self.bits[124:138]):
                    self.tablebin.append(['124-137',
                                          self.bits[124:138],
                                          'Spare:',
                                          'OK'])
                else:
                    self.tablebin.append(['124-137',
                                          self.bits[124:138],
                                          'Spare:',
                                          'ERROR: Bits 124-137 following aircraft operator and serial numbers should be 1'])

            ##########################
            # Other Vessel IDs Spare #
            ##########################

            else:
                self.tablebin.append(['91-93',
                                      self.bits[91:94],
                                      'Vessel ID:',
                                      'Spare'])



            ##BIT 138-154 Spare bits [137-153]
            if Func.checkones(self.bits[138:155]):
                self.tablebin.append(['138-154',
                                      self.bits[138:155],
                                      'Spare:',
                                      'OK'])
            else:
                self.tablebin.append(['138-154',
                                      self.bits[138:155],
                                      'Spare:',
                                      'ERROR: Bits 138-154 should be 1s'])



            #######################################
            #                                     #
            #  BIT 155-202 48 BIT ROTATING FIELD  #
            #                                     #
            #######################################

            self.rotatingID = Func.bin2dec(self.bits[155:159])


            ######################################################
            # Rotating Field 0: C/S G.008 Objective Requirements #
            ######################################################

            if self.rotatingID == 0:
                self.tablebin.append(['155-158 (Rotating field 1-4)',
                                      self.bits[155:159],
                                      'Rotating Field Type:',
                                      '(#0) C/S G.008 Objective Requirements'])
                self.rotatingbin = rotating.rotating0(self.bits[155:203])


            ########################################
            # Rotating Field 1: Inflight Emergency #
            ########################################

            elif self.rotatingID == 1:
                self.tablebin.append(['155-158 (Rotating field 1-4)',
                                      self.bits[155:159],
                                      'Rotating Field Type:',
                                      '(#1) Inflight Emergency'])
                self.rotatingbin = rotating.rotating1(self.bits[155:203])


            #########################
            # Rotating Field 2: RLS #
            #########################

            elif self.rotatingID == 2:
                self.tablebin.append(['155-158 (Rotating field 1-4)',
                                      self.bits[155:159],
                                      'Rotating Field Type:',
                                      '(#2) RLS'])
                self.rotatingbin = rotating.rotating2(self.bits[155:203])


            ##################################
            # Rotating Field 3: National Use #
            ##################################

            elif self.rotatingID == 3:
                self.tablebin.append(['155-158 (Rotating field 1-4)',
                                      self.bits[155:159],
                                      'Rotating Field Type:',
                                      '(#3) National Use'])
                self.rotatingbin = rotating.rotating3(self.bits[155:203])


            ###########################################
            # Rotating Field 15: Cancellation Message #
            ###########################################

            elif self.rotatingID == 15:
                self.tablebin.append(['155-158 (Rotating field 1-4)',
                                      self.bits[155:159],
                                      'Rotating Field Type:',
                                      '(#15) Cancellation Message'])
                self.rotatingbin = rotating.rotating15(self.bits[155:203])


            ##################################
            # All other roating fields spare #
            ##################################

            else:
                self.tablebin.append(['155-158 (Rotating field 1-4)',
                                      self.bits[155:159],
                                      'Rotating Field Type:',
                                      'Spare'])


            ##Add rotating field data to our list
            self.tablebin.extend(self.rotatingbin)



            ####################
            # BEACON 23 HEX ID #
            ####################
            self.hexID = []

            ##Hex ID BIT 1 = fixed binary 1
            self.hexID.append('1')

            ##Hex ID BIT 2-11 = BITS 31-40 (C/S Country Code)
            self.hexID.append(self.bits[31:41])

            ##Hex ID BIT 12 = fixed binary 1
            self.hexID.append('1')

            ##Hex ID BIT 13 = fixed binary 0
            self.hexID.append('0')

            ##Hex ID BIT 14 = fixed binary 1
            self.hexID.append('1')

            ##Hex ID BIT 15-34 = BITS 1-20 (C/S TAC No)
            self.hexID.append(self.bits[1:21])

            ##Hex ID BIT 35-44 = BITS 21-30 (Beacon Serial Number)
            self.hexID.append(self.bits[21:31])

            ##Hex ID BIT 45-47 = BITS 91-93 (Aircraft/Vessel ID Type)
            self.hexID.append(self.bits[91:94])

            ##Hex ID BIT 48-91 = BITS 94-137 (Aircraft/Vessel ID)
            self.hexID.append(self.bits[94:138])

            ##Hex ID BIT 92 = fixed binary 1
            self.hexID.append('1')


            ##Join list together and convert to Hexadecimal
            self.beaconHexID = Func.bin2hex(''.join(self.hexID))

            ##Add the 23 Hex ID to our table
            self.tablebin.append(['',
                                  '',
                                  'Beacon 23 Hex ID:',
                                  self.beaconHexID])


            ####################################
            # 48-BIT BCH ERROR CORRECTING CODE #
            ####################################
            if len(self.bits) == 251:
                ##Calculate the BCH
                self.calculatedBCH = Func.calcBCH(self.bits[1:], 0, 202, 250)

                ##Compare to the BCH in the beacon message
                self.BCHerrors = Func.errors(self.calculatedBCH, self.bits[203:])

                ##Write the number of errors to our table
                self.tablebin.append(['',
                                      '',
                                      'Number of BCH errors:',
                                      str(self.BCHerrors)])

        else:
            self.type = ('Hex string length of ' + str(len(strhex)) + '.'
                         + '\nBit string length of ' + str(len(self.bits)) + '.'
                         + '\nLength of First Gen Beacon Hex String must be 15, 22 or 30'
                         + '\nLength of Second Gen Beacon Bit String must be 250 bits')
            raise Gen2Error('LengthError', self.type)

    def country(self):
        return (('Country Code:', self.countryCode), ('Country Name:', self.countryName))

    def has_loc(self):
        if self.latitude == 'No latitude data available' or self.latitude == 'Invalid Latitude' or self.longitude == 'No longitude data available' or self.longitude == 'Invalid Longitude':
            return False
        else:
            return True




