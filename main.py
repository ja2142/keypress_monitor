## This Python file uses the following encoding: utf-8
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
        self._keys_pressed = ''
        # TODO stop this thread somehow
        self.read_thread = threading.Thread(target=self.read)
        self.read_thread.start()

    def read(self):
        while True:
            time.sleep(1)
            self._keys_pressed += 'x'
            print(f"text: {self._keys_pressed}")
            self.keysPressedChanged.emit(self._keys_pressed)

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    keypressprovider = KeyPressProvider()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("text_provider", keypressprovider)
    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)

    window = engine.rootObjects()[0]
    text = window.findChild(QObject, 'text')

    k = keypressprovider.keysPressedChanged
    k.connect(window.setText)
    sys.exit(app.exec_())
