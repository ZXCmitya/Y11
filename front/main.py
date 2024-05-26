import sys
from typing import Callable

import logic

from front import helper
from front.schemas import User, UserAuth, UserPosts

import mainUi, itemUi, itemUi_UserPost
from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QLineEdit


class Item(QWidget, itemUi.Ui_Form):
    def __init__(self, user: User, on_delete: Callable[[int], bool], parent=None, flags=...):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.user = user
        self.on_delete = on_delete

        self.label_id.setText(str(self.user.id))
        self.label_name.setText(str(self.user.name))
        self.label_username.setText(str(self.user.username))
        self.label_email.setText(str(self.user.email))

        self.btn_remove.clicked.connect(self.handle_btn_delete)

    def handle_btn_delete(self):
        if self.on_delete(self.user.id):
            print(":)")
        else:
            print(":(")


class Item2(QWidget, itemUi_UserPost.Ui_Form):
    def __init__(self, post: UserPosts, parent=None, flags=...):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.post = post

        self.label_post_username.setText(str(self.post.username))
        self.label_post_content.setText(str(self.post.content))
        self.label_post_time.setText(str(self.post.time_of_upload))


class MainApp(QWidget, mainUi.Ui_Form):
    def __init__(self, parent=None, flags=...):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.setGeometry(512, 300, 800, 500)

        self.line_password.setEchoMode(QLineEdit.Password)

        self.line_reg_password.setEchoMode(QLineEdit.Password)

        self.btn_fill.clicked.connect(self.fill_users)

        self.btn_fill_posts.clicked.connect(self.fill_posts)

        self.btn_login.clicked.connect(self.login_handler)

        self.btn_register.clicked.connect(self.register_handler)

        self.btn_to_registration.clicked.connect(self.to_registration)

        self.btn_to_auth.clicked.connect(self.to_auth)

        self.btn_logout.clicked.connect(self.to_auth)

        self.btn_to_info.clicked.connect(self.to_info)

        self.btn_to_post.clicked.connect(self.to_post)

        self.btn_send_post.clicked.connect(self.create_post)

        self.btn_to_settings.clicked.connect(self.to_settings)

        self.btn_to_back.clicked.connect(self.to_main)

        self.btn_save_theme.clicked.connect(self.change_theme)  # button for radios

        self.setStyleSheet(logic.get_current_style_css(logic.get_style_name()))

        try:
            helper.get_current_user()
            self.stackedWidget.setCurrentIndex(2)
            
            user_json = helper.get_current_user_json()
            self.label_name_info.setText(user_json["name"])
            self.label_username_info.setText(user_json["username"])
            self.label_email_info.setText(user_json["email"])
        except:
            self.stackedWidget.setCurrentIndex(0)

    def change_theme(self):
        if self.radio__no_theme.isChecked():
            logic.set_current_style("no-theme")

        elif self.radio__dark_blue.isChecked():
            logic.set_current_style("dark-blue")

        elif self.radio__dark_orange.isChecked():
            logic.set_current_style("dark-orange")

        style_name = logic.get_style_name()

        self.setStyleSheet(logic.get_current_style_css(style_name))

    def to_main(self):
        self.stackedWidget_Settings.setCurrentIndex(0)

    def to_settings(self):
        self.stackedWidget_Settings.setCurrentIndex(1)

    def to_info(self):
        self.stackedWidget_2.setCurrentIndex(0)

    def to_post(self):
        self.stackedWidget_2.setCurrentIndex(1)

    def to_auth(self):
        self.stackedWidget.setCurrentIndex(0)

    def to_registration(self):
        self.stackedWidget.setCurrentIndex(1)
        print(self.stackedWidget.currentIndex())

    def register_handler(self):
        name = self.line_reg_user.text()
        username = self.line_reg_username.text()
        user_email = self.line_reg_email.text()
        password = self.line_reg_password.text()
        mixed = name + username + user_email + password
        mixed_wo_name = username + user_email + password

        if len(name) == 0 or len(username) == 0 or len(user_email) == 0 or len(password) == 0 or ' ' in mixed_wo_name:
            self.label_errors_reg.setText("Введите данные во все поля")
        elif len(name) <= 2 or len(username) <= 2 or len(user_email) <= 2:
            self.label_errors_reg.setText("Длина данных слишком мала. \nПопробуйте еще раз")
        elif '@' not in user_email or '.' not in user_email:
            self.label_errors_reg.setText("Почта введена некорректно")
        elif '\n' in mixed or '\t' in mixed:
            self.label_errors_reg.setText("Даже не думай :)")
        else:
            users = helper.get_all_users()
            is_unique = True

            for user in users:
                if user.username == name or user.email == user_email:
                    is_unique = False

            if not is_unique:
                self.label_errors_reg.setText("Такой пользователь уже существует")
            else:
                user_data = User(name=name, username=username, email=user_email, password=password)
                res = helper.register_user(user_data)

                if res:
                    self.stackedWidget.setCurrentIndex(0)
                else:
                    print("Error")

    def login_handler(self):
        username = self.line_username.text()
        password = self.line_password.text()

        if len(username) == 0 or len(password) == 0:
            self.label_errors_auth.setText("Введите логин и пароль")

        userauth = UserAuth(username=username, password=password)
        res = helper.authorize(userauth)

        if res:
            user_json = helper.get_current_user_json()
            self.stackedWidget.setCurrentIndex(2)
            self.label_name_info.setText(user_json["name"])
            self.label_username_info.setText(user_json["username"])
            self.label_email_info.setText(user_json["email"])
        else:
            print(":( Неверная авторизация")
            self.label_errors_auth.setText("Неверная авторизация")

    def fill_users(self):
        users = helper.get_all_users()  # Получение данных

        self.list_users.clear()

        for user in users:

            userItem = QListWidgetItem(self.list_users)
            self.list_users.addItem(userItem)

            row = Item(user, self.delete_user)
            userItem.setSizeHint(row.minimumSizeHint())

            self.list_users.setItemWidget(userItem, row)

    def fill_posts(self):
        posts = helper.get_all_posts()  # Получение данных

        self.list_posts.clear()

        for post in posts:

            postItem = QListWidgetItem(self.list_posts)
            self.list_posts.addItem(postItem)

            row = Item2(post)
            postItem.setSizeHint(row.minimumSizeHint())

            self.list_posts.setItemWidget(postItem, row)

    def delete_user(self, id: int) -> bool:
        res = helper.remove_user(id)
        if res:
            # self.fill_users()
            for i in range(self.list_users.count()):
                userItem = self.list_users.item(i)
                itemWidget = self.list_users.itemWidget(userItem)

                if itemWidget.user.id == id:
                    self.list_users.takeItem(i)
                    return True
        return False

    def create_post(self):
        content = self.text_post.toPlainText()
        helper.create_post(post=content, user=helper.get_current_user())
        self.text_post.setPlainText("")





if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(logic.get_current_style_css(logic.get_style_name()))
    w = MainApp()
    # pyuic5 -x mainApp.ui -o mainUi.py
    w.show()
    app.exec()
