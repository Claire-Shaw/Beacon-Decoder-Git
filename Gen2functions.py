import definitions


def bin2dec(binary_str):
    """Convert binary string to decimal integer"""

    return int(binary_str, 2)

def hex2bin(my_hex):
    """Second generation beacons transmit a burst of 300 binary bits.
    The first 50 bits are the preamble, set to binary 0
    This preamble is followed by a 250 bit message (202 information bits and 48 bit BCH)
    This function will convert the hex code to binary
    """

    if len(my_hex) == 51:
        out_bin = bin(int(my_hex, 16))[2:].zfill(202)
    else:
        out_bin = bin(int(my_hex, 16))[2:].zfill(250)

    return str(out_bin)

def bin2hex(binval):
    """Convert binary string to hexadecimal string"""
    return str(hex(int(binval, 2)))[2:].upper().strip('L')

def countryname(mid):
    try:
        cname = definitions.countrydic[mid]
    except KeyError:
        cname = 'Unknown MID'
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
        return ('No latitude data available', 'N/A')
    else:
        if lat[0] == '0':
            nsflag = 'N'
        else:
            nsflag = 'S'

        degreelat = bin2dec(lat[1:8])
        degreelatdec = float(bin2dec(lat[8:24]))/pow(2, 15)
        latitude = float("{0:.5f}".format(degreelatdec + degreelat))

        if latitude > 90:
            return ('Invalid Latitude', 'N/A')
        else:
            if nsflag == 'N':
                signedLat = latitude
            else:
                signedLat = latitude * -1.0
            return ((str(latitude) + " " + nsflag), signedLat)


def getlongitude(lon):
    if lon == 011111111111110000011111:
        return ('No longitude data available', 'N/A')
    else:
        if lon[0] == '0':
            ewflag = 'E'
        else:
            ewflag = 'W'

        degreelon = bin2dec(lon[1:9])
        degreelondec = float(bin2dec(lon[9:25]))/pow(2, 15)
        longitude = float("{0:.5f}".format(degreelondec + degreelon))

        if degreelon > 180:
            return ('Invalid Longitude', 'N/A')
        else:
            if ewflag == 'E':
                signedLon = longitude
            else:
                signedLon = longitude * -1.0
            return ((str(longitude) + " " + ewflag), signedLon)

def baudot2str(binary, chars):
    message = ""
    start = 0
    stop = 6
    increment = 6
    for i in range(0, chars):
        bits = str(binary[start:stop])
        try:
            message = message + definitions.baudot[bits]
        except KeyError:
            message = message + 'error'
        start += increment
        stop += increment
    return message

def checkones(b):
    isones = True
    for j in range(0, len(b)):
        if b[j] == '0':
            isones = False
    return isones

def checkzeros(a):
    iszeros = True
    for k in range(0, len(a)):
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
        mydop = definitions.dop[b]
    except KeyError:
        mydop = 'Unknown DOP'
    return mydop

def errors(b1, b2):
    """Take two stings of bits, compare, and output the # of differences"""
    bitError = 0
    for num, bit in enumerate(b1):
        bitError = bitError + abs(int(bit) - int(b2[num]))
    return bitError

def calcBCH(binary, b1start, b1end, b2end):
    gx = '1110001111110101110000101110111110011110010010111'
    bchlist = list(binary[b1start:b1end] + '0'*(b2end-b1end))
    for i in range(b1end-b1start):
        if bchlist[i] == '1':
            for k in range(len(gx)):
                if bchlist[i+k] == gx[k]:
                    bchlist[i+k] = '0'
                else:
                    bchlist[i+k]= '1'
    return ''.join(bchlist)[b1end-b2end:]