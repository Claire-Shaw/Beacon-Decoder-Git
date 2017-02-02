"""Functions specific to Second Generation Beacons"""

import definitions



def bin2dec(binary_str):
    """Convert binary string to decimal integer

    Args:
        binary_str(str): Binary data in string format
    Returns:
        dec_int(int): Decoded integer
    """

    dec_int = int(binary_str, 2)

    return dec_int



def hex2bin(my_hex):
    """Second generation beacons transmit a burst of 300 binary bits.
    The first 50 bits are the preamble, set to binary 0
    This is followed by a 250 bit message (202 information bits and 48 bit BCH)
    This function will convert the hex code to binary, omitting the 50 bit preamble, to form
    a 250 bit string

    Args:
        my_hex (str): hexadecimal string
    Returns:
        out_bin (str): binary data in string format, 250 bits long
    """
    if len(my_hex) == 51:
        out_bin = bin(int(my_hex, 16))[2:].zfill(202)
    else:
        out_bin = bin(int(my_hex, 16))[2:].zfill(250)
    return str(out_bin)



def bin2hex(binval):
    """Convert binary to hexadecimal

    Args:
        binval (str): binary data in string format
    Returns:
        hex_str (str): hexadecimal string
    """

    hex_str = str(hex(int(binval, 2)))[2:].upper().strip('L')

    return hex_str



def countryname(mid):
    """Retrieves country name in definitions.countrydic

    Args:
        mid (str): 3 digit Maritime Identification Digit
    Returns:
        cname (str): Country name
    """

    try:
        cname = definitions.countrydic[mid]
    except KeyError:
        cname = 'Unknown MID'
    return cname



def getlatitude(lat):
    """Decodes 23 latitude bits

    Args:
        lat (str): 23 binary bits
                   - Bit 0: N/S flag
                   - Bit 1-7: degrees
                   - Bit 8-23: decimal parts of a degree
    Returns:
        latitude + nsflag (str): latitude value and N/S flag
        signedLat (float): If N/S flag is N, signedLat will be positive.
            Otherwise, it will be negative
    """

    if lat == '01111111000001111100000':  #Default value
        return ('No latitude data available', 'N/A')

    else:
        if lat[0] == '0':
            nsflag = 'N'
        else:
            nsflag = 'S'

        degreelat = bin2dec(lat[1:8])
        degreelatdec = float(bin2dec(lat[8:]))/pow(2, 15)
        latitude = float("{0:.5f}".format(degreelatdec + degreelat))

        if nsflag == 'N':
            signedLat = latitude
        else:
            signedLat = latitude * -1.0

        if latitude > 90:
            return ('Invalid Latitude', 'N/A')
        else:
            return ((str(latitude) + " " + nsflag), signedLat)



def getlongitude(lon):
    """Decodes 24 latitude bits

    Args:
        lon (str): 24 binary bits
                   - Bit 0: E/W flag
                   - Bit 1-8: degrees
                   - Bit 9-24: decimal parts of a degree
    Returns:
        longitude + ewflag (str): longitude value and E/W flag
        signedLon (float): If E/W flag is E, signedLon will be positive.
            Otherwise, it will be negative
    """

    if lon == '011111111111110000011111':     #Default value
        return ('No longitude data available', 'N/A')

    else:
        if lon[0] == '0':
            ewflag = 'E'
        else:
            ewflag = 'W'

        degreelon = bin2dec(lon[1:9])
        degreelondec = float(bin2dec(lon[9:]))/pow(2, 15)
        longitude = float("{0:.5f}".format(degreelondec + degreelon))

        if ewflag == 'E':
            signedLon = longitude
        else:
            signedLon = longitude * -1.0

        if degreelon > 180:
            return ('Invalid Longitude', 'N/A')
        else:
            return ((str(longitude) + " " + ewflag), signedLon)



def baudot2str(binary, chars):
    """Input binary string + expected # of characters.
    Each group of 6 bits is then decoded to a character

    Args:
        binary (str): binary string to be decoded
        chars (int): number of expected characters
    Returns:
        message (str): decoded Baudot message
    """

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
    """Checks if input string is all ones

    Args:
        b (str): binary string
    Returns:
        isones (bool): True if all ones, otherwise False
    """

    isones = True
    for j in range(0, len(b)):
        if b[j] == '0':
            isones = False
    return isones



def checkzeros(a):
    """Checks if input string is all zeros

    Args:
        a (str): binary string
    Returns:
        iszeros (bool): True if all zeros, otherwise False
    """

    iszeros = True
    for k in range(0, len(a)):
        if a[k] == '1':
            iszeros = False
    return iszeros



def getaltitude(alt_bits):
    """If input is all ones, not altitude available.
    Otherwise, convert the binary string to decimal.
    Altitude starts at -400 meters.

    Args:
        alt_bits (str): binary string
    Returns:
        altitude (str): string containing decoded altitude data
    """

    if checkones(alt_bits):
        altitude = 'No altitude data available'
    else:
        altitude = str(-400 + 16*bin2dec(alt_bits))+' m'
    return altitude



def sec2utc(timebits):
    """Converts binary string to decimal.
    Input is total number of seconds. Convert seconds to formatted hours, minutes & seconds.

    Args:
        timebits (str): total time in seconds, in binary format
    Returns:
        hh:mm:ss (str): formatted UTC time
    """

    time = bin2dec(timebits)
    hh = (int)(time / 3600)
    mm = (int)((time - hh*3600)/60)
    ss = time - (hh*3600) - (mm*60)
    return str(hh) + ':' + str(mm) + ':' + str(ss) + ' UTC'



def getDOP(dop_bits):
    """Input binary string, look up in DOP table.

    Args:
        dop_bits (str): bit string
    Returns:
        mydop (str): string containing DOP (dilution of precision)
    """

    try:
        mydop = definitions.dop[dop_bits]
    except KeyError:
        mydop = 'Unknown DOP'
    return mydop



def errors(b1, b2):
    """Take two stings of bits, compare, and output the # of differences.

    Args:
        b1 (str): bit string 1 to be compared
        b2 (str): bit string 2 to be compared
    Returns:
        bitError (int): number of differences between the two bit strings
    """

    bitError = 0
    for num, bit in enumerate(b1):
        bitError = bitError + abs(int(bit) - int(b2[num]))
    return bitError



def calcBCH(binary, b1start, b1end, b2end):
    """ Calculates the expected BCH error-correcting code for a given binary string.
    See C/S T.018 for details.

    Args:
        binary (str): binary string
        b1start (int): bit at which to start calculating
        b1end (int): bit at which to end calculating
        b2end (int): total length of bit string
    Returns:
        bchlist: calculated BCH code
    """

    gx = '1110001111110101110000101110111110011110010010111'
    bchlist = list(binary[b1start:b1end] + '0'*(b2end-b1end))
    for i in range(b1end-b1start):
        if bchlist[i] == '1':
            for k in range(len(gx)):
                if bchlist[i+k] == gx[k]:
                    bchlist[i+k] = '0'
                else:
                    bchlist[i+k] = '1'
    return ''.join(bchlist)[b1end-b2end:]
    