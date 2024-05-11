import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginbutton_2.clicked.connect(self.gotocreate)

    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()
        print(email, password)

    def gotocreate(self):
        createacc = Register()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Register(QMainWindow):
    def __init__(self):
        super(Register, self).__init__()
        loadUi("signup.ui", self)
        self.signupbutton.clicked.connect(self.registerfunction)

    def registerfunction(self):
        email = self.email2.text()
        if self.password_2.text() in self.confirmpassword.text():
            password = self.password_2.text()
            print(email, password)
            login = Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            print('что то пошло не так')











app = QApplication(sys.argv)
mainwindow = Login()
mainwindow.show()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.show()
widget.setFixedWidth(480)
widget.setFixedHeight(620)
sys.exit(app.exec_())