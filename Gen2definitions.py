# Beacon Hex Decoding Definitions
#This is a test

countrydic = {}
country = open('countries.csv')
for line in country.readlines():
    mid = int(line.split(',')[0].rstrip())
    cname = line.split(',')[1].rstrip()
    countrydic[mid] = cname

baudot = {'111000':'A', '110011':'B', '101110':'C', '110010':'D',
          '110000':'E', '110110':'F', '101011':'G', '100101':'H',
          '101100':'I', '111010':'J', '111110':'K', '101001':'L',
          '100111':'M', '100110':'N', '100011':'O', '101101':'P',
          '111101':'Q', '101010':'R', '110100':'S', '100001':'T',
          '111100':'U', '101111':'V', '111001':'W', '110111':'X',
          '110101':'Y', '110001':'Z', '100100':' ', '011000':'-',
          '010111':'/', '001101':'0', '011101':'1', '011001':'2',
          '010000':'3', '001010':'4', '000001':'5', '010101':'6',
          '011100':'7', '001100':'8', '000011':'9', '010110':'?',
          '000000':'='}

dop = {'0000':'DOP <=1', '0001':'DOP >1 and <=2', '0010':'DOP >2 and <=3', 
       '0011':'DOP >3 and <=4', '0100':'DOP >4 and <=5', '0101':'DOP >5 and <=6',
       '0110':'DOP >6 and <=7', '0111':'DOP >7 and <=8', '1000':'DOP >8 and <=10',
       '1001':'DOP >10 and <=12', '1010':'DOP >12 and <=15', '1011':'DOP >15 and <=20',
       '1100':'DOP >20 and <=30', '1101':'DOP >30 and <=50', '1110':'DOP >50',
       '1111':'DOP not available'}

activation_note = {'00':'Manual activation by user',
                   '01':'Automatic activation by the beacon',
                   '10':'Automatic activation by external means',
                   '11':'Spare'}

battery = {'000':'<=5% remaining',
           '001':'>5% and <=10% remaining',
           '010':'>10% and <=25% remaining',
           '011':'>25% and <=50% remaining',
           '100':'>50% and <=75% remaining',
           '101':'>75% and <=100% remaining',
           '110':'reserved for future use',
           '111':'battery capacity not available'}

gnss_status = {'00':'No fix',
               '01':'2D location only',
               '10':'3D location',
               '11':'Reserved for future use'}

triggering_event = {'0001':'Manual activation by the crew',
                    '0100':'G-switch/deformation activation',
                    '1000':'Automatic activation from avionics or triggering system'}

inflight_battery = {'00':'<=9 hours autonomy remaining',
                    '01':'>9 and <=18 hours autonomy remaining',
                    '10':'>18 hours autonomy remaining',
                    '11':'Battery capacity not available'}

beacon_type = {'00':'ELT',
               '01':'EPIRB',
               '10':'PLB',
               '11':'RLS Test Protocol'}

rls_provider = {'001':'GALILEO Return Link Service Provider',
                '010':'GLONASS Return Link Service Provider'}

deactivation = {'00':'Spare',
                '10':'Manual de-activation by user',
                '01':'Automatic de-activation by external means',
                '11':'Spare'}
