#48 BIT ROTATING FIELD

import Gen2functions as Func
import definitions as definitions



##############################################################
# Rotating Field Type: C/S G.008 Objective Requirements (#0) #
##############################################################

def rotating0(bits):
    rotatingbin = []

    #Add a single bit offset so bits array index # matches documentation for readbility
    bits = '0'+ bits


    ##BIT 5-10 (159-164) Elapsed time since activation (0 to 63 hours in 1 hour steps)
    t_act = Func.bin2dec(bits[5:11])
    rotatingbin.append(['159-164 (Rotating field 5-10)',
                        bits[5:11],
                        'Elapsed time since activation:',
                        str(t_act) + ' hours'])

    ##BIT 11-21 (165-175) Time from last encoded location (0 to 2047 minutes in 1 minute steps)
    t_encoded = Func.bin2dec(bits[11:22])
    rotatingbin.append(['165-175 (Rotating field 11-21)',
                        bits[11:22],
                        'Time from last encoded location:',
                        str(t_encoded)+' minutes'])

    ##BIT 22-31 (176-185) Altitude of encoded location
    altitude = Func.getaltitude(bits[22:32])
    rotatingbin.append(['176-185 (Rotating field 22-31)',
                        bits[22:32],
                        'Altitude of encoded location: ',
                        altitude])

    ##BIT 32-39 (186-193) Dilution of precision
    hdop = Func.getDOP(bits[32:36])
    rotatingbin.append(['186-189 (Rotating field 32-34)',
                        bits[32:36],
                        'HDOP:',
                        hdop])

    vdop = Func.getDOP(bits[36:40])
    rotatingbin.append(['190-193 (Rotating field 35-39)',
                        bits[36:40],
                        'VDOP:',
                        vdop])

    ##BIT 40-41 (194-195) Automated/manual activation notification
    activation = definitions.activation_note[bits[40:42]]
    rotatingbin.append(['194-194 (Rotating field 40-41)',
                        bits[40:42],
                        'Automated/manual activation notification',
                        activation])

    ##BIT 42-44 (196-198) Remaining battery capacity
    battery = definitions.battery[bits[42:45]]
    rotatingbin.append(['196-198 (Rotating field 42-44)',
                        bits[42:45],
                        'Remaining battery capacity',
                        battery])

    ##BIT 45-46 (199-200) GNSS status
    gnss = definitions.gnss_status[bits[45:47]]
    rotatingbin.append(['199-200 (Rotating field 45-46)',
                        bits[45:47],
                        'GNSS status',
                        gnss])

    ##BIT 47-48 (201-202) Spare
    if Func.checkzeros(bits[47:]):
        rotatingbin.append(['201-202 (Rotating field 47-48)',
                            bits[47:],
                            'Spare',
                            'OK'])
    else:
        rotatingbin.append(['201-202 (Rotating field 47-48)',
                            bits[47:],
                            'Spare',
                            'ERROR: Should be 00'])

    return rotatingbin



################################################
# Rotating Field Type: Inflight Emergency (#1) #
################################################

def rotating1(bits):
    rotatingbin = []

    #Add a single bit offset so bits array index # matches documentation for readbility
    bits = '0'+ bits

    ##BIT 5-21 (159-175) Time of last encoded location
    time = Func.sec2utc(bits[5:22])
    rotatingbin.append(['159-175 (Rotating field 5-21)',
                        bits[5:22],
                        'Time of last encoded location',
                        time])

    ##BIT 22-31 (176-185) Altitude of encoded location
    altitude = Func.getaltitude(bits[22:32])
    rotatingbin.append(['176-185 (Rotating field 22-31)',
                        bits[22:32],
                        'Altitude of encoded location:',
                        altitude])

    ##BIT 32-35 (186-189) Triggering event
    try:
        trigger = definitions.triggering_event[bits[32:36]]
    except KeyError:
        trigger = 'ERROR: Unknown trigger'
    rotatingbin.append(['186-189 (Rotating field 32-35)',
                        bits[32:36],
                        'Triggering event',
                        trigger])

    ##BIT 36-37 (190-191) GNSS Status
    gnss = definitions.gnss_status[bits[36:38]]
    rotatingbin.append(['190-191 (Rotating field 36-37)',
                        bits[36:38],
                        'GNSS status',
                        gnss])

    ##BIT 38-39 (192-193) Remaining battery capacity
    battery = definitions.inflight_battery[bits[38:40]]
    rotatingbin.append(['192-193 (Rotating field 38-39)',
                        bits[38:40],
                        'Remaining battery capacity',
                        battery])

    ##BIT 40-48 (194-202) Spare
    if Func.checkzeros(bits[40:]):
        rotatingbin.append(['194-202 (Rotating field 40-48)',
                            bits[40:],
                            'Spare',
                            'OK'])
    else:
        rotatingbin.append(['194-202 (Rotating field 40-48)',
                            bits[40:],
                            'Spare',
                            'ERROR: Should be 0s'])

    return rotatingbin



#################################
# Rotating Field Type: RLS (#2) #
#################################

