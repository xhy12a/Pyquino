# -*- coding: utf-8 -*-



from PyQt5 import QtWidgets , QtCore
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtWidgets import QMainWindow
import platform
import serialportcontext 
import threading
import time
import serial

from Ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    _receive_signal = QtCore.pyqtSignal(str)
    _auto_send_signal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initForms()

        #self.comboBoxBaud.setCurrentIndex(len(bauds) - 1)        
        
        
    def initForms(self):
        
        if platform.system() == "Windows":
            ports = list()
            for i in range(8):
                ports.append("COM%d" %((i+1)))    
            self.comboBoxPort.addItems(ports)
            print(ports)
        else:
            #todo:scan system serial port
            self.__scanSerialPorts__()
        
        bauds = ["50","75","134","110","150","200","300","600","1200","2400","4800","9600","14400","19200","38400","56000","57600",
                 "115200"];
        self.comboBoxBaud.addItems(bauds)
        self.comboBoxBaud.setCurrentIndex(len(bauds) - 1)
        
        checks = ["None","Odd","Even","Zero","One"]
        self.comboBoxCheckSum.addItems(checks)
        self.comboBoxCheckSum.setCurrentIndex(len(checks) - 1)
        
        bits = ["4 Bits","5 Bits","6 Bits" ,"7 Bits","8 Bits"]
        self.comboBoxBits.addItems(bits)
        self.comboBoxBits.setCurrentIndex(len(bits) - 1)
        
        stopbits = ["1 Bit","1.5 Bits","2 Bits"];
        self.comboBoxStopBits.addItems(stopbits)
        self.comboBoxStopBits.setCurrentIndex(0)
        
        #self._auto_send_signal.connect(self.__auto_send_update__)
        
        port = self.comboBoxPort.currentText()
        #print(port)
        
        baud = int("%s" % self.comboBoxBaud.currentText(),10)
        self._serial_context_ = serialportcontext.SerialPortContext(port = port,baud = baud)
        
#        self.lineEditReceivedCounts.setText("0")
#        self.lineEditSentCounts.setText("0")
        
        self.pushButtonOpenSerial.clicked.connect(self.__open_serial_port__)
       # self.pushButtonClearRecvArea.clicked.connect(self.__clear_recv_area__)
        self.pushButtonSendData.clicked.connect(self.__send_data__)
        self._receive_signal.connect(self.__display_recv_data__)
        

        
       # self.pushButtonOpenRecvFile.clicked.connect(self.__save_recv_file__)
     #   self.pushButtonOpenSendFile.clicked.connect(self.__open_send_file__)
     

   # def __auto_send_update__(self):
    #    self.lineEditSentCounts.setText("%d" % self._serial_context_.getSendCounts())
     
    def __handle_send_looping__(self):
        if self._is_auto_sending:
            self._is_auto_sending = False
            self.pushButtonSendData.setEnabled(True)
     
     
    def __clear_all_counts(self):
       # self.lineEditReceivedCounts.setText("0")
       # self.lineEditSentCounts.setText("0")
        self._serial_context_.clearAllCounts()
        
    def __clear_send_counts(self):
        self._serial_context_.clearSentCounts()
        #self.lineEditSentCounts.setText("0")
    
    def __clear_recv_counts(self):
        self._serial_context_.clearRecvCounts()
       # self.lineEditReceivedCounts.setText("0")

    def __set_display_hex__(self):
        self.textEditReceived.clear()    
    
    def __display_recv_data__(self,data):
        #for l in range(len(data)):
         #   hexstr = "%02X " % ord(str(data[l]))
          #  self.textEditReceived.insertPlainText(hexstr)
          
        #print("gogog", data)
        for l in range(len(data)):
            self.textEditReceived.insertPlainText(data[l])
                
        #if self.checkBoxNewLine.isChecked():
        #    self.textEditReceived.insertPlainText("\n")
                    
       # self.lineEditReceivedCounts.setText("%d" % self._serial_context_.getRecvCounts())

                
    def __scanSerialPorts__(self):
        ports = []
        for i in range(32):
            ports.append("/dev/ttyS%d" % i)
        for i in range(32):
            ports.append("/dev/ttyUSB%d" % i)
        self.comboBoxPort.addItems(ports)
        
    def __open_serial_port__(self):
        if  self._serial_context_.isRunning():
            self._serial_context_.close()
            #self.pushButtonOpenSerial.setText(u'打开')
            print("open")
        else:
            try:
                #currentIndex() will get the number
                portss = self.comboBoxPort.currentText()
                port = self.comboBoxPort.currentText()
                print("the", portss)
                baud = int("%s" % self.comboBoxBaud.currentText(),10)
                self._serial_context_ = serialportcontext.SerialPortContext(port = port,baud = baud)
                #print(self._serial_context_ )
                self._serial_context_ .recall()
                self._serial_context_.registerReceivedCallback(self.__data_received__)
                print("4")
                self._serial_context_.open()
                print("5")
                #self.pushButtonOpenSerial.setText(u'关闭')
                
            except Exception as e:
                print("error")
                #QtGui.QMessageBox.critical(self,u"打开端口",u"打开端口失败,请检查!")
                
    def __clear_recv_area__(self):
        self.textEditReceived.clear()
        
    def __clear_send_area__(self):
        self.textEditSent.clear()
    
    def closeEvent(self,event):
        self._is_auto_sending = False
        if self._serial_context_.isRunning():
            self._serial_context_.close()
       # if self._recv_file_ != None:
            print("123")
           # self._recv_file_.flush()
           # self._recv_file_.close()
    
        
    def __data_received__(self,data):
        print('recv:%s' % data)
        self._receive_signal.emit(data)
        #if self._recv_file_ != None and self.checkBoxSaveAsFile.isChecked():
        #    self._recv_file_.write(data)    
    
    def __send_data__(self):
        data = str(self.textEditSent.toPlainText()+'\n')
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0)
                print(data)
                #self.lineEditSentCounts.setText("%d" % self._serial_context_.getSendCounts())
                #if self.checkBoxEmptyAfterSent.isChecked():
                    #self.textEditSent.clear()
            
                #if self.checkBoxSendLooping.isChecked():
                  #  self.pushButtonSendData.setEnabled(False)
                    #delay = self.spinBox.value() * 100.0 / 1000.0
                    #delay = 100.0 / 1000.0
                   # self._auto_send_thread = threading.Thread(target=self.__auto_send__,args=(delay,))
                    
                   # self._is_auto_sending = True
                   # self._auto_send_thread.setDaemon(True)
                    #self._auto_send_thread.start()
                    
                    
                    
    def __auto_send__(self,delay):
        while self._is_auto_sending:
            #if self.checkBoxSendFile.isChecked():
                #if len(self._send_file_data) > 0:
                    #self._serial_context_.send(self._send_file_data, self.checkBoxSendHex.isChecked())
                    #self._auto_send_signal.emit()
                    #break
            #else:
            data = str(self.textEditSent.toPlainText())
            print("123gogo", data)
            if self._serial_context_.isRunning():
                if len(data) > 0:
                    self._serial_context_.send(data, 1)
                    #self._auto_send_signal.emit()
                        
            time.sleep(delay)
    
    
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    run = MainWindow()
    run.show()
    sys.exit(app.exec_())