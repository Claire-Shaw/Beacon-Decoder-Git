import decodefunctions as Fcn
### -*- coding: utf-8 -*-
import definitions
import time

class Bch:
    def __init__(self, testbin, mtype):
        bch1 = bch2 = bch1error = bch2error = 'na'
        self.complete = '0'
        if mtype in ['Short Msg', 'Long Msg no Framesynch', 'Long Msg with Framesynch']:
            bch1 = Fcn.calcbch(testbin, "1001101101100111100011", 25, 86, 107)
            bch1error = self.errors(testbin[86:107], bch1)

        if mtype in ['Long Msg no Framesynch', 'Long Msg with Framesynch']:
            bch2 = Fcn.calcbch(testbin, '1010100111001', 107, 133, 145)
            bch2error = self.errors(testbin[133:145], bch2)
            if bch2error == 0:
                self.complete = '1'

        self.bch = (bch1, bch2, testbin[86:107], testbin[133:145], bch1error, bch2error)

    def errors(self, b1, b2):
        e = 0
        for n, bit in enumerate(b1):
            e = e + abs(int(bit) - int(b2[n]))
        return e

    def bcherror(self, n):
        return 'BCH-{} errors: {}'.format(str(n), self.bch[3+int(n)])

    def bch1calc(self):
        return 'BCH-1 Calculated:  {bchcalc}  Errors: {e}'.format(bchcalc=self.bch[0], e=self.bch[4])

    def bch2calc(self):
        return 'BCH-2 Calculated:  {bchcalc}  Errors: {e}'.format(bchcalc=self.bch[1], e=self.bch[5])

    def writebch1(self):
        return 'BCH-1 Encoded: {bch1enc}   BCH-1 Calculated:  {bchcalc}  Errors: {e}'.format(bch1enc=self.bch[2], bchcalc=self.bch[0], e=self.bch[4])
    def writebch2(self):
        return 'BCH-2 Encoded: {bch2enc}   BCH-2 Calculated:  {bchcalc}  Errors: {e}'.format(bch2enc=self.bch[3], bchcalc=self.bch[1], e=self.bch[5])





class HexError(Exception):
    def __init__(self, value, message):
        self.value = value
        self.message = message

    def __str__(self):
        return repr(self.value, self.message)

class Country:
    def __init__(self, midbin):
        mid = Fcn.bin2dec(midbin)
        try:
            cname = definitions.countrydic[mid]
        except KeyError:
            cname = 'Unknown MID'

        #self.result = 'Country Code (bits 27-36) :({b})  Decimal: {d}   Name: {n}.'.format(b=midbin,d=mid,n=cname)
        self._result = (('Country Code:', mid), ('Country Name:', cname))

        self.cname = "{} ({})".format(cname, mid)
        self.mid = mid
    def countrydata(self):
        s = ''
        for t in self._result:
            for c in t:
                s = s + (str(c)) + '  '
            s = s + '     '
        return s




