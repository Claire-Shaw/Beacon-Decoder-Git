import newdefinitions
import binascii

def bin2dec(s):
    return int(s,2)

def hex2bin(hex):
    out_bin = bin(int(hex,16))[2:].zfill(204)
    return str(out_bin)

def countryname(mid):
    try:
        cname=newdefinitions.countrydic[mid]
    except KeyError:
        cname='Unknown MID'
    return cname

def homingstatus(homing):
    if homing == '1':
        return 'Beacon is equipped with at least one homing signal. If beacon has been activated, at least one homing device is functional and transmitting'
    else:
        return 'Beacon is not equipped with any homing signals or they have been deliberately disabled.  If beacon has been activated, no homing device is functional or it has been deliberately disabled'

def selftest(stest):
    if stest == '1':
        return 'Normal beacon operation (transmitting a distress)'
    else:
        return 'Self-test transmission'

def usercancel(cancel):
    if cancel == '1':
        return 'User cancellation message'
    else:
        return 'Normal beacon operation (transmitting a distress or self-test message)' 

def getlatitude(lat):
    if lat == 01111111000001111100000:
        return 'No latitude data available'
    else:
        if lat[0] == '0':
            nsflag = 'N'
        else:
            nsflag = 'S'

        degreelat = bin2dec(lat[1:8])
        degreelatdec = float(bin2dec(lat[8:24]))/pow(2,15)
        latitude = float("{0:.5f}".format(degreelatdec + degreelat))

        if degreelat > 90:
            return 'Invalid Latitude'
        else:
            return str(latitude) + " " + nsflag
     

def getlongitude(lon):
    if lon == 011111111111110000011111:
        return 'No longitude data available'
    else:
        if lon[0] == '0':
            ewflag = 'E'
        else:
            ewflag = 'W'

        degreelon = bin2dec(lon[1:9])
        degreelondec = float(bin2dec(lon[9:25]))/pow(2,15)
        longitude = float("{0:.5f}".format(degreelondec + degreelon))

        if degreelon > 180:
            return 'Invalid Longitude'
        else:
            return str(longitude) + " " + ewflag

def baudot2str(binary, chars):
    message = ""
    start = 0
    stop = 6
    increment = 6
    for i in range(0,chars):
        bits = str(binary[start:stop])
        try:
            message = message + newdefinitions.baudot[bits]
        except KeyError:
            message = message + 'error'
        start += increment
        stop += increment
    return message

def checkones(b):
    isones = True
    for j in range(0,len(b)):
        if b[j] == '0':
            isones = False
    return isones

def checkzeros(a):
    iszeros = True
    for k in range(0,len(a)):
        if a[k] == '1':
            iszeros = False
    return iszeros

def getaltitude(m):
    if checkones(m):
        return 'No altitude data available'
    else:
        return str(-400 + 16*bin2dec(m))+' m'

def sec2utc(b):
    time = bin2dec(b)
    hh = (int)(time / 3600)
    mm = (int)((time - hh*3600)/60)
    ss = time - (hh*3600) - (mm*60)
    return str(hh)+':'+str(mm)+':'+str(ss)+' UTC'

def getDOP(b):
    try:
        mydop=newdefinitions.dop[b]
    except KeyError:
        mydop='Unknown DOP'
    return mydop
