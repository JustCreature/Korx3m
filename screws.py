# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'screws.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(297, 173)
        Form.setMinimumSize(QtCore.QSize(297, 173))
        Form.setMaximumSize(QtCore.QSize(297, 173))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.sc_btn_ok = QtWidgets.QPushButton(Form)
        self.sc_btn_ok.setObjectName("sc_btn_ok")
        self.gridLayout.addWidget(self.sc_btn_ok, 2, 0, 1, 1)
        self.sc_btn_cancel = QtWidgets.QPushButton(Form)
        self.sc_btn_cancel.setObjectName("sc_btn_cancel")
        self.gridLayout.addWidget(self.sc_btn_cancel, 2, 1, 1, 1)
        self.frame_RPNV = QtWidgets.QFrame(Form)
        self.frame_RPNV.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_RPNV.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_RPNV.setObjectName("frame_RPNV")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_RPNV)
        self.verticalLayout.setObjectName("verticalLayout")
        self.inp_RPNV_IO = QtWidgets.QDoubleSpinBox(self.frame_RPNV)
        self.inp_RPNV_IO.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.inp_RPNV_IO.setDecimals(0)
        self.inp_RPNV_IO.setMaximum(10000.0)
        self.inp_RPNV_IO.setObjectName("inp_RPNV_IO")
        self.verticalLayout.addWidget(self.inp_RPNV_IO)
        self.inp_RPNV_Dvp = QtWidgets.QDoubleSpinBox(self.frame_RPNV)
        self.inp_RPNV_Dvp.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.inp_RPNV_Dvp.setDecimals(0)
        self.inp_RPNV_Dvp.setMaximum(10000.0)
        self.inp_RPNV_Dvp.setObjectName("inp_RPNV_Dvp")
        self.verticalLayout.addWidget(self.inp_RPNV_Dvp)
        self.inp_RPNV_a = QtWidgets.QDoubleSpinBox(self.frame_RPNV)
        self.inp_RPNV_a.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.inp_RPNV_a.setDecimals(0)
        self.inp_RPNV_a.setMaximum(10000.0)
        self.inp_RPNV_a.setObjectName("inp_RPNV_a")
        self.verticalLayout.addWidget(self.inp_RPNV_a)
        self.gridLayout.addWidget(self.frame_RPNV, 1, 0, 1, 2)
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Нажим. винты"))
        self.sc_btn_ok.setText(_translate("Form", "Ок"))
        self.sc_btn_cancel.setText(_translate("Form", "Отмена"))
        self.inp_RPNV_IO.setSpecialValueText(_translate("Form", "IO"))
        self.inp_RPNV_Dvp.setSpecialValueText(_translate("Form", "Dвп"))
        self.inp_RPNV_a.setSpecialValueText(_translate("Form", "a"))
        self.label.setText(_translate("Form", "Расч. полож. нажимных винтов от \n"
"базовой настройки"))
import source_rc