class BeaconHex(HexError):
    "decode beacon message hex"
    def __init__(self, strhex=None):

        if strhex:
            self.processHex(str(strhex))

    def processHex(self, strhex):
        self.bch1 = self.bch2 = self.tac = 'na'
        self.courseloc = ('na', 'na')
        self.location = ('na', 'na')
        self.fixedbits = ''
        self.hex = str(strhex)
        self.count = 1
        #print strhex
        self._loc = False
        self.tablebin = []
        if Fcn.hextobin(strhex):
            if len(strhex) == 15:
                #   15 Hex does not use bit 25 so an extra 0 needs to be padded
                self.type = '15 Hex ID'
                pad = '0'* 25


            elif len(strhex) == 22:
                self.type = 'Short Message'
                pad = '0' * 24
            elif len(strhex) == 30:
                self.type = 'Long Msg no Framesynch'
                pad = '0' * 24
            elif len(strhex) == 36:
                pad = ''
                self.type = 'Long Msg with Framesynch'
            else:
                self.type = 'Hex length of ' + str(len(strhex)) + '.' + '\nLength of First Generation Beacon Hex Code must be 15, 22 or 30'
                raise HexError('LengthError', self.type)
            self.hexcode=str(strhex)            
            
            
            
        else:
            self.type = 'Not a valid Hex ID'
            raise HexError('FormatError',self.type)         
     
        self.bin = '_' + pad + Fcn.hextobin(strhex) + (144 - len(pad + Fcn.hextobin(strhex)))*'0'

        if self.bin[17:25]== '11010000':
            self.testmsg='1'
        else:
            self.testmsg='0'

                
        self.bch=Bch(self.bin,self.type)      
        
        self.id=()
        
        if  self.type !='15 Hex ID':
            formatflag=(self.bin[25],definitions.messagetype[self.bin[25]])            
        else:
            formatflag=('n/a','bit 25 not relevant in 15 Hex')
        
        protocolflag=self.bin[26] 
        self.formatflag=formatflag    
        self.countrydetail=Country(self.bin[27:37])   #self.country()

        #   protocol == '0' :Standard Location Protocol.
        #   type of location protocol is found at bits 37-40
        self._pflag=['Location','User'][int(self.bin[26])]
        self.tablebin.append(['25',self.bin[25],'Message format',self.formatflag[1]])        
        self.tablebin.append(['26',self.bin[26],'User or Location Protocol',self._pflag])
        self.tablebin.append(['27-36',self.bin[27:37],'Country',self.countrydetail.cname])

        
        if protocolflag == '0'  :            
            self.locationProtocol()

        #   protocol == '1' 'User Protocol'
        #   type of user protocol located at bits 37-39    
        elif protocolflag == '1'  :            
            self.userProtocol()
        
        #print self.bin
        
                    
    def has_loc(self):
        return self._loc
    
    def protocolflag(self):
        return self._pflag

    def identdata(self):
        return '  '.join(self._id)
        
    def country(self):
        return self.countrydetail._result
    
 
    def protocoldata(self):
        s=''
        for k in sorted(self._protocold):
            s=s+self._protocold[k]+'        '
            
        return s

    def btype(self):
        return self._btype
    
    def loctype(self):
        return self._loctype

    def userProtocol(self):
        self.hex15=Fcn.bin2hex(self.bin[26:86])
        self.tablebin.append(['26-85',self.bin[26:86],'Beacon UIN',self.hex15])
        self._loctype="User"
        self.encpos='na'
        btype='Unknown Beacon'
        tano='na'

        
        #############################################################################                                                                            #
        #       Bit 37-39: 011: Serial User Protocol                                #
        #       011:    Serial User Protocol                                        #
        #############################################################################

        typeuserprotbin=self.bin[37:40]
        self._loctype=definitions.userprottype[typeuserprotbin]
        
        self._protocol=('Protocol Flag (Bit 26) :'+ self.bin[26],
                       definitions.protocol[self.bin[26]],
                       'User Protocol Type (bits 37-39) : '+typeuserprotbin,
                       definitions.userprottype[typeuserprotbin])

        self._protocold={'pflag':definitions.protocol[self.bin[26]],
                       'ptype' :definitions.userprottype[typeuserprotbin],'serial':''                     
                       }
    
        
                
        if typeuserprotbin=='011':
            #   Bit 37-39: 011: Serial User Protocol (see bits 40 to 42)
            susertype=self.bin[40:43]
            serialtype=definitions.serialusertype[susertype]
            self._protocold['serial']=serialtype
            self.tablebin.append(['37-39',str(self.bin[37:40]),'User protocol type','Serial user'])
            self.tablebin.append(['40-42',str(self.bin[40:43]),'Serial type',serialtype])
            
            #   Bit 43 value 1 - Yes for type approval certificate
            if self.bin[43]=='1':  
                tacert='Bit 43 assisgned. Type Approval at bits 74-84.'
                #   Bits 64-73 all 0 or national use
                #   Bits 74-83 is the Type Approval Certificate Number
                tano=str(Fcn.bin2dec((self.bin)[74:84]))
                
            else:
                #   Bits 64-83 is national use or as defined by other protocl
                tacert='Bit 43 not assisgned - no type approval number in Hex'
                tano='na'

            self.tablebin.append(['43',str(self.bin[43]),'TAC',tacert])


            #   Bits 40-42 : 000 : ELT with Serial Identification
            #   Bits 40-42 : 010 : Float free EPIRB with Serial Identification
            #   Bits 40-42 : 100 : Nonfloat free EPIRB with Serial Identification
            #   Bits 40-42 : 110 : PLB with Serial Identification                
            #   Serial ID is from bit 44-63
            
            if susertype in ['000','010','100','110']:
                s1,s2=('Bits 64-73 : '+(self.bin[64:74]),
                          'Serial ID Decimal Value: ' + str(Fcn.bin2dec(self.bin[44:64]))                          
                          )
                auxradiodevice='Aux Radio Device: '+self.bin[84:86]+' '+definitions.auxlocdevice[self.bin[84:86]]
                
                if susertype in ['010','100']:
                    btype='EPIRB'
                elif susertype=='000':
                    btype='ELT'
                elif susertype=='110':
                    btype='PLB'
                self.tablebin.append(['44-63',str(self.bin[44:64]),'Serial Number',str(Fcn.bin2dec(self.bin[44:64]))])
                self.tablebin.append(['64-73',str(self.bin[64:74]),'National use',str(Fcn.bin2dec(self.bin[64:74]))])
                
             
            #   For Serial User Protocol
            #   Bit 40-42 : 011:   ELT with Aircraft 24-bit Address     
            if susertype == '011' : 
                btype,s1,s2=('ELT','Aircraft 24 bit Address (bits 44-67) :Dec value: '+ str(Fcn.bin2dec(self.bin[44:68]))+ '  Hex Value  : '+ Fcn.bin2hex(self.bin[44:68]),
                            'Number of Additional ELTs (bits 68-73):'+str(Fcn.bin2dec(self.bin[68:74])))
                auxradiodevice='Aux Radio Device: '+self.bin[84:86]+' '+definitions.auxlocdevice[self.bin[84:86]]
                emergencycode='Emergency Code (109-112): '
                self.tablebin.append(['44-67',str(self.bin[44:68]),'AirCraft 24 bit identification',str(Fcn.bin2dec(self.bin[44:68]))]) 


            #   Bit 40-42 : 001 : Aircraft operator designator and serial number
            #   Aircraft Operator is in bits 44-61
            #   Serial ID is from bit 62-73
            
            if susertype == '001' :
                btype,s1,s2=('ELT','AirCraft Operator Designator : '+ Fcn.baudot(self.bin,44,62),
                          'Serial # Assigned by Operator: ' + str(Fcn.bin2dec(self.bin[62:74])))
                auxradiodevice='Aux Radio Device: '+self.bin[84:86]+' '+definitions.auxlocdevice[self.bin[84:86]]
                self.tablebin.append(['44-61',str(self.bin[44:62]),'AirCraft Operator Designator',Fcn.baudot(self.bin,44,62)])
                self.tablebin.append(['62-73',str(self.bin[62:74]),'Serial No Assigned by Operator',str(Fcn.bin2dec(self.bin[62:74]))])
            if susertype in ['111','101']:
                self.tablebin.append(['44-73',str(self.bin[44:74]),'Unknown Serial type',''])
                
            
            self._protocol=('Protocol Flag (Bit 26) :'+ self.bin[26],
                           definitions.protocol[self.bin[26]],
                           typeuserprotbin,definitions.userprottype[typeuserprotbin],
                           susertype,serialtype)
                                     
                       

            self.typeapproval=(tacert,'Type Approval ',str(tano))  
            
            
            
            self.tablebin.append(['74-83',str(self.bin[74:84]),'Type approval certificate No',tano])
            self.tablebin.append(['84-85',str(self.bin[84:86]),'Auxiliary radio device',definitions.auxlocdevice[self.bin[84:86]]])
                 
        #############################################################################
        #       Bit 37-39: 000 Orbitography User Protocol                           #
        #############################################################################  

        elif typeuserprotbin=='000' :
            self.tablebin.append(['37-39',str(self.bin[37:40]),'User protocol type',definitions.userprottype[typeuserprotbin]])
            btype='Orbitography'
            self.tablebin.append(['40-85',str(self.bin[40:86]),'Identification',str(Fcn.bin2hex(self.bin[40:88]))])
            self.tablebin.append(['86-106',str(self.bin[86:107]),'BCH 1',str(self.bch.bch1calc())])
            self.tablebin.append(['107-132',str(self.bin[107:133]),'Reserved','Reserved for national use'])            
            self.tablebin.append(['133-144',str(self.bin[133:145]),'BCH 2',str(self.bch.bch2calc())])

        #############################################################################
        #       Bit 37-39: 001 ELT Aviation User Protocol                           #
        #############################################################################        

        elif typeuserprotbin=='001' :
            self.tablebin.append(['37-39',str(self.bin[37:40]),'User protocol type','ELT Aviation User'])
            aircraftid=Fcn.baudot(self.bin,40,82)
            self.tablebin.append(['40-81',str(self.bin[40:82]),'Aircraft ID',aircraftid])
            self.tablebin.append(['82-83',str(self.bin[82:84]),'ELT No',str(Fcn.bin2dec(self.bin[82:84]))])
            self.tablebin.append(['84-85',str(self.bin[84:86]),'Auxiliary radio device',definitions.auxlocdevice[self.bin[84:86]]])
            btype='ELT'
              
            
        #############################################################################
        #       Bit 37-39: 111 : Test User protocol                                 #
        #############################################################################
        
        elif typeuserprotbin=='111':
            self.tablebin.append(['37-39',str(self.bin[37:40]),'User protocol type','Test user'])
            self.tablebin.append(['40-85',str(self.bin[40:86]),'National use',''])
            btype='Test'
            
        #############################################################################
        #   Bit 37-39: 110 : Radio Call Sign xxx                                    #
        #############################################################################       
        elif typeuserprotbin=='110':
            btype='EPIRB'
            mmsi=bcd=emergencycode=''            
            m=self.bin[40:76]
            pad=''
            if Fcn.bin2dec(self.bin[72:76])<10:
                pad=str(Fcn.bin2dec(self.bin[72:76]))            
            radiocallsign=Fcn.baudot(self.bin,40,64)+str(Fcn.bin2dec(self.bin[64:68])) + str(Fcn.bin2dec(self.bin[68:72]))+pad            
            self.tablebin.append(['37-39',str(self.bin[37:40]),'User protocol type',definitions.userprottype[typeuserprotbin]])
            self.tablebin.append(['40-75',str(self.bin[40:76]),'Radio call sign',radiocallsign])
            self.tablebin.append(['76-81',str(self.bin[76:82]),'Beacon No',self.bin[76:82]+': ' + Fcn.baudot(self.bin,76,82)])
            self.tablebin.append(['82-83',str(self.bin[82:84]),'Spare No',str(Fcn.bin2dec(self.bin[82:84]))])
            self.tablebin.append(['84-85',str(self.bin[84:86]),'Auxiliary radio device',definitions.auxlocdevice[self.bin[84:86]]])

        #############################################################################
        #   Bit 37-39: 010 Maritime User Protocol                                   #
        #############################################################################               
        elif typeuserprotbin=='010' :
            mmsi='MMSI: '+ Fcn.baudot(self.bin,40,76)
            btype='EPIRB'          
            
            self.tablebin.append(['37-39',str(self.bin[37:40]),'User protocol type',definitions.userprottype[typeuserprotbin]])
            self.tablebin.append(['40-75',str(self.bin[40:76]),'MMSI',Fcn.baudot(self.bin,40,76)])
            self.tablebin.append(['76-81',str(self.bin[76:82]),'Beacon No',self.bin[76:82]+': ' + Fcn.baudot(self.bin,76,82)])
            self.tablebin.append(['82-83',str(self.bin[82:84]),'Spare No',str(Fcn.bin2dec(self.bin[82:84]))])
            self.tablebin.append(['84-85',str(self.bin[84:86]),'Auxiliary radio device',definitions.auxlocdevice[self.bin[84:86]]])


        ##############################################################################
        #   Bit 37-39: 100  National User Protocol                                   #
        ##############################################################################        
        elif typeuserprotbin=='100' :
            self._protocol=(self.bin[26],definitions.protocol[self.bin[26]],typeuserprotbin,definitions.userprottype[typeuserprotbin])
            
            self.tablebin.append(['37-39',str(self.bin[37:40]),'User protocol type',definitions.userprottype[typeuserprotbin]])
            self.tablebin.append(['40-85',str(self.bin[84:86]),'Reserved','Reserved for national use'])
            self.tablebin.append(['86-106',str(self.bin[86:107]),'BCH 1',str(self.bch.bch1calc())])
            self.tablebin.append(['107-112',str(self.bin[107:113]),'Reserved','Reserved for national use'])
            self.tablebin.append(['113-132',str(self.bin[113:133]),'Reserved','Reserved for national use'])
            self.tablebin.append(['133-144',
                                  str(self.bin[133:145]),
                                      'BCH 2',
                                      str(self.bch.bch2calc())])


        if typeuserprotbin not in ['100','000'] : # and self.bch.complete=='1':            
            location_data = 'Check for location'
            self.encpos=str(self.bin[107])
            lat,declat, latdir,ltminutes=Fcn.latitude(self.bin[108],self.bin[109:116],self.bin[116:120])
            lg,declng, lngdir,lgminutes=Fcn.longitude(self.bin[120],self.bin[121:129],self.bin[129:133])
            
            self.tablebin.append(['86-106',str(self.bin[86:107]),'BCH 1',str(self.bch.bch1calc())])
            self.tablebin.append(['107',str(self.bin[107]),'Encoded location source',definitions.enc_delta_posflag[self.encpos]])
            
            if Fcn.is_number(declat) and Fcn.is_number(declng):
                self._loc=True
                a = self.update_locd(declat,latdir)
                b = self.update_locd(declng,lngdir)                
                
            else:
                a = declat
                b = declng
            self.location=(a,b)
            self.tablebin.append(['108-119',str(self.bin[108:120]),'Latitude','{} (decimal: {})'.format(lat,a)])                               
            self.tablebin.append(['120-132',str(self.bin[120:133]),'Longitude','{} (decimal: {})'.format(lg,b)])
            self.tablebin.append(['','','Resolved location','{} {}'.format(a,b)])
                
                
            self.tablebin.append(['133-144',
                                  str(self.bin[133:145]),
                                      'BCH 2',
                                      str(self.bch.bch2calc())])      
        

        
        self._btype=btype

        
    def update_locd(self,_dec,_dir):        
        return '{:.3f}'.format(Fcn.latlongdir(_dir)*float(abs(_dec)))

    def locationProtocol(self):      
        
        typelocprotbin=self.bin[37:41]        
        self._locd=dict(lat='not provided',long='not provided',comp='')                          
        tano='na'
        self.encpos='na'
        if typelocprotbin in ['0010','0110','1010','1100']:
            btype='EPIRB'
        elif typelocprotbin in ['0011','0101','0100','1000','1001']:
            btype='ELT'
        elif typelocprotbin in ['0111','1011']:
            btype='PLB'
        elif typelocprotbin=='1110':
            btype='Std Loc Test'
        elif typelocprotbin=='1111':
            btype='Nat Loc Test'
        elif typelocprotbin=='1101' :
            if self.bin[41:43] == '00' :
                btype='ELT'
            elif self.bin[41:43] == '01' :
                btype='EPIRB'
            elif self.bin[41:43] == '10' :
                btype='PLB'
            elif self.bin[41:43] == '11':
                btype='RLS Loc Test'
                
        else:
            btype='Unknown'
       

        self._protocold={'pflag':definitions.protocol[self.bin[26]],
                       'ptype' :definitions.locprottype[typelocprotbin],'serial':''                     
                       }

       
        self._protocol=('Protocol Flag (Bit 26) :'+ self.bin[26],definitions.protocol[self.bin[26]],
                       'Location Protocol type (bits 37-40) : '+typelocprotbin,
                       definitions.locprottype[typelocprotbin],typelocprotbin)
   
                
   
        ident=('')
        
        #Standard Location protocols
        if typelocprotbin in definitions.stdloctypes : #['0010','0011','0100','0101','0110','0111','1100','1110']
            default='011111111101111111111'
            self._loctype='Standard Location'
            
            self.hex15=Fcn.bin2hex(self.bin[26:65]+default)
            self.tablebin.append(['37-40',str(self.bin[37:41]),'Location protocol', definitions.locprottype[typelocprotbin]])
            self.tablebin.append(['26-85',self.bin[26:65]+default,'Beacon UIN',self.hex15])
            latdelta,longdelta,ltoffset,lgoffset = Fcn.latlongresolution(self.bin,113,133)
            lat,declat, latdir,ltminutes=Fcn.latitude(self.bin[65],self.bin[66:73],self.bin[73:75])
            lng,declng, lngdir,lgminutes=Fcn.longitude(self.bin[75],self.bin[76:84],self.bin[84:86])          
            self.courseloc=(declat,declng)

            
            #   EPIRB MMSI
            if typelocprotbin=='0010':                
                ident=('MMSI ID Number: ',str(Fcn.bin2dec(self.bin[41:61])),'Specific Beacon :',str(Fcn.bin2dec(self.bin[61:65])))
                self.tablebin.append(['41-60',str(self.bin[41:61]),'MMSI ID No',str(Fcn.bin2dec(self.bin[41:61]))])
                self.tablebin.append(['61-64',str(self.bin[61:65]),'Specific beacon No',str(Fcn.bin2dec(self.bin[61:65]))])
         

            #   ELT 24 bit address
            elif typelocprotbin=='0011':
                
                
                self.tablebin.append(['41-64',str(self.bin[41:65]),'Aircraft ID No','{} ({})'.format(str(Fcn.bin2dec(self.bin[41:65])),str(Fcn.bin2hex(self.bin[41:65])))])

            #   ELT - Aircraft Operator Designator Standard Location Protocol
            elif typelocprotbin=='0101':
                
                
                self.tablebin.append(['41-64',str(self.bin[41:65]),
                                      'ELT Operator ID',
                                      '{} ELT No:{}'.format(str(Fcn.baudot(self.bin,41,55,True)),str(Fcn.bin2dec(self.bin[56:65])))])

            
            #   PLB, ELT and EBIRB Serial
            elif typelocprotbin in ['0100','0110','0111']:                
                self.tablebin.append(['37-40',str(self.bin[37:41]),'Location protocol','Serial {}'.format(btype)])
                self.tablebin.append(['41-50',str(self.bin[41:51]),'Type approval certificate',str(Fcn.bin2dec(self.bin[41:51]))])
                self.tablebin.append(['51-64',str(self.bin[51:65]),'Serial No',str(Fcn.bin2dec(self.bin[51:65]))])

            elif typelocprotbin == '1110':                
                self.tablebin.append(['41-65',str(self.bin[41:66]),'No decode identification',definitions.locprottype[typelocprotbin]])
                

            if self.type!='15 Hex ID':
                self.tablebin.append(['65-74',str(self.bin[65:75]),'Latitude','{} ({})'.format(lat,declat)])
                self.tablebin.append(['75-85',str(self.bin[75:86]),'Longitude','{} ({})'.format(lng,declng)])

                
                if self.bin[107:111]=='1101':
                    computed='107-110 should be 1101.  Passed.'
                else:
                    computed= '107-110 :'  + self.bin[107:111] + '. Not  1101. Failed'

                self.fixedbits=computed
                self.tablebin.append(['86-106',str(self.bin[86:107]),'BCH 1',str(self.bch.bch1calc())])
                self.tablebin.append(['107-110',str(self.bin[107:111]),'Validity',computed])
                self.tablebin.append(['111',
                                      str(self.bin[111]),
                                          'Encoded position',
                                          definitions.enc_delta_posflag[self.bin[111]]])

                self.tablebin.append(['112',
                                      str(self.bin[112]),
                                          'Aux device',
                                          definitions.homer[self.bin[112]]])
                self.encpos=str(self.bin[111])
                self.tablebin.append(['113-122',
                                      str(self.bin[113:123]),
                                          'Latitude offset', ltoffset])
                                          

                self.tablebin.append(['123-132',
                                      str(self.bin[123:133]),
                                          'Longitude offset', lgoffset])
                                          

                self.tablebin.append(['133-144',
                                      str(self.bin[133:145]),
                                          'BCH 2',
                                          str(self.bch.bch2calc())])                             
            
            elif self.type=='15 Hex ID':
                self.tablebin.append(['65-85',default,'Default bits',''])                
            

        #   National Location protocols - PLB, ELT and EPIRB
        elif typelocprotbin in definitions.natloctypes: #['1000','1010','1011','1111']:            
            
           
            self._loctype='National Location'                         
            self.tablebin.append(['37-40',str(self.bin[37:41]),'Location protocol','{} {}'.format(btype,self._loctype)])                
            default='011111110000001111111100000' #59-85 default data 27 bit binary (to construct 15 Hex UIN when no location present)
            self.hex15=Fcn.bin2hex(self.bin[26:59]+default)
            self.tablebin.append(['26-85',self.bin[26:59]+default,'Beacon UIN',self.hex15])
            ident= ('Serial Number :',str(Fcn.bin2dec(self.bin[41:59])))            
            self.tablebin.append(['41-58',str(self.bin[41:59]),'Serial No','#{}'.format(str(Fcn.bin2dec(self.bin[41:59])))])
            latdelta,longdelta,ltmin,ltsec,lgmin,lgsec,ltoffset,lgoffset =(0,0,0,0,0,0,0,0)
            lat,declat,latdir,ltminutes =  Fcn.latitude(self.bin[59],self.bin[60:67],self.bin[67:72])           
            lng,declng,lngdir,lgminutes =  Fcn.longitude(self.bin[72],self.bin[73:81],self.bin[81:86])
            self.courseloc=(declat,declng)
            if self.type!='15 Hex ID':
                self.tablebin.append(['59-71',str(self.bin[59:72]),'Latitude','{} ({})'.format(lat,declat)])
                self.tablebin.append(['72-85',str(self.bin[72:86]),'Longitude','{} ({})'.format(lng,declng)])
                self.tablebin.append(['86-106',str(self.bin[86:107]),'BCH 1',str(self.bch.bch1calc())])                
                if self.bin[107:110]=='110':
                    computed='107-109 should be 110.  Passed.'
                else:
                    computed= '107-109 :'  + self.bin[107:110] + '. Not  110. Failed'
                self.tablebin.append(['107-109',str(self.bin[107:110]),'Validity',computed])
                self.fixedbits=computed
                finallat=finallng='Not Used'            
                self._locd['encpos']=definitions.enc_delta_posflag[self.bin[111]]
            
                if self.bin[110]=='0':
                    self._locd['comp']='Value 0: bits 113-132 for national use'
                    latdelta=longdelta=0
                    self.tablebin.append(['110',str(self.bin[110]),
                                          'Location check',
                                          self._locd['comp']])
                    self.tablebin.append(['111',
                                          str(self.bin[111]),
                                          'Location source',
                                          self._locd['encpos']])
                    
                    self.tablebin.append(['112',
                                          str(self.bin[112]),
                                          'Aux device',
                                          definitions.homer[self.bin[112]]])
                    self.tablebin.append(['113-132',
                                      str(self.bin[113:133]),
                                          'National use',''])


                    
                else:
                    
                    latdelta,longdelta,ltoffset,lgoffset = Fcn.latlongresolution(self.bin,113,127)


                    self.tablebin.append(['110',str(self.bin[110]),
                                          'Location check',
                                          'bits 113-126 for location.\n 127-132 for national use'])
                    
                    self.tablebin.append(['111',
                                          str(self.bin[111]),
                                          'Location source',
                                          definitions.enc_delta_posflag[self.bin[111]]])
                    self.encpos=str(self.bin[111])
                    self.tablebin.append(['112',
                                          str(self.bin[112]),
                                          'Aux device',
                                          definitions.homer[self.bin[112]]])

                
                    self.tablebin.append(['113-119',str(self.bin[113:120]),'Latitude offset',ltoffset])                                        

                    self.tablebin.append(['120-126',str(self.bin[120:127]),'Longitude offset',lgoffset])
                    self.tablebin.append(['127-132',
                                      str(self.bin[127:133]),
                                          'National use',''])


                self.tablebin.append(['133-144',
                                  str(self.bin[133:145]),
                                      'BCH 2',
                                      str(self.bch.bch2calc())])

            elif self.type=='15 Hex ID':
                self.tablebin.append(['59-85',default,'Default bits',''])
            
            
            
        # RLS Location Protocol 
        elif typelocprotbin =='1101':
            default='0111111110111111111' #67-85 default 19 bit binary (to construct 15 Hex UIN when no location present)
            self.hex15=Fcn.bin2hex(self.bin[26:67]+default)
            self.tablebin.append(['26-85',self.bin[26:59]+default,'Beacon UIN',self.hex15])          
            self._loctype='RLS Location'                
            self.tablebin.append(['37-40',str(self.bin[37:41]),'Location protocol','{} {}'.format(btype,self._loctype)])            
            tano=str(Fcn.bin2dec(self.bin[43:53]))
            self.tablebin.append(['41-42',str(self.bin[41:43]),'Beacon type',btype])
            self.tablebin.append(['43-52',str(self.bin[43:53]),'RLS Tac No','#{}'.format(tano)])                      
            self.tablebin.append(['53-66',str(self.bin[53:67]),'Serial No','#{}'.format(str(Fcn.bin2dec(self.bin[53:67])))])
            latdelta,longdelta,ltmin,ltsec,lgmin,lgsec,ltoffset,lgoffset =(0,0,0,0,0,0,0,0)
            lat,declat,latdir =  Fcn.latitudeRLS(self.bin[67],self.bin[68:76])           
            lng,declng,lngdir =  Fcn.longitudeRLS(self.bin[76],self.bin[77:86])
            self.courseloc=(declat,declng)
            if self.type!='15 Hex ID':
                self.tablebin.append(['67-75',str(self.bin[67:76]),'Latitude','{} ({})'.format(lat,declat)])
                self.tablebin.append(['76-85',str(self.bin[76:86]),'Longitude','{} ({})'.format(lng,declng)])
                self.tablebin.append(['86-106',str(self.bin[86:107]),'BCH 1',str(self.bch.bch1calc())])
                self.tablebin.append(['107-108',str(self.bin[107:109]),'supplementary','supplementary'])
                self._locd['encpos']=definitions.enc_delta_posflag[self.bin[107]]
                self.encpos=str(self.bin[107])
                self._locd['homer']=definitions.homer[self.bin[108]]
                self.tablebin.append(['107',str(self.bin[107]),'encoded position source',self._locd['encpos']])
                self.tablebin.append(['108',str(self.bin[108]),'homer',self._locd['homer']])
                self.tablebin.append(['109-114',str(self.bin[109:115]),'reserved','reserved for RLS data'])                
                finallat=finallng='Not Used'                    
                latdelta,longdelta,ltoffset,lgoffset = Fcn.latlongresolution(self.bin,115,133)            
                self.tablebin.append(['115-123',str(self.bin[115:124]),'Latitude offset',ltoffset])
                self.tablebin.append(['124-132',str(self.bin[124:133]),'Longitude offset',lgoffset])
                self.tablebin.append(['133-144',
                                  str(self.bin[133:145]),
                                      'BCH 2',
                                      str(self.bch.bch2calc())])
            elif self.type=='15 Hex ID':
                self.tablebin.append(['67-85',default,'Default bits',''])



            
        # ELT-DT Location Protocol   
        elif typelocprotbin == '1001':
            default='0111111110111111111' #67-85 default 19 bit binary (to construct 15 Hex UIN when no location present)
            self.hex15=Fcn.bin2hex(self.bin[26:67]+default)
            self.tablebin.append(['26-85',self.bin[26:59]+default,'Beacon UIN',self.hex15])
            self._loctype='ELT-DT Location'
            self.tablebin.append(['37-40',str(self.bin[37:41]),'Location protocol','{} {}'.format(btype,self._loctype)])            
            self.tablebin.append(['41-42',str(self.bin[41:43]),'ELT Type',definitions.eltdt[str(self.bin[41:43])]])
            if str(self.bin[41:43])=='10':
                tano=str(Fcn.bin2dec(self.bin[43:53]))
                self.tablebin.append(['43-52',str(self.bin[43:53]),'Tac No','#{}'.format(tano)])                      
                self.tablebin.append(['53-66',str(self.bin[53:67]),'Serial No','#{}'.format(str(Fcn.bin2dec(self.bin[53:67])))])
            elif str(self.bin[41:43])=='00':                
                self.tablebin.append(['43-66',str(self.bin[43:67]),'Aircraft 24 bit address','#{}'.format(str(Fcn.bin2dec(self.bin[43:67])))])
            elif str(self.bin[41:43])=='01':
                self.tablebin.append(['43-60',str(self.bin[43:61]),'AirCraft Operator Designator',Fcn.baudot(self.bin,43,61)])
                self.tablebin.append(['61-66',str(self.bin[61:67]),'Serial No Assigned by Operator',str(Fcn.bin2dec(self.bin[61:67]))])
            elif str(self.bin[41:43])=='11':
                self.tablebin.append(['43-66',str(self.bin[43:67]),'ELT(DT) Location Test Protocol','reserved'])

            latdelta,longdelta,ltmin,ltsec,lgmin,lgsec,ltoffset,lgoffset =(0,0,0,0,0,0,0,0)
            lat,declat,latdir =  Fcn.latitudeRLS(self.bin[67],self.bin[68:76])           
            lng,declng,lngdir =  Fcn.longitudeRLS(self.bin[76],self.bin[77:86])
            self.courseloc=(declat,declng)

            if self.type!='15 Hex ID':
                self.tablebin.append(['67-75',str(self.bin[67:76]),'Latitude','{} ({})'.format(lat,declat)])
                self.tablebin.append(['76-85',str(self.bin[76:86]),'Longitude','{} ({})'.format(lng,declng)])
                self.tablebin.append(['86-106',str(self.bin[86:107]),'BCH 1',str(self.bch.bch1calc())])
                means = {'01':'automatic','11':'manual','00':'spare','10':'spare'}
                meansbin = str(self.bin[107:109])
                self.tablebin.append(['107-108',meansbin,'means of activation',means[meansbin]])                                            
                enc_altbin=str(self.bin[109:113])
                enc_altstr='altitude is between {} and {}'.format(definitions.enc_alt[enc_altbin][0],definitions.enc_alt[enc_altbin][1])
                self.tablebin.append(['109-112',enc_altbin,'encoded altitude',enc_altstr])                
                finallat=finallng='Not Used'
                enc_loc_fresh = {'01':'old','11':'current','00':'old','10':'old'}
                enc_freshbin=str(self.bin[113:115])
                self.tablebin.append(['113-114',enc_freshbin,'encoded location freshness',enc_loc_fresh[enc_freshbin]])                
                latdelta,longdelta,ltoffset,lgoffset = Fcn.latlongresolution(self.bin,115,133)            
                self.tablebin.append(['115-123',str(self.bin[115:124]),'Latitude offset',ltoffset])
                self.tablebin.append(['124-132',str(self.bin[124:133]),'Longitude offset',lgoffset])
                self.tablebin.append(['133-144',
                                  str(self.bin[133:145]),
                                      'BCH 2',
                                      str(self.bch.bch2calc())])
            elif self.type=='15 Hex ID':
                self.tablebin.append(['67-85',default,'Default bits',''])

        if Fcn.is_number(declat) and Fcn.is_number(latdelta) and Fcn.is_number(declng) and Fcn.is_number(longdelta):
            self._loc=True
            a=self.update_locd((abs(declat)+latdelta),latdir)         
            b=self.update_locd((abs(declng)+longdelta),lngdir)
        else:
            self._loc=False
            a=declat
            b=declng

            

        self.tablebin.append(['','','Composite location','{} {}'.format(a,b)])
        self.location=(a,b)        
        self._btype=btype
        self.tac=tano

        




    
