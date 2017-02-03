




def bch(binary,gx,filename=None):
    bchlist=list(binary+'0'*(len(gx)-1))
    newrow=[]
    c=0
    print '-'+''.join(bchlist)
    
    for i in range(len(binary)):
        c=c+1
        if bchlist[i] == '1':
            
            if c>0:
                print "{}{} \n{}{}".format((c)*'+',gx,c*'-',''.join(newrow))
            newrow=[]
            for k in range(len(gx)):
                if bchlist[i+k] == gx[k]:
                    bchlist[i+k] = '0'
                    newrow.append('0')
                else:
                    bchlist[i+k] = '1'
                    newrow.append('1')
    return ''.join(bchlist)[-((len(gx))-1):]





if __name__ == "__main__":
    
    b="""1001100100110100000000000011100110100011110111000000000000000000000000000000000000000000000111000110000011001110100011001000101000000010010010111111111111000000000100000000110000011001100000001001011011"""
    print len(b)
    gx='1110001111110101110000101110111110011110010010111'

    a=bch(b,gx)
    print "Initial length of input binary: {} \nLength of bch calculated binary:{} \nComputed bch: {} ".format(len(b),len(a),a)


    
