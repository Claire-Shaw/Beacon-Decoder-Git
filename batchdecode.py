import decodefunctions as Fcn
import decodehex2 as Bcn
### -*- coding: utf-8 -*-
import definitions
import time


def decode(sourcefilename,targetfilename):
    hexcodes=open(sourcefilename)
    decoded=open(targetfilename,'w')
    n=0
    c=Bcn.BeaconHex()
    decoded.write("""Input Message,Self Test,15 Hex ID,Complete,Test Coded,Beacon Type,TAC,Country Code,Country Name,Location Type,Position Source,Course Lat,Course Long,Final Lat,Final Long\n""")
    for line in hexcodes.readlines():
        line=str(line.strip())
        decoded.write('{h},'.format(h=str(line)))
        try:
            c.processHex(str(line))
            if c._btype=='Test':
                testcode='1'
            else:
                testcode='0'
            decoded.write('{},'.format(str(c.testmsg)))
            decoded.write('{},'.format(c.hex15))
            decoded.write('{},'.format(c.bch.complete))
            decoded.write('{},'.format(testcode))
            decoded.write('{},'.format(c._btype))
            decoded.write('{},'.format(c.tac))
            decoded.write('{},'.format(c.countrydetail.mid))
            decoded.write('{},'.format(c.countrydetail.cname))
            decoded.write('{},'.format(c._loctype))
            decoded.write('{},'.format(c.encpos))
            decoded.write('{},'.format(str(c.courseloc[0])))
            decoded.write('{},'.format(str(c.courseloc[1])))
            

            
            decoded.write('{},'.format(c.location[0]))
            decoded.write('{},'.format(c.location[1]))
            
            
            
            
        
    
        except Bcn.HexError as e:
           
            decoded.write(e.value + '  '+e.message)
        decoded.write('\n')

    hexcodes.close()
    decoded.close()
        


        
            
            
        
            
            
            

if __name__ == "__main__":
        
        
        

    t0 = time.time()
    decode('inputhex.csv','decodedhex.csv')
    print(time.time() - t0, "seconds wall time")
    

        
