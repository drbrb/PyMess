import datetime, time
import threading

import requests
from PyQt5 import QtWidgets
import clientui
"""
Клиент UI для сервера 
"""
# pyuic5 messenger.ui -o clientui.py - преобразование формы в питон форму

class MessengerApp(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.button_clicked)
        self.mutex = threading.Lock()
        threading.Thread(target=self.update_messages).start()


    def send_messege(self, username, password, text):
        response = requests.post('http://127.0.0.1:5000/auth', json={"username": username, "password": password})
        if not response.json()['ok']:
            self.add_to_chat('Сообщение не отправлено')
            return

        response = requests.post('http://127.0.0.1:5000/send', json={"username": username, "password": password, "text": text})

        if not response.json()['ok']:
            self.add_to_chat('Сообщение не отправлено')

    def update_messages(self):
        last_time = 0

        while True:
            try:
                response = requests.get('http://127.0.0.1:5000/messages', params={'after': last_time})

                messages = response.json()["messages"]

                for message in messages:
                    beauty_time = datetime.datetime.fromtimestamp(message["time"])
                    beauty_time = beauty_time.strftime('%d/%m/%Y %H:%M:%S')
                    self.add_to_chat(message["username"]+' '+beauty_time)
                    self.add_to_chat(message["text"])
                    self.add_to_chat("")

                    last_time = message["time"]
            except:
                self.add_to_chat('Произошла ошибка при вводе')
            time.sleep(1)


    def button_clicked(self):
        try:
            self.send_messege(
                self.textEdit_2.toPlainText(),
                self.textEdit_3.toPlainText(),
                self.textEdit.toPlainText()
            )
        except:
            self.add_to_chat('Произошла ошибка')
        self.textEdit.setText('') # чистит поле
        # self.textEdit.repaint() # перерисовывает форму если не отображается



    def add_to_chat(self, text):
        self.mutex.acquire()
        self.textBrowser.append(text)
        self.mutex.release()

app = QtWidgets.QApplication([])
window = MessengerApp()
window.show()
app.exec_()