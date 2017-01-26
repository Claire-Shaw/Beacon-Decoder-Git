


# Beacon Hex Decoding Definitions
protocols=['Location Protocol','User Protocol']
countrydic={}
country=open('countries.csv')

messagetype={'0':'Short Message','1':'Long Message'} #bit 25
protocol={'0':'Location Protocol','1':'User Protocol'} #bit 26 

emergencycode={'0001':'Fire/explosion',
               '0010':'Flooding',
               '0011':'Collision',
               '0100':'Grounding',
               '0101':'Listing, in danger of capsizing',
               '0110':'Sinking',
               '0111':'Disabled and adrift',
               '0000':'Unspecified distress',
               '1000':'Abandoning ship'}
               
#Bits 84 to 85
auxlocdevice={'00':'No Auxiliary Radio-locating Device',
              '':'No Auxiliary Radio-locating Device',
              '01':'121.5 MHz Auxiliary Radio-locating Device',
              '10':'9 GHz SART Locating Device',
              '11':'Other Auxiliary Radio-locating Device(s)'}

#Bits 37 to 40
locprottype={'0000':'Unknown location type'
             ,'0001':'Unknown location type'
             
             ,'0010':'Standard Location Protocol EPIRB-MMSI'
             ,'0110':'Standard Location Protocol - EPIRB (Serial)'
             ,'1010':'National location protocol - EPIRB'
             ,'1100':'Std. Location ship security protocol (SSAS)'
             
             ,'0011':'Std Loc. ELT 24-bit Address Protocol'
             ,'0100':'Standard Location Protocol - ELT (Serial)'
             ,'0101':'Std Loc. Serial ELT - Aircraft Operator Designator Protocol'
             ,'1000':'National location protocol - ELT'
             ,'1001':'ELT - DT Location Protocol - ELT'
             
             ,'0111':'Standard Location Protocol - PLB (Serial)'             
             ,'1011':'National location protocol - PLB'
             
             ,'1101':'RLS Location Protocol'
             ,'1110':'Standard Location Protocol - Test'             
             ,'1111':'National location protocol - Test'             
             }


#Bits 41 to 42 for ELT-DT
eltdt ={'00':'Aircraft 24 bit address'
        ,'01': 'Aircraft operators designator and serial number'
        ,'10': 'TAC with serial number'
        ,'11': 'Location Test Protocol'
        }

stdloctypes = ['0010','0011','0100','0101','0110','0111','1110','0000','1100','0001']
natloctypes = ['1000','1010','1011','1111']

#Bits 37 to 39
userprottype={'011':'Serial User Protocol (see bits 40 to 42)'
              ,'001':'ELT Aviation User Protocol'
              ,'111':'Test User Protocol'
              ,'110':'Radio Call Sign - EPIRB'
              ,'000':'Orbitography Protocol'
              ,'100':'National User Protocol ELT/EPIRB/PLB'
              ,'010':'Maritime User Protocol - EPIRB'
              ,'101':'Spare - undefined'
              }

#Bits 40 to 42
serialusertype={'000':'ELT with Serial Identification'
                ,'011':'ELT with Aircraft 24-bit Address'
                ,'110':'PLB with Serial Identification Number'
                ,'010':'Float Free EPIRB with Serial Identification Number'
                ,'100':'Non Float Free EPIRB with Serial Identification'
                ,'001':'ELT with Aircraft Operator Designator & Serial Number'
                ,'111':'Spare'
                ,'101':'Spare'
                }

baudot={'111000':'A','110011':'B','101110':'C','110010':'D','110000':'E','110110':'F','101011':'G','100101':'H'
        ,'101100':'I','111010':'J','111110':'K','101001':'L','100111':'M'
        ,'100110':'N','100011':'O','101101':'P','111101':'Q','101010':'R','110100':'S','100001':'T','111100':'U','101111':'V'
        ,'111001':'W','110111':'X','110101':'Y','110001':'Z'
        ,'100100':' ','011000':'-','010111':'/','001101':'0','011101':'1'
        ,'011001':'2','010000':'3','001010':'4','000001':'5','010101':'6','011100':'7'
        ,'001100':'8','000011':'9','010110':'?','000000':'='}


posneg={'0':'-1','1':'1'}
dataflag110={'0':'Result of bits 113 to 132 defined nationally'
                ,'1':'Delta position data defined in PDF-2'}

enc_delta_posflag={'0':'Encoded position data is provided by an external navigation device',
                '1':'Encoded position data is provided by an internal navigation device'}


enc_alt={'0000':['0','400 m (1312 ft)'],
         '0001':['400 m (1312 ft)','800 m (2625 ft)'],
         '0010':['800 m (2625 ft)','1200 m (3937 ft)'],
         '0011':['1200 m (3937 ft) ','1600 m (5249 ft)'],
         '0100':['1600 m (5249 ft)','2200 m (7218 ft)'],
         '0101':['2200 m (7218 ft)','2800 m (9186 ft)'],
         '0110':['2800 m (9186 ft)','3400 m (11155 ft)'],
         '0111':['3400 m (11155 ft)','4000 m (13123 ft)'],
         '1000':['4000 m (13123 ft)','4800 m (15748 ft)'],
         '1001':['4800 m (15748 ft)','5600 m (18373 ft)'],
         '1010':['5600 m (18373 ft)','6600 m (21654 ft)'],
         '1011':['6600 m (21654 ft)','7600 m (24934 ft)'],
         '1100':['7600 m (24934 ft)','8800 m (28871 ft)'],
         '1101':['8800 m (28871 ft)','10000 m (32808 ft)'],
         '1110':['10000 m (32808 ft)','greater'],
         '1111':['not available','not available']
         }


homer={'0':'121.5 MHz Homing device not present','1':'121.5 MHz Homing device present'}

for line in country.readlines():
        mid             = int(line.split(',')[0].rstrip())
        cname           = line.split(',')[1].rstrip()
        countrydic[mid] = cname

