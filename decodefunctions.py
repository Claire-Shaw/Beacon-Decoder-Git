#decode functions

# -*- coding: utf-8 -*-
import definitions
import time


def calcbch(binary,gx,b1start,b1end,b2end):        
    bchlist=list(binary[b1start:b1end] +'0'*(b2end-b1end))    
    for i in range(b1end-b1start):    
        if bchlist[i]=='1':           
            for k in range(len(gx)):
                if bchlist[i+k]==gx[k] :                    
                    bchlist[i+k]='0'
                else:                    
                    bchlist[i+k]='1'           
    return ''.join(bchlist)[b1end-b2end:]


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



def dec2bin(n,ln=None):
    '''convert denary integer n to binary string bStr'''
    bStr = ''
    
    if n < 0:  raise ValueError, "must be a positive integer"
    #if n == 0: return '0'
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1
    if not ln:
        l=len(bStr)
    else:
        l=ln
    b='0'*(l-len(bStr))+bStr
    return b


def is_neg(s):
    if s<0:
        return -1
    else:
        return 1

def  bin2dec(s):
    return int(s, 2)

def bin2hex(binval):
    return str(hex(int(binval, 2)))[2:].upper().strip('L')

def hextobin(hexval):
        '''
        Takes a string representation of hex data with
        arbitrary length and converts to string representation
        of binary.  Includes padding 0s
        '''
        thelen = len(hexval)*4
        hexval=str(hexval)
        
        try:
            binval = bin(int(hexval, 16))[2:]
        except ValueError:
            return False
        while ((len(binval)) < thelen):
            binval = '0' + binval
        return binval


def baudot(binstr,startpos,endpos,short=False):
    if short:
        jump=5
        one='1'
    else:
        jump=6
        one=''
    #baudot string values are 6 bit length binary with following code reference
    baudot={
            '111000':'A','110011':'B','101110':'C','110010':'D','110000':'E'
            ,'110110':'F','101011':'G','100101':'H','101100':'I','111010':'J'
            ,'111110':'K','101001':'L','100111':'M','100110':'N','100011':'O'
            ,'101101':'P','111101':'Q','101010':'R','110100':'S','100001':'T'
            ,'111100':'U','101111':'V','111001':'W','110111':'X','110101':'Y'
            ,'110001':'Z','100100':' ','011000':'-','010111':'/','001101':'0'
            ,'011101':'1','011001':'2','010000':'3','001010':'4','000001':'5'
            ,'010101':'6','011100':'7','001100':'8','000011':'9','010110':'?'
            ,'000000':'?','100000':''
            }    
    baudstr=b=''
      
    while startpos < endpos:
        
        try:
            b=baudot[one+binstr[startpos:startpos+jump]]
            
        except KeyError:
            b='?'
        
        startpos+=jump
        baudstr=baudstr+b
    return baudstr
        


def latlongresolution(binary,startpos,endpos):
    #   PDF-2 from 20 or 14 bits starting from bit 113
    #   Standard Location Procols are 20 bit length ( bits 113 to 132) with from 0-30 minutes resolution adjustment
    #   and 0 to 60 secondsresolution in 4 second increments.
    #   National Location Protocol are 14 bit length - Bits 113 to 126 express 0-3 minute resultions and 0-60 second,(4 sec) increments resolution.
    #

    l=endpos-startpos

    if binary[startpos]=='0':                                           #   1 bit (113)
        signlat=-1
        latdir='negative'
    else:
        signlat=1
        latdir='positive'
    


    if l==20:
        # Standard Location Protocol is 20 bits of data.
        # Five bits for minutes of max 30 minute adjustment

       
        latminutes  =   float(bin2dec(binary[startpos+1:startpos+6]))         #   5 bits 
        latseconds  =   float(bin2dec(binary[startpos+6:startpos+10])* 4 )    #   4 bits
        longminutes =   float(bin2dec(binary[startpos+11:startpos+16]))       #   5 bits
        longseconds =   float(bin2dec(binary[startpos+16:startpos+20])* 4 )   #   4 bits       

        if binary[startpos+10]=='0':                                        #   1 bit
            signlong=-1
            lndir='negative'
        else:
            signlong=1
            lndir='positive'
        




    elif l==14:
        # National Location Protocol is 14 bits of data.
        # Only 2 bits for minutes of max 3 minute adjustment        
        latminutes  =   float(bin2dec(binary[startpos+1:startpos+3]))         #   2 bits   
        latseconds  =   float(bin2dec(binary[startpos+3:startpos+7])*4)       #   4 bits
        longminutes =   float(bin2dec( binary[startpos+8:startpos+10]))       #   2 bits
        longseconds =   float(bin2dec(binary[startpos+10:startpos+14])*4)     #   4 bits
        if binary[startpos+7]=='0':                                         #   1 bit
            signlong=-1
            lndir='negative'
        else:
            signlong=1
            lndir='positive'
        

    elif l==18:
        print 'rls',binary[startpos+14:startpos+20]
        # RLS or ELT-DT Location Protocol is 18 bits of data.
        # Only 4 bits for minutes of max 15 minute adjustment
        latminutes  =   float(bin2dec(binary[startpos+1:startpos+5]))         #   4 bits   
        latseconds  =   float(bin2dec(binary[startpos+5:startpos+9])*4)       #   4 bits
        longminutes =   float(bin2dec(binary[startpos+10:startpos+14]))       #   4 bits
        longseconds =   float(bin2dec(binary[startpos+14:startpos+18])* 4 )   #   4 bits       
        if binary[startpos+9]=='0':                                        #   1 bit
            signlong=-1
            lndir='negative'
        else:
            signlong=1
            lndir='positive'

    else:
        # Bad length.  Length must be 14,18 or 20.
        return False


    if int(latminutes) > 30:
        longoffset = latoffset = 'default'
        
    else:
        latoffset =  '{} minutes {} seconds ({})'.format(latminutes,latseconds,latdir)
        longoffset = '{} minutes {} seconds ({})'.format(longminutes,longseconds,lndir)
    return  (signlat*(float(latminutes/60)+float(latseconds/3600)),
             signlong*(float(longminutes/60)+float(longseconds/3600)),             
             latoffset,
             longoffset)


