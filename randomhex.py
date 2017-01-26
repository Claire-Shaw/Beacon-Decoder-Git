import decodefunctions as Fcn
import random
decoded=open('samplehex.csv','w')

# generate 154 bit hex codes
for n in range(10000):
    binstr=''
    for i in range(154):
        x=random.random()
        if x<.5:
            b='0'
        else:
            b='1'

        binstr=binstr+b
    decoded.write(Fcn.bin2hex(binstr)+'\n')
decoded.close()


#print binstr,len(binstr),Fcn.bin2hex(binstr)
        
        

