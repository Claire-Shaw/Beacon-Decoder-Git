# -*- coding: cp1252 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_beaconhex
import ui_map
import ui_progress

import os
import html
import decodehex2
import definitions
import sys
##import psutil

import Gen2secondgen as Gen2
import Gen2functions




class MapDlg(QDialog, ui_map.Ui_Dialog):
    def __init__(self, parent=None):
        super(MapDlg, self).__init__(parent)
        msize = '15 digit beacon UIN'
        self.setupUi(self)

        self._lat = 0
        self._long = 0
        self.currentframe = self.mapWebView.page().currentFrame()
        self.mapWebView.loadFinished.connect(self.handleLoadFinished)

    def set_code(self, html):
        self.mapWebView.setHtml(html)

    def handleLoadFinished(self, ok):
        if ok:
            self.get_marker_coordinates()


    def get_marker_coordinates(self):
        self.currentframe.evaluateJavaScript('Marker({0},{1})'.format(self._lat, self._long))
        self.setWindowTitle("Latitude:  {}   Longitude:  {}".format(self._lat, self._long))




class Progress(QDialog, ui_progress.Ui_Dialog):
    def __init__(self, parent=None):
        super(Progress, self).__init__(parent)
        self.setupUi(self)




    def updateProgress(self, val):
        self.progressBar.setValue(val)
        if val > 99:
            self.close()




