# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graphing_form.ui'
#
# Created: Sun Jun 05 23:52:05 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_GrapheneWindow(object):
    def setupUi(self, GrapheneWindow):
        GrapheneWindow.setObjectName("GrapheneWindow")
        GrapheneWindow.resize(1074, 772)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GrapheneWindow.sizePolicy().hasHeightForWidth())
        GrapheneWindow.setSizePolicy(sizePolicy)
        GrapheneWindow.setMinimumSize(QtCore.QSize(0, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(57, 57, 57))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(57, 57, 57))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(57, 57, 57))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(57, 57, 57))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        GrapheneWindow.setPalette(palette)
        self.centralwidget = QtGui.QWidget(GrapheneWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.scrl_objectivesWindow = QtGui.QScrollArea(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrl_objectivesWindow.sizePolicy().hasHeightForWidth())
        self.scrl_objectivesWindow.setSizePolicy(sizePolicy)
        self.scrl_objectivesWindow.setMinimumSize(QtCore.QSize(0, 0))
        self.scrl_objectivesWindow.setMaximumSize(QtCore.QSize(380, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.scrl_objectivesWindow.setPalette(palette)
        self.scrl_objectivesWindow.setFrameShape(QtGui.QFrame.Panel)
        self.scrl_objectivesWindow.setLineWidth(2)
        self.scrl_objectivesWindow.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrl_objectivesWindow.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrl_objectivesWindow.setWidgetResizable(True)
        self.scrl_objectivesWindow.setObjectName("scrl_objectivesWindow")
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 376, 309))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrl_objectivesWindow.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrl_objectivesWindow, 0, 0, 1, 1)
        self.plot_widget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_widget.sizePolicy().hasHeightForWidth())
        self.plot_widget.setSizePolicy(sizePolicy)
        self.plot_widget.setMinimumSize(QtCore.QSize(594, 584))
        self.plot_widget.setAutoFillBackground(False)
        self.plot_widget.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.plot_widget.setObjectName("plot_widget")
        self.gridLayout.addWidget(self.plot_widget, 0, 1, 3, 1)
        self.gfx_layoutPreview = QtGui.QGraphicsView(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gfx_layoutPreview.sizePolicy().hasHeightForWidth())
        self.gfx_layoutPreview.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(57, 57, 57))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.gfx_layoutPreview.setPalette(palette)
        self.gfx_layoutPreview.setFrameShape(QtGui.QFrame.Panel)
        self.gfx_layoutPreview.setFrameShadow(QtGui.QFrame.Raised)
        self.gfx_layoutPreview.setLineWidth(3)
        self.gfx_layoutPreview.setObjectName("gfx_layoutPreview")
        self.gridLayout.addWidget(self.gfx_layoutPreview, 1, 0, 1, 1)
        self.objective_values_table = QtGui.QTableView(self.centralwidget)
        self.objective_values_table.setMaximumSize(QtCore.QSize(380, 150))
        self.objective_values_table.setObjectName("objective_values_table")
        self.gridLayout.addWidget(self.objective_values_table, 2, 0, 1, 1)
        self.bnt_saveLayout = QtGui.QPushButton(self.centralwidget)
        self.bnt_saveLayout.setObjectName("bnt_saveLayout")
        self.gridLayout.addWidget(self.bnt_saveLayout, 3, 0, 1, 1)
        self.btn_export_csv = QtGui.QPushButton(self.centralwidget)
        self.btn_export_csv.setObjectName("btn_export_csv")
        self.gridLayout.addWidget(self.btn_export_csv, 4, 0, 1, 1)
        self.navbar_widget = QtGui.QWidget(self.centralwidget)
        self.navbar_widget.setMinimumSize(QtCore.QSize(594, 40))
        self.navbar_widget.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.navbar_widget.setObjectName("navbar_widget")
        self.gridLayout.addWidget(self.navbar_widget, 4, 1, 2, 1)
        #self.Electro_Thermal_btn = QtGui.QPushButton(self.centralwidget)
        #self.Electro_Thermal_btn.setObjectName("Electro_Thermal_btn")
        #self.gridLayout.addWidget(self.Electro_Thermal_btn, 5, 0, 1, 1)
        GrapheneWindow.setCentralWidget(self.centralwidget)
        self.action_save_image = QtGui.QAction(GrapheneWindow)
        self.action_save_image.setObjectName("action_save_image")
        self.action_quit = QtGui.QAction(GrapheneWindow)
        self.action_quit.setObjectName("action_quit")

        self.retranslateUi(GrapheneWindow)
        QtCore.QMetaObject.connectSlotsByName(GrapheneWindow)

    def retranslateUi(self, GrapheneWindow):
        GrapheneWindow.setWindowTitle(QtGui.QApplication.translate("GrapheneWindow", "Graphene", None, QtGui.QApplication.UnicodeUTF8))
        self.bnt_saveLayout.setText(QtGui.QApplication.translate("GrapheneWindow", "Save Layout to Main Window", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_export_csv.setText(QtGui.QApplication.translate("GrapheneWindow", "Export Solution Set", None, QtGui.QApplication.UnicodeUTF8))
        #self.Electro_Thermal_btn.setText(QtGui.QApplication.translate("GrapheneWindow", "Electro-Thermal co-simulation of pareto-front", None, QtGui.QApplication.UnicodeUTF8))
        self.action_save_image.setText(QtGui.QApplication.translate("GrapheneWindow", "Save Image", None, QtGui.QApplication.UnicodeUTF8))
        self.action_quit.setText(QtGui.QApplication.translate("GrapheneWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))

