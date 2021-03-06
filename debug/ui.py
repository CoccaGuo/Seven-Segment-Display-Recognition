# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import time, socket

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2

from vision import process


class Pressure(QtCore.QObject):
    update_pressure = QtCore.pyqtSignal(str, str)
    # udp server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    PORT = 5060
    server_address = ("localhost", PORT) 

    def upgrade_pressure(self):
        # setup ccd
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
        for i in range(10): rval, frame = cap.read()
        while rval:
            rval, frame = cap.read()
            p_stm, p_prep = process(frame)
            self.update_pressure.emit(p_stm, p_prep)
            # delete space for Labview and broadcasting by udp
            self.client_socket.sendto(f'{p_stm.replace(" ","")},{p_prep.replace(" ","")}'.encode(), self.server_address)
            time.sleep(0.2)


class Ui_Dialog(QtWidgets.QDialog):

    def update_pressures(self, p_stm, p_prep):
        self.p_stm_num.setText(p_stm)
        self.p_prep_num.setText(p_prep)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 180)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.horizontalFrame = QtWidgets.QFrame(Dialog)
        self.horizontalFrame.setGeometry(QtCore.QRect(0, 0, 400, 180))
        self.horizontalFrame.setObjectName("horizontalFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.horizontalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.horizontalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.p_stm_num = QtWidgets.QLabel(self.horizontalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.p_stm_num.setFont(font)
        self.p_stm_num.setAlignment(QtCore.Qt.AlignCenter)
        self.p_stm_num.setObjectName("p_stm_num")
        self.verticalLayout_3.addWidget(self.p_stm_num)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.horizontalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.p_prep_num = QtWidgets.QLabel(self.horizontalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.p_prep_num.setFont(font)
        self.p_prep_num.setAlignment(QtCore.Qt.AlignCenter)
        self.p_prep_num.setObjectName("p_prep_num")
        self.verticalLayout_2.addWidget(self.p_prep_num)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_5 = QtWidgets.QLabel(self.horizontalFrame)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_2 = QtWidgets.QLabel(self.horizontalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        ## add signal functions
        self.thread = QtCore.QThread()
        self.pressure = Pressure()
        self.pressure.update_pressure.connect(self.update_pressures)
        self.pressure.moveToThread(self.thread)
        self.thread.started.connect(self.pressure.upgrade_pressure)
        self.thread.start()
      

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Pressure Control"))
        self.label.setText(_translate("Dialog", "Pressure Control"))
        self.label_3.setText(_translate("Dialog", "STM"))
        self.p_stm_num.setText(_translate("Dialog", "NaN"))
        self.label_4.setText(_translate("Dialog", "PREP"))
        self.p_prep_num.setText(_translate("Dialog", "NaN"))
        self.label_5.setText(_translate("Dialog", "UDP broadcasting on 5060"))
        self.label_2.setText(_translate("Dialog", "Check settings on ./settings.conf"))
