###########################################
# Second Generation Beacon Decode Program #
###########################################

import myfunctions as Func
import newdefinitions
import rotating
import csv


class SecondGen(object):

    def __init__(self,hex):
        self.bits=Func.hex2bin(hex)

    def processHex(self):
        
        self.tablebin = []
        self.rotatingbin = []

        ##BIT 1-20  Type Approval Certificate # 
        self.tac = Func.bin2dec(self.bits[1:21])
        self.tablebin.append(['1-20',
                              self.bits[1:21],
                              'Type Approval Certificate #:',
                              self.tac])

        ##BIT 21-30 Serial Number 
        self.serialNum = Func.bin2dec(self.bits[21:31])
        self.tablebin.append(['21-30',
                              self.bits[21:31],
                              'Serial Number:',
                              self.serialNum])

        ##BIT 31-40 Country code 
        self.countryCode = Func.bin2dec(self.bits[31:41])
        self.countryName = Func.countryname(self.countryCode)
        self.tablebin.append(['31-40',
                              self.bits[31:41],
                              'Country code:',
                              str(self.countryCode)+' '+str(self.countryName)])

        ##BIT 41 Status of homing device 
        self.status = Func.homingstatus(self.bits[41])
        self.tablebin.append(['41',
                              self.bits[41],
                              'Status of homing device:',
                              self.status])

        ##BIT 42 Self-test function 
        self.selfTestStatus = Func.selftest(self.bits[42])
        self.tablebin.append(['42',
                              self.bits[42],
                              'Self-test function:',
                              self.selfTestStatus])

        ##BIT 43 User cancellation 
        self.cancel = Func.usercancel(self.bits[43])
        self.tablebin.append(['43',
                              self.bits[43],
                              'User cancellation:',
                              self.cancel])

        ##BIT 44-90 Encoded GNSS location 
        self.latitude = Func.getlatitude(self.bits[44:67])
        self.tablebin.append(['44-66',
                              self.bits[44:67],
                              'Latitude:',
                              self.latitude])

        self.longitude = Func.getlongitude(self.bits[67:91])
        self.tablebin.append(['67-90',
                              self.bits[67:91],
                              'Longitude:',
                              self.longitude])



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
            self.mmsi_string = str(self.mmsi)
            
            if self.mmsi == 111111:
                self.tablebin.append(['94-123',
                                      self.bits[94:124],
                                      'MMSI:',
                                      'No MMSI available'])
            else:
                while len(self.mmsi_string) < 9:
                    self.mmsi_string = '0' + self.mmsi_string
                    
                self.tablebin.append(['94-123',
                                      self.bits[94:124],
                                      'Unique ship station identity M1I2D3X4X5X6X7X8X9:',
                                      self.mmsi_string])
                self.mmsi_country = Func.countryname(int(self.mmsi_string[0:3]))
                self.tablebin.append(['M1I2D3',
                                      self.mmsi_string[0:3],
                                      'Flag state of vessel:',
                                      self.mmsi_country])
                self.tablebin.append(['X4X5X6X7X8X9',
                                      self.mmsi_string[3:],
                                      'Unique vessel number:',
                                      self.mmsi_string[3:]])

                self.epirb_ais = Func.bin2dec(self.bits[124:138])

                if self.epirb_ais == 10922:
                    self.tablebin.append(['124-137',
                                          self.bits[124:138],
                                          'EPIRB-AIS System Identity:',
                                          'No EPIRB-AIS System'])
                else:
                    self.epirb_ais_str = str(self.epirb_ais)

                    while len(self.epirb_ais_str) < 4:
                        self.epirb_ais_str = '0' + self.epirb_ais_str

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

            self.callsign = Func.baudot2str(self.bits[94:136], 7)
            
            if self.callsign == "       ":
                self.tablebin.append(['94-135',
                                      self.bits[94:136],
                                      'Radio Callsign:',
                                      'No radio callsign available'])
            else:
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

            self.tailnum = Func.baudot2str(self.bits[94:136], 7)
            
            if self.tailnum == "       ":
                self.tablebin.append(['94-135',
                                      self.bits[94:136],
                                      'Aircraft Registration Marking:',
                                      'No aircraft registration marking available'])
            else:
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
                                  self.aviationBitAddress])

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
                                  self.serialnum])

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
            self.tablebin.append(['155-158',
                                  self.bits[155:159],
                                  'Rotating Field Type:',
                                  '(#0) C/S G.008 Objective Requirements'])
            self.rotatingbin = rotating.rotating0(self.bits[155:203])


        ########################################
        # Rotating Field 1: Inflight Emergency #
        ########################################
        
        elif self.rotatingID == '1':
            self.tablebin.append(['155-158',
                                  self.bits[155:159],
                                  'Rotating Field Type:',
                                  '(#1) Inflight Emergency'])
            self.rotatingbin = rotating.rotating1(self.bits[155:203])


        #########################
        # Rotating Field 2: RLS #
        #########################
        
        elif self.rotatingID == '2':
            self.tablebin.append(['155-158',
                                  self.bits[155:159],
                                  'Rotating Field Type:',
                                  '(#2) RLS'])
            self.rotatingbin = rotating.rotating2(self.bits[155:203])


        ##################################
        # Rotating Field 3: National Use #
        ##################################
        
        elif self.rotatingID == '3':
            self.tablebin.append(['155-158',
                                  self.bits[155:159],
                                  'Rotating Field Type:',
                                  '(#3) National Use'])
            self.rotatingbin = rotating.rotating3(self.bits[155:203])


        ###########################################
        # Rotating Field 15: Cancellation Message #
        ###########################################
        
        elif self.rotatingID == '15':
            self.tablebin.append(['155-158',
                                  self.bits[155:159],
                                  'Rotating Field Type:',
                                  '(#15) Cancellation Message'])
            self.rotatingbin = rotating.rotating15(self.bits[155:203])

                
        ##################################
        # All other roating fields spare #
        ##################################
        
        else:
            self.tablebin.append(['155-158',
                                  self.bits[155:159],
                                  'Rotating Field Type:',
                                  'Spare'])



        self.tablebin.append(self.rotatingbin)







