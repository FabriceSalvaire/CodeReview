# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'email_bug_form.ui'
#
# Created: Tue Jun  2 14:18:03 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_email_bug_form(object):
    def setupUi(self, email_bug_form):
        email_bug_form.setObjectName("email_bug_form")
        email_bug_form.setWindowModality(QtCore.Qt.ApplicationModal)
        email_bug_form.resize(1000, 800)
        self.verticalLayout = QtWidgets.QVBoxLayout(email_bug_form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.from_label = QtWidgets.QLabel(email_bug_form)
        self.from_label.setObjectName("from_label")
        self.verticalLayout.addWidget(self.from_label)
        self.from_line_edit = QtWidgets.QLineEdit(email_bug_form)
        self.from_line_edit.setObjectName("from_line_edit")
        self.verticalLayout.addWidget(self.from_line_edit)
        self.recipients_label = QtWidgets.QLabel(email_bug_form)
        self.recipients_label.setObjectName("recipients_label")
        self.verticalLayout.addWidget(self.recipients_label)
        self.recipients_line_edit = QtWidgets.QLineEdit(email_bug_form)
        self.recipients_line_edit.setWhatsThis("")
        self.recipients_line_edit.setObjectName("recipients_line_edit")
        self.verticalLayout.addWidget(self.recipients_line_edit)
        self.subject_label = QtWidgets.QLabel(email_bug_form)
        self.subject_label.setObjectName("subject_label")
        self.verticalLayout.addWidget(self.subject_label)
        self.subject_line_edit = QtWidgets.QLineEdit(email_bug_form)
        self.subject_line_edit.setObjectName("subject_line_edit")
        self.verticalLayout.addWidget(self.subject_line_edit)
        self.description_label = QtWidgets.QLabel(email_bug_form)
        self.description_label.setObjectName("description_label")
        self.verticalLayout.addWidget(self.description_label)
        self.description_plain_text_edit = QtWidgets.QPlainTextEdit(email_bug_form)
        self.description_plain_text_edit.setObjectName("description_plain_text_edit")
        self.verticalLayout.addWidget(self.description_plain_text_edit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.cancel_button = QtWidgets.QPushButton(email_bug_form)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_2.addWidget(self.cancel_button)
        self.send_email_button = QtWidgets.QPushButton(email_bug_form)
        self.send_email_button.setObjectName("send_email_button")
        self.horizontalLayout_2.addWidget(self.send_email_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.from_label.setBuddy(self.recipients_line_edit)
        self.recipients_label.setBuddy(self.recipients_line_edit)
        self.subject_label.setBuddy(self.subject_line_edit)
        self.description_label.setBuddy(self.description_plain_text_edit)

        self.retranslateUi(email_bug_form)
        self.cancel_button.clicked.connect(email_bug_form.reject)
        QtCore.QMetaObject.connectSlotsByName(email_bug_form)
        email_bug_form.setTabOrder(self.subject_line_edit, self.description_plain_text_edit)
        email_bug_form.setTabOrder(self.description_plain_text_edit, self.send_email_button)

    def retranslateUi(self, email_bug_form):
        _translate = QtCore.QCoreApplication.translate
        email_bug_form.setWindowTitle(_translate("email_bug_form", "Email Bug Form"))
        self.from_label.setText(_translate("email_bug_form", "From:"))
        self.from_line_edit.setToolTip(_translate("email_bug_form", "Type your email, for example \"john.doe@company.com\""))
        self.recipients_label.setText(_translate("email_bug_form", "Additional Recipients:"))
        self.recipients_line_edit.setToolTip(_translate("email_bug_form", "Type something like \"john.doe@company.com,jean.dupont@company.com,...\""))
        self.subject_label.setText(_translate("email_bug_form", "Subject:"))
        self.subject_line_edit.setToolTip(_translate("email_bug_form", "Type a short description"))
        self.description_label.setText(_translate("email_bug_form", "Description:"))
        self.cancel_button.setText(_translate("email_bug_form", "Cancel"))
        self.send_email_button.setText(_translate("email_bug_form", "Send"))