def latitudeRLS(latsono,latdeg):    
    if latsono=='1':
        latdir='South'
        sg=-1
    else:
        latdir='North'
        sg=1    
    deg=float(bin2dec(latdeg))/float(2)
    decimal=sg*deg
    if deg>90:
        if '0' not in latdeg:
            lat = decimal = 'Default - no location'
        else:
             lat = decimal = 'Error >90 (Deg:{})'.format(decimal)        
    else:
        lat = str(deg)+' Degrees '+latdir    
    return (lat,decimal,latdir)

def longitudeRLS(longEW,longdeg):    
    if longEW=='0':
        longdir='East'
        sg=1
    else:
        longdir='West'
        sg=-1    
    deg=float(bin2dec(longdeg))/float(2)
    print longdeg,bin2dec(longdeg)
    decimal=sg*deg
    if deg>180:
        if '0' not in longdeg:
            longe = decimal = 'Default - no location'
        else:
             longe = decimal = 'Error >180 (Deg:{})'.format(decimal)        
    else:
        longe = str(deg)+' Degrees '+longdir    
    return (longe,decimal,longdir)

    
def latitude(latsono,latdeg,latmin):    
    n=1
    if latsono=='1':
        latdir='South'
        sg=-1
    else:
        latdir='North'
        sg=1
        
    if len(latmin)==5:
        n=2
    elif len(latmin)==4:
        n=4
    elif len(latmin)==2:
        n=15       
    
    minutes=float(bin2dec(latmin)*n)
    deg=float(bin2dec(latdeg))
    decimal=sg*(float(deg)+float(minutes/60))
    if deg>90:
        if '0' not in latdeg:
            lat = decimal = 'Default - no location'
        else:
             lat = decimal = 'Error >90 (Deg:{})'.format(decimal)     
        
    else:
        

        lat = str(int(deg))+' Degrees '+str(int(minutes))+' Minutes '+latdir 
    
    
    return (lat,decimal,latdir,minutes)

def longitude(longeswe,longdeg,longmin):
    n=1
    if longeswe=='0':
        lngdir='East'
        sg=1
    else:
        lngdir='West'
        sg=-1
    
    if len(longmin)==5:
        n=2
    elif len(longmin)==4:
        n=4
    elif len(longmin)==2:
        n=15
    minutes=float(bin2dec(longmin)*n)
    deg=float(bin2dec(longdeg))
    decimal=sg*(float(deg)+float(minutes/60))
    if deg>180:
        if '0' not in longdeg:
            
            lng = decimal = 'Default - no location'
            
        else:
            lng = decimal = 'Error! > 180 (Deg:{})'.format(decimal)
            
        
        
    else:
        
        lng =str(int(deg))+' Degrees '+str(int(minutes))+' Minutes '+ lngdir
    
    
    #decimal=deg + float( minutes / 60 )
    
    return (lng,decimal,lngdir,minutes)


def latlongdir(direction):
    if direction in ['South','West']:
        return -1
    else:
        return 1

def samplehex():
    b='10001100110110010'
    
    c='0000000110000010110000001000001111001011010011010000011011011110011011100011100000001111000101110110011'
    return bin2hex(b+c),len(b+c)
    
x=hextobin('8CD724C83949AC4D9716778EA03CC0')
y=bin2hex('100011001101011100100100110010000011100101001001101011000100110110010111000101100111011110001110101000000001110011000000')
