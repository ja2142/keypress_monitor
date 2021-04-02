#!/usr/bin/env python3

import sys
import os
import time
import threading

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine


class KeyPressProvider(QObject):
    keysPressedChanged = pyqtSignal(str)
    def __init__(self, parent=None):
        super(KeyPressProvider, self).__init__()
        self.keys_pressed = ''
        self.read_thread = threading.Thread(target=self.read)
        # the daemon thread will be terminated once main thread dies
        self.read_thread.daemon = True
        self.read_thread.start()

    def clearFuncKeys(self, to_clear = ['<Enter>', '<LShft>', '<#+8>', '<#+18>']):
        for function_key in to_clear:
            pass

    def read(self):
        with open('keylogger_pipe', 'r') as keylogger_pipe:
            while True:
                new_char = keylogger_pipe.read(1)
                if new_char == '':
                    break
                if new_char == '\n':
                    self.keys_pressed = ''
                else:
                    self.keys_pressed += new_char
                print(f"text: {self.keys_pressed}")
                self.keysPressedChanged.emit(self.keys_pressed)
        print('keylogger_pipe closed, reading thread terminating')

if __name__ == "__main__":
    app = QGuiApplication(sys.argv[:1])
    keypressprovider = KeyPressProvider()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("text_provider", keypressprovider)
    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))
    window = engine.rootObjects()[0]
    if not window:
        sys.exit(-1)

    k = keypressprovider.keysPressedChanged
    k.connect(window.setText)
    sys.exit(app.exec_())
