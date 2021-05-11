#!/usr/bin/env python3

import os
import re
import shlex
import subprocess
import sys
import tempfile
import threading
import time

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

def launch_backend(no_func_keys=False):
    tmp_dir = tempfile.TemporaryDirectory()
    pipe_filename = tmp_dir.name+'/keylogger_pipe'
    os.mkfifo(pipe_filename)
    print(f'fifo created at {pipe_filename}')
    os.chmod(pipe_filename, 0o600)
    logkeys_cmd = f'logkeys -s --no-daemon --keymap keymap --no-timestamps --output={pipe_filename}'
    if no_func_keys:
        logkeys_cmd += ' --no-func-keys'
    return (subprocess.Popen(shlex.split(logkeys_cmd)), tmp_dir)

class KeyPressProvider(QObject):
    keysPressedChanged = pyqtSignal(str)

    def __init__(self, parent=None, ignore_keys=[], no_func_keys=False):
        super(KeyPressProvider, self).__init__()
        self.keylogger_process, self.tmp_dir = launch_backend(no_func_keys)
        self.pipe_filename = self.tmp_dir.name + '/keylogger_pipe'
        self.keys_pressed = ''
        # ignore backsapce, bacause it's emulated in clearFuncKeys
        self.ignore_keys = ignore_keys + ['<BckSp>']

        self.read_thread = threading.Thread(target=self.read)
        # the daemon thread will be terminated once main thread dies
        self.read_thread.daemon = True
        self.read_thread.start()

    def clearFuncKeys(self):
        # remove letters before backspace first, then if any leading <BckSp> remains
        # it will be removed through self.ignore_keys
        self.keys_pressed = re.sub('.<BckSp>', '', self.keys_pressed)
        for function_key in self.ignore_keys:
            self.keys_pressed = self.keys_pressed.replace(function_key, '')

    def read(self):
        with open(self.pipe_filename, 'r') as keylogger_pipe:
            while True:
                new_char = keylogger_pipe.read(1)
                if new_char == '':
                    break
                if new_char == '\n':
                    self.keys_pressed = ''
                else:
                    self.keys_pressed += new_char
                self.clearFuncKeys()
                print(f"text: {self.keys_pressed}")
                self.keysPressedChanged.emit(self.keys_pressed)
        print('keylogger_pipe closed, reading thread terminating')

def main():
    if os.getuid() != 0:
        print('root permissions needed to launch keylogger')
        return
    no_func_keys = '--no-func-keys' in sys.argv
    if no_func_keys:
        ignored_keys = []
    else:
        ignored_keys=['<Enter>', '<LShft>', '<#+8>', '<#+18>']

    app = QGuiApplication(sys.argv[:1])

    keypressprovider = KeyPressProvider(ignore_keys=ignored_keys, no_func_keys=no_func_keys)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("text_provider", keypressprovider)
    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))
    window = engine.rootObjects()[0]
    if not window:
        sys.exit(-1)

    k = keypressprovider.keysPressedChanged

    k.connect(window.setText)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