class MainWindow(QMainWindow, ui_beaconhex.Ui_BeaconDecoder):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self._mtype = 'Hex15'
        self.setupUi(self)


        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)    # File only, not registry
        self.updateUi()


    def closeEvent(self, event):
        event.accept()
        sys.exit()


    @pyqtSignature("")
    def on_pushButton_clicked(self):
        self.dialog = MapDlg(self)
        self.dialog.show()
        if self._beacon.has_loc():
            h = html.google_map
            self.dialog._lat = unicode(self._beacon.location[0])
            self.dialog._long = unicode(self._beacon.location[1])
        else:
            h = html.blank
        self.dialog.set_code(h)
        if self.dialog.exec_():
            self.dialog.close()




    @pyqtSignature("QString")
    def on_hexLineEdit_textChanged(self):
        c = self.hexLineEdit.cursorPosition()
        t = unicode(self.hexLineEdit.text()).upper()
        self.hexLineEdit.setText(t)
        self.hexLineEdit.setCursorPosition(c)
        self.hexLineEdit.setSelection(c, 1)
        hexcode = unicode(self.hexLineEdit.text())
        self._lasthex = hexcode

        if len(hexcode) == 63 or len(hexcode) == 51 or len(hexcode) == 75:
            self._beacon = Gen2.SecondGen(hexcode)
        else:
            self._beacon = decodehex2.BeaconHex()
        try:
            self._beacon.processHex(hexcode)
            ctry = self._beacon.country()
            mid = unicode(ctry[0][1])
            name = unicode(ctry[1][1])
            self.tableWidget.clear()

            for n, lrow in enumerate(self._beacon.tablebin):
                for m, item in enumerate(lrow):
                    newitem = QTableWidgetItem(item)
                    newitem.setFlags(Qt.ItemIsEnabled)
                    self.tableWidget.setItem(n, m, newitem)
            self.tableWidget.setHorizontalHeaderLabels(['Bit range',
                                                        'Bit value',
                                                        'Name',
                                                        'Decoded'])
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()

        except Gen2.Gen2Error as e:
            self.tableWidget.clear()
            qb = QMessageBox.critical(self, e.value, e.message)

        except decodehex2.HexError as e:
            self.tableWidget.clear()
            qb = QMessageBox.critical(self, e.value, e.message)

        finally:
            pass





    def pickHex(self, item):
        s = unicode(item.text())
        # QMessageBox.information(self, "ListWidget", "You clicked: "+s)
        self.hexLineEdit.setText(s.split()[1])


    def updateUi(self):
        self.statusBar().showMessage('Ready')
        self._beacon = decodehex2.BeaconHex()
        # Create main menu
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu('&File')
        # Add open file
        openButton = QAction('&Open', self)
        openButton.setShortcut('Ctrl+O')
        openButton.setStatusTip('Open a file')
        openButton.setStatusTip('Select file with hexidecimal codes')
        openButton.triggered.connect(self.file_dialog)
        # Add save file
        saveButton = QAction('&Save (First Generation)', self)
        saveButton.setShortcut('Ctrl+S')
        saveButton.setStatusTip('Export decoded')
        saveButton.setStatusTip('Export decoded file')
        saveButton.triggered.connect(self.filesave_dialog)

        # Add save file
        save2GenButton = QAction('&Save (Second Generation)', self)
        save2GenButton.setShortcut('Ctrl+Shift+S')
        save2GenButton.setStatusTip('Export decoded')
        save2GenButton.setStatusTip('Export decoded file')
        save2GenButton.triggered.connect(self.secondgen_filesave_dialog)

        # Add exit button
        exitButton = QAction('&Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)

        fileMenu.addAction(openButton)
        fileMenu.addAction(saveButton)
        fileMenu.addAction(save2GenButton)
        fileMenu.addAction(exitButton)



        hexRe = QRegExp(r"[0-9a-fA-F_]{"+'75'+"}")
        self.hexLineEdit.setText('')
        self.hexLineEdit.setValidator(
            QRegExpValidator(hexRe, self))

        #exitAction = QAction(r"c:\\decodeUI\\Ver4\\open.png", 'Exit program', self)

        #exitAction.triggered.connect(self.close)

        #self.toolbar = self.addToolBar("Exit")
        #self.toolbar.addAction(exitAction)




        self.hexlist.itemClicked.connect(self.pickHex)
        self.hexlist.currentItemChanged.connect(self.pickHex)

    def filesave_dialog(self):

        fd = QFileDialog(self)
        self.filesave = fd.getSaveFileName(self, "Export decode file", "", 'Save export as csv (*.csv)')

        if self.filesave != '':
            self.export_secondgen = False
            self.threadclass = ThreadClassSave(self.filename, self.filesave,self.export_secondgen)
            self.threadclass.start()
            self.connect(self.threadclass, SIGNAL('EXPORT'), self.threadclass.updateProgress)

    def secondgen_filesave_dialog(self):

        fd = QFileDialog(self)
        self.filesave = fd.getSaveFileName(self, "Export decode file", "", 'Save export as csv (*.csv)')

        if self.filesave != '':
            self.export_secondgen = True
            self.threadclass = ThreadClassSave(self.filename, self.filesave, self.export_secondgen)
            self.threadclass.start()
            self.connect(self.threadclass, SIGNAL('EXPORT'), self.threadclass.updateProgress)

    def file_dialog(self):
        fd = QFileDialog(self)
        self.filename = fd.getOpenFileName()
        from os.path import isfile
        if isfile(self.filename):
            self.tableWidget.clear()
            self.hexlist.clear()
            self.threadclass = ThreadClassOpen(self.filename, self.hexlist)
            self.threadclass.start()
            self.connect(self.threadclass, SIGNAL('LOAD'), self.threadclass.updateProgress)




class ThreadClassOpen(QThread):
    def __init__(self, filename, hexlist, parent=None):
        super(ThreadClassOpen, self).__init__(parent)


        self.filename = filename
        self.hexlist = hexlist
        self.dialog = Progress()
        self.dialog.show()


    def run(self):
        self.emit(SIGNAL('LOAD'), 50)
        hexcodes = open(self.filename, 'r')

        content = ['{num:05d}  {h}'.format(num=n+1, h=x.strip('\n')) for n, x in enumerate(hexcodes.readlines())]
        self.emit(SIGNAL('LOAD'), 95)
        self.hexlist.addItems(content)
        self.emit(SIGNAL('LOAD'), 100)

        if self.dialog.exec_():
            self.dialog.close()

    def updateProgress(self, val):
        self.dialog.updateProgress(val)




class ThreadClassSave(QThread):
    """
    Thread class is used to show progress bar since export can take several seconds.
    Otherwise user may think the system is frozen.
    """
    def __init__(self, filename, filesave, secgen, parent=None):
        super(ThreadClassSave, self).__init__(parent)
        self.filename = filename
        self.filesave = filesave
        self.dialog = Progress()
        self.dialog.show()
        self.secgen = secgen


    def run(self):

        count = 0
        thefile = open(self.filename, 'rb')
        while 1:
            buffer = thefile.read(8192*1024)
            if not buffer: break
            count += buffer.count('\n')
        thefile.close()
        print count
        hexcodes = open(self.filename)
        decoded = open(self.filesave, 'w')



        i = 0

        ###SECOND GENERATION EXPORT
        if self.secgen == True:

            c = Gen2.SecondGen()

            decoded.write("""Input Message,Self Test,23 Hex ID,BCH Errors,Vessel ID,TAC,Country Code,Country Name,Latitude,Longitude\n""")

            for line in hexcodes.readlines():
                i += 1
                #print i, count, i/float(count),i/float(count)*100
                self.emit(SIGNAL('EXPORT'), i/float(count)*100)
                line = str(line.strip())

                decoded.write('{h},'.format(h=str(line)))

                try:
                    c.processHex(str(line))

                    ##Self Test
                    decoded.write('{},'.format(c.bits[42]))
                    ##23 Hex ID
                    decoded.write('{},'.format(c.beaconHexID))
                    ##BCH Errors
                    decoded.write('{},'.format(c.BCHerrors))
                    ##Vessel ID
                    decoded.write('{},'.format(Gen2functions.bin2dec(c.vesselID)))
                    ##TAC
                    decoded.write('{},'.format(c.tac))
                    ##Country Code
                    decoded.write('{},'.format(c.countryCode))
                    ##Country Name
                    decoded.write('{},'.format(c.countryName))
                    ##Latitude
                    decoded.write('{},'.format(c.latitude[1]))
                    ##Longitude
                    decoded.write('{},'.format(c.longitude[1]))


                except Gen2.Gen2Error as e2:
                    decoded.write(e2.value)

                decoded.write('\n')


        ##FIRST GENERATION EXPORT
        else:
            c = decodehex2.BeaconHex()

            decoded.write("""Input Message,Self Test,15 Hex ID,Complete,Test Coded,Beacon Type,TAC,Country Code,Country Name,Location Type,Position Source,Course Lat,Course Long,Final Lat,Final Long,Fixed Bits\n""")

            for line in hexcodes.readlines():
                i += 1
                #print i, count, i/float(count),i/float(count)*100
                self.emit(SIGNAL('EXPORT'), i/float(count)*100)
                line = str(line.strip())
                decoded.write('{h},'.format(h=str(line)))
                try:
                    c.processHex(str(line))
                    if str(c.location[0]).find('Error') != -1:
                        finallat = courselat = 'error'
                    elif str(c.location[0]).find('Default') != -1:
                        finallat = courselat = 'default'
                    else:
                        finallat = c.location[0]
                        courselat = c.courseloc[0]

                    if str(c.location[1]).find('Error') != -1:
                        finallong = courselong = 'error'
                    elif str(c.location[1]).find('Default') != -1:
                        finallong = courselong = 'default'
                    else:
                        finallong = c.location[1]
                        courselong = c.courseloc[1]

                    if c._btype == 'Test':
                        testcode = '1'
                    else:
                        testcode = '0'
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
                    decoded.write('{},'.format(courselat))
                    decoded.write('{},'.format(courselong))
                    decoded.write('{},'.format(finallat))
                    decoded.write('{},'.format(finallong))
                    decoded.write('{},'.format(c.fixedbits))

                except decodehex2.HexError as e:

                    decoded.write(e.value)
                decoded.write('\n')

        decoded.close()
        self.emit(SIGNAL('EXPORT'), 100)



    def updateProgress(self, val):
        self.dialog.updateProgress(val)









if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()
