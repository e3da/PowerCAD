# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ResponseSurface.ui'
#
# Created: Mon Jun 04 11:22:15 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ResponseSurface(object):
    def setupUi(self, ResponseSurface):
        ResponseSurface.setObjectName("ResponseSurface")
        ResponseSurface.resize(714, 278)
        self.frame = QtGui.QFrame(ResponseSurface)
        self.frame.setGeometry(QtCore.QRect(10, 30, 690, 231))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_add_layer_stack = QtGui.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.btn_add_layer_stack.setFont(font)
        self.btn_add_layer_stack.setObjectName("btn_add_layer_stack")
        self.gridLayout.addWidget(self.btn_add_layer_stack, 0, 0, 2, 2)
        self.label_22 = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 0, 7, 1, 1)
        self.list_mdl_lib = QtGui.QListView(self.frame)
        self.list_mdl_lib.setObjectName("list_mdl_lib")
        self.gridLayout.addWidget(self.list_mdl_lib, 1, 7, 8, 1)
        self.label_4 = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 3)
        self.lineEdit_maxW = QtGui.QLineEdit(self.frame)
        self.lineEdit_maxW.setObjectName("lineEdit_maxW")
        self.gridLayout.addWidget(self.lineEdit_maxW, 2, 4, 1, 1)
        self.label_14 = QtGui.QLabel(self.frame)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 2, 5, 1, 1)
        self.label_7 = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 3)
        self.lineEdit_maxL = QtGui.QLineEdit(self.frame)
        self.lineEdit_maxL.setObjectName("lineEdit_maxL")
        self.gridLayout.addWidget(self.lineEdit_maxL, 3, 4, 1, 1)
        self.label_15 = QtGui.QLabel(self.frame)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 3, 5, 1, 1)
        self.label_16 = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 4, 0, 1, 3)
        self.label_17 = QtGui.QLabel(self.frame)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 5, 0, 1, 1)
        self.lineEdit_fmin = QtGui.QLineEdit(self.frame)
        self.lineEdit_fmin.setObjectName("lineEdit_fmin")
        self.gridLayout.addWidget(self.lineEdit_fmin, 5, 1, 1, 2)
        self.label_18 = QtGui.QLabel(self.frame)
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 5, 3, 1, 1)
        self.lineEdit_fmax = QtGui.QLineEdit(self.frame)
        self.lineEdit_fmax.setObjectName("lineEdit_fmax")
        self.gridLayout.addWidget(self.lineEdit_fmax, 5, 4, 1, 1)
        self.label_24 = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 6, 0, 1, 2)
        self.label_25 = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.gridLayout.addWidget(self.label_25, 7, 0, 1, 2)
        self.lineEdit_name = QtGui.QLineEdit(self.frame)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 7, 2, 1, 3)
        self.btn_build = QtGui.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.btn_build.setFont(font)
        self.btn_build.setObjectName("btn_build")
        self.gridLayout.addWidget(self.btn_build, 8, 0, 1, 2)
        self.label_27 = QtGui.QLabel(self.frame)
        self.label_27.setObjectName("label_27")
        self.gridLayout.addWidget(self.label_27, 7, 5, 1, 1)
        self.cmb_sims = QtGui.QComboBox(self.frame)
        self.cmb_sims.setObjectName("cmb_sims")
        self.cmb_sims.addItem("")
        self.cmb_sims.addItem("")
        self.gridLayout.addWidget(self.cmb_sims, 6, 2, 1, 1)

        self.retranslateUi(ResponseSurface)
        QtCore.QMetaObject.connectSlotsByName(ResponseSurface)

    def retranslateUi(self, ResponseSurface):
        ResponseSurface.setWindowTitle(QtGui.QApplication.translate("ResponseSurface", "ResponseSurface", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_add_layer_stack.setText(QtGui.QApplication.translate("ResponseSurface", "Import Layer Stack", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setText(QtGui.QApplication.translate("ResponseSurface", "Model Library", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ResponseSurface", "Maximum Trace Width:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("ResponseSurface", "mm", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("ResponseSurface", "Maximum Trace Length:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("ResponseSurface", "mm", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("ResponseSurface", "Frequency Sweep (kHz):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("ResponseSurface", "Min", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("ResponseSurface", "Max", None, QtGui.QApplication.UnicodeUTF8))
        self.label_24.setText(QtGui.QApplication.translate("ResponseSurface", "Simulator", None, QtGui.QApplication.UnicodeUTF8))
        self.label_25.setText(QtGui.QApplication.translate("ResponseSurface", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_build.setText(QtGui.QApplication.translate("ResponseSurface", "Build", None, QtGui.QApplication.UnicodeUTF8))
        self.label_27.setText(QtGui.QApplication.translate("ResponseSurface", ".rsmdl", None, QtGui.QApplication.UnicodeUTF8))
        self.cmb_sims.setItemText(0, QtGui.QApplication.translate("ResponseSurface", "Q3D", None, QtGui.QApplication.UnicodeUTF8))
        self.cmb_sims.setItemText(1, QtGui.QApplication.translate("ResponseSurface", "FastHenry", None, QtGui.QApplication.UnicodeUTF8))

