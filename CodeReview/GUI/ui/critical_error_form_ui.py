# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'critical_error_form.ui'
#
# Created: Thu Jun  4 13:00:42 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_critical_error_form:
    def setupUi(self, critical_error_form):
        critical_error_form.setObjectName("critical_error_form")
        critical_error_form.setWindowModality(QtCore.Qt.ApplicationModal)
        critical_error_form.resize(997, 683)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(critical_error_form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.error_message_label = QtWidgets.QLabel(critical_error_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.error_message_label.sizePolicy().hasHeightForWidth())
        self.error_message_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.error_message_label.setFont(font)
        self.error_message_label.setLineWidth(1)
        self.error_message_label.setTextFormat(QtCore.Qt.RichText)
        self.error_message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_message_label.setObjectName("error_message_label")
        self.verticalLayout_3.addWidget(self.error_message_label)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.show_backtrace_button = QtWidgets.QPushButton(critical_error_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_backtrace_button.sizePolicy().hasHeightForWidth())
        self.show_backtrace_button.setSizePolicy(sizePolicy)
        self.show_backtrace_button.setObjectName("show_backtrace_button")
        self.horizontalLayout.addWidget(self.show_backtrace_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.back_trace_text_browser = QtWidgets.QTextEdit(critical_error_form)
        self.back_trace_text_browser.setEnabled(True)
        self.back_trace_text_browser.setMinimumSize(QtCore.QSize(800, 500))
        self.back_trace_text_browser.setDocumentTitle("")
        self.back_trace_text_browser.setReadOnly(True)
        self.back_trace_text_browser.setObjectName("back_trace_text_browser")
        self.verticalLayout_2.addWidget(self.back_trace_text_browser)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.exit_button = QtWidgets.QPushButton(critical_error_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit_button.sizePolicy().hasHeightForWidth())
        self.exit_button.setSizePolicy(sizePolicy)
        self.exit_button.setObjectName("exit_button")
        self.verticalLayout.addWidget(self.exit_button)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.ok_button = QtWidgets.QPushButton(critical_error_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ok_button.sizePolicy().hasHeightForWidth())
        self.ok_button.setSizePolicy(sizePolicy)
        self.ok_button.setObjectName("ok_button")
        self.verticalLayout.addWidget(self.ok_button)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.retranslateUi(critical_error_form)
        self.ok_button.clicked.connect(critical_error_form.accept)
        QtCore.QMetaObject.connectSlotsByName(critical_error_form)
        critical_error_form.setTabOrder(self.exit_button, self.ok_button)

    def retranslateUi(self, critical_error_form):
        _translate = QtCore.QCoreApplication.translate
        critical_error_form.setWindowTitle(_translate("critical_error_form", "CodeReview Critical Error"))
        self.error_message_label.setText(_translate("critical_error_form", "Error Message"))
        self.show_backtrace_button.setText(_translate("critical_error_form", "Show Back Trace"))
        self.back_trace_text_browser.setHtml(_translate("critical_error_form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Back Trace</span></p></body></html>"))
        self.exit_button.setText(_translate("critical_error_form", "Exit CodeReview"))
        self.ok_button.setText(_translate("critical_error_form", "OK"))

