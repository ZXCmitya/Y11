# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'listItem_UserPost_deletable.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(552, 211)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_post_username = QtWidgets.QLabel(Form)
        self.label_post_username.setObjectName("label_post_username")
        self.verticalLayout_2.addWidget(self.label_post_username)
        self.label_post_content = QtWidgets.QLabel(Form)
        self.label_post_content.setObjectName("label_post_content")
        self.verticalLayout_2.addWidget(self.label_post_content)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_2.addItem(spacerItem)
        self.label_post_time = QtWidgets.QLabel(Form)
        self.label_post_time.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_post_time.setObjectName("label_post_time")
        self.verticalLayout_2.addWidget(self.label_post_time, 0, QtCore.Qt.AlignRight)
        self.btn_delete_post = QtWidgets.QPushButton(Form)
        self.btn_delete_post.setMaximumSize(QtCore.QSize(60, 18))
        self.btn_delete_post.setObjectName("btn_delete_post")
        self.verticalLayout_2.addWidget(self.btn_delete_post, 0, QtCore.Qt.AlignRight)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_post_username.setText(_translate("Form", "Username"))
        self.label_post_content.setText(_translate("Form", "Lorem ipsum"))
        self.label_post_time.setText(_translate("Form", "24:00"))
        self.btn_delete_post.setText(_translate("Form", "Удалить"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
