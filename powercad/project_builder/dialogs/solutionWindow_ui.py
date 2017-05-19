# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'solutionWindow.ui'
#
# Created: Thu Mar 30 20:56:47 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_layout_form(object):
    def setupUi(self, layout_form):
        layout_form.setObjectName("layout_form")
        layout_form.resize(1056, 904)
        layout_form.setMinimumSize(QtCore.QSize(200, 200))
        self.gridLayout = QtGui.QGridLayout(layout_form)
        self.gridLayout.setObjectName("gridLayout")
        self.grfx_layout = QtGui.QGraphicsView(layout_form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grfx_layout.sizePolicy().hasHeightForWidth())
        self.grfx_layout.setSizePolicy(sizePolicy)
        self.grfx_layout.setMinimumSize(QtCore.QSize(100, 100))
        self.grfx_layout.setObjectName("grfx_layout")
        self.gridLayout.addWidget(self.grfx_layout, 0, 4, 10, 1)
        self.tbl_info = QtGui.QTableWidget(layout_form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbl_info.sizePolicy().hasHeightForWidth())
        self.tbl_info.setSizePolicy(sizePolicy)
        self.tbl_info.setMaximumSize(QtCore.QSize(300, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(225, 225, 225))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(225, 225, 225))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(225, 225, 225))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        self.tbl_info.setPalette(palette)
        self.tbl_info.setFrameShape(QtGui.QFrame.NoFrame)
        self.tbl_info.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tbl_info.setAlternatingRowColors(True)
        self.tbl_info.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tbl_info.setShowGrid(False)
        self.tbl_info.setWordWrap(True)
        self.tbl_info.setRowCount(0)
        self.tbl_info.setColumnCount(3)
        self.tbl_info.setObjectName("tbl_info")
        self.tbl_info.setColumnCount(3)
        self.tbl_info.setRowCount(0)
        self.tbl_info.horizontalHeader().setVisible(False)
        self.tbl_info.horizontalHeader().setSortIndicatorShown(False)
        self.tbl_info.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tbl_info, 0, 1, 1, 1)
        self.btn_export_spice_reduced_parasitics = QtGui.QPushButton(layout_form)
        self.btn_export_spice_reduced_parasitics.setObjectName("btn_export_spice_reduced_parasitics")
        self.gridLayout.addWidget(self.btn_export_spice_reduced_parasitics, 8, 1, 1, 1)
        self.line = QtGui.QFrame(layout_form)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 2, 10, 1)
        self.btn_export_spice_parasitics = QtGui.QPushButton(layout_form)
        self.btn_export_spice_parasitics.setObjectName("btn_export_spice_parasitics")
        self.gridLayout.addWidget(self.btn_export_spice_parasitics, 6, 1, 1, 1)
        self.btn_export_spice_thermal = QtGui.QPushButton(layout_form)
        self.btn_export_spice_thermal.setObjectName("btn_export_spice_thermal")
        self.gridLayout.addWidget(self.btn_export_spice_thermal, 7, 1, 1, 1)
        self.btn_export_solidworks = QtGui.QPushButton(layout_form)
        self.btn_export_solidworks.setMaximumSize(QtCore.QSize(300, 16777215))
        self.btn_export_solidworks.setObjectName("btn_export_solidworks")
        self.gridLayout.addWidget(self.btn_export_solidworks, 5, 1, 1, 1)
        self.btn_export_q3d = QtGui.QPushButton(layout_form)
        self.btn_export_q3d.setMaximumSize(QtCore.QSize(300, 16777215))
        self.btn_export_q3d.setObjectName("btn_export_q3d")
        self.gridLayout.addWidget(self.btn_export_q3d, 4, 1, 1, 1)
        self.btn_run_drc = QtGui.QPushButton(layout_form)
        self.btn_run_drc.setObjectName("btn_run_drc")
        self.gridLayout.addWidget(self.btn_run_drc, 3, 1, 1, 1)

        self.retranslateUi(layout_form)
        QtCore.QMetaObject.connectSlotsByName(layout_form)

    def retranslateUi(self, layout_form):
        layout_form.setWindowTitle(QtGui.QApplication.translate("layout_form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_export_spice_reduced_parasitics.setText(QtGui.QApplication.translate("layout_form", "Export SPICE Electrical Reduced Parasitics Netlist", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_export_spice_parasitics.setText(QtGui.QApplication.translate("layout_form", "Export SPICE Electrical Parasitics Netlist", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_export_spice_thermal.setText(QtGui.QApplication.translate("layout_form", "Export SPICE Thermal Netlist", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_export_solidworks.setText(QtGui.QApplication.translate("layout_form", "Export Solution to SolidWorks", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_export_q3d.setText(QtGui.QApplication.translate("layout_form", "Export Solution to Q3D", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_run_drc.setText(QtGui.QApplication.translate("layout_form", "Run DRC", None, QtGui.QApplication.UnicodeUTF8))