def rotating2(bits):
    rotatingbin = []

    #Add a single bit offset so bits array index # matches documentation for readbility
    bits = '0'+ bits

    ##BIT 5-6 (159-160) Beacon Type
    beacon = definitions.beacon_type[bits[5:7]]
    rotatingbin.append(['159-160 (Rotating field 5-6)',
                        bits[5:7],
                        'Beacon type',
                        beacon])

    ##BIT 7-12 (161-166) Beacon RLS Capability
    if bits[7] == '1':
        rotatingbin.append(['161 (Rotating field 7)',
                            bits[7],
                            'Capability to process automatically generated (Acknowledgement RLM Type-1)',
                            'Acknowledgement Type-1 accepted by this beacon'])
    else:
        rotatingbin.append(['161 (Rotating field 7)',
                            bits[7],
                            'Capability to process automatically generated (Acknowledgement RLM Type-1)',
                            'Acknowledgement Type-1 not requested and not accepted by this beacon'])

    if bits[8] == '1':
        rotatingbin.append(['162 (Rotating field 8)',
                            bits[8],
                            'Capability to process manually generated RLM (e.g. Acknowledgement Type-2)',
                            'Manually generated RLM accepted by this beacon'])
    else:
        rotatingbin.append(['162 (Rotating field 8)',
                            bits[8],
                            'Capability to process manually generated RLM (e.g. Acknowledgement Type-2)',
                            'Manually generated RLM not requested and not accepted by this beacon'])

    rotatingbin.append(['163-166 (Rotating field 9-12)',
                        bits[9:13],
                        'Reserved for future use',
                        'Reserved'])

    ##BIT 13-15 (167-169) RLS Provider Identification
    try:
        rlsp = definitions.rls_provider[bits[13:16]]
    except KeyError:
        rlsp = 'Unknown RLS provider'
    rotatingbin.append(['167-169 (Rotating field 13-15)',
                        bits[13:16],
                        'RLS Provider Identification',
                        rlsp])

    ##BIT 16-37 (170-190) Beacon Feedback (acknowledgement of RLM reception)
    if bits[13:16] == '001':
        if bits[16] == '0':
            rotatingbin.append(['170 (Rotating field 16)',
                                bits[16],
                                'RLM Short/Long message identifier',
                                'Short RLM'])
        else:
            rotatingbin.append(['170 (Rotating field 16)',
                                bits[16],
                                'RLM Short/Long message identifier',
                                'Long RLM'])

        rotatingbin.append(['171 (Rotating field 17)',
                            bits[17],
                            'Reserved',
                            'Reserved'])



        if (bits[16] == '0') & (bits[17] == '0'):
            rotatingbin.append(['172-190 (Rotating field 18-37)',
                                bits[18:38],
                                'RLM',
                                'Copy of bits 61-80 of the short RLM in the Open Service Signal in Space (section 5.2 of OS SIS ICD)'])
        else:
            rotatingbin.append(['172-190 (Rotating field 18-37)',
                                bits[18:38],
                                'To be defined',
                                'To be defined'])
    else:
        rotatingbin.append(['170-190 (Rotating field 16-37)',
                            bits[16:38],
                            'Reserved',
                            'Reserved'])

    ##BIT 38-48 (191-202) Unassigned
    if Func.checkzeros(bits[38:]):
        rotatingbin.append(['191-202 (Rotating field 38-48)',
                            bits[38:],
                            'Unassigned',
                            'OK'])
    else:
        rotatingbin.append(['191-202 (Rotating field 38-48)',
                            bits[38:],
                            'Unassigned',
                            'ERROR: Should be all 0s'])

    return rotatingbin



##########################################
# Rotating Field Type: National Use (#3) #
##########################################

def rotating3(bits):
    rotatingbin = []

    #Add a single bit offset so bits array index # matches documentation for readbility
    bits = '0'+ bits

    ##BIT 5-48 (159-202) As defined by national administrations
    if Func.checkzeros(bits[5:]):
        rotatingbin.append(['159-202 (Rotating field 5-48)',
                            bits[5:],
                            'As defined by national administrations',
                            'default'])
    else:
        rotatingbin.append(['159-202 (Rotating field 5-48)',
                            bits[5:],
                            'As defined by national administrations',
                            ''])

    return rotatingbin



###################################################
# Rotating Field Type: Cancellation Message (#15) #
###################################################

def rotating15(bits):
    rotatingbin = []

    #Add a single bit offset so bits array index # matches documentation for readbility
    bits = '0'+ bits

    ##BIT 5-46 (159-200) Fixed
    if Func.checkones(bits[5:47]):
        rotatingbin.append(['159-200 (Rotating field 5-46)',
                            bits[5:47],
                            'Fixed',
                            'OK'])
    else:
        rotatingbin.append(['159-200 (Rotating field 5-46)',
                            bits[5:47],
                            'Fixed',
                            'ERROR: Should be all 1s'])

    ##BIT 47-48 (201-202) Method of deactivation
    deact = definitions.deactivation[bits[47:]]
    rotatingbin.append(['201-202 (Rotating field 47-48)',
                        bits[47:],
                        'Method of deactivation',
                        deact])

    return rotatingbin
