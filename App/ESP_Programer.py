import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QGridLayout, QLineEdit, QTextEdit, QComboBox, QPushButton, QLabel
from PyQt5.QtCore import QProcess, QTextStream, QFile, QTimer
from PyQt5.QtGui import QIcon
from serial.tools.list_ports import comports

from pathlib import Path

import re


cwd = os.getcwd()

style_file = QFile("Resource\Combinear.qss")
style_file.open(QFile.ReadOnly | QFile.Text)


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowIcon(QIcon('Resource\download.png'))

        self.setWindowTitle('ESP Programer')
        self.setGeometry(500, 200, 800, 800)

        layout = QGridLayout()
        self.setLayout(layout)

        self.read_process = QProcess(self)
        self.output = QTextEdit(self)
        self.read_process.readyReadStandardOutput.connect(self.read_output)
        self.read_process.start("cmd.exe")

        # file selection 1
        file_browse = QPushButton('Browse')
        file_browse.clicked.connect(self.open_file_dialog)
        self.filename_edit = QLineEdit()

        self.COM = QComboBox()

        self.coms = []
        self.timer = QTimer()

        self.timer.start(1000)

        self.timer.timeout.connect(self.updateCom)

        # self.COM.addItems(com[0] for com in comports())

        # self.COM.dropEvent(self.COM.addItems(self.coms))
        # self.COM.activated.connect(self.COMChange)

        self.Program = QPushButton('Program')
        self.Program.clicked.connect(self.program)

        layout.addWidget(QLabel('mainapp File: '), 0, 0)
        layout.addWidget(self.filename_edit, 0, 1)
        layout.addWidget(file_browse, 0, 2)

        layout.addWidget(QLabel('COM: '), 1, 0)
        layout.addWidget(self.COM, 1, 1)

        layout.addWidget(self.Program, 2, 1)
        layout.addWidget(self.output, 3, 1)

        self.show()

    def updateCom(self):
        if len([com[0] for com in comports()]) != len(self.coms):
            _ = self.COM.currentText()
            self.coms = [com[0] for com in comports()]
            self.COM.clear()
            self.COM.addItems(self.coms)
            self.COM.setCurrentIndex(self.COM.findData(_))

    def open_file_dialog(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            cwd,
            ""
        )
        if filename:
            path = Path(filename)
            self.filename_edit.setText(str(path))
            self.main_file_name = self.filename_edit.text().split(
                "\\")[-1].split(".")[0]
            self.dir = self.filename_edit.text().split(self.main_file_name)[0]
            self.boot_loader = self.dir + self.main_file_name + ".ino.bootloader.bin"
            self.partitions = self.dir + self.main_file_name + ".ino.partitions.bin"
            self.app0 = self.dir + "boot_app0.bin"
            self.main_file = self.filename_edit.text()

            self.boot_loader = "\"" + self.boot_loader + "\""
            self.partitions = "\"" + self.partitions + "\""
            self.app0 = "\"" + self.app0 + "\""
            self.main_file = "\"" + self.main_file + "\""

    def read_output(self):
        stream = QTextStream(self.read_process).readAll()

        if re.search("Connecting|Writing at", stream):
            self.Program.setStyleSheet("background-color: green;")
        elif re.search("A fatal error occurred:", stream):
            self.Program.setStyleSheet("background-color: red;")
        elif re.search("Hard resetting via RTS pin...", stream):
            self.Program.setStyleSheet(
                "background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(84, 84, 84, 255),stop:1 rgba(59, 59, 59, 255));")
        self.output.append(stream)

    def program(self):
        self.output.clear()
        self.command = ['Resource\esptool.exe', '--chip', 'esp32', '--port', self.COM.currentText(), '--baud', '115200', '--before', 'no_reset', '--after', 'hard_reset', 'write_flash', '-e', '-z',
                        '--flash_mode', 'dio', '--flash_freq', '40m', '--flash_size', '4MB', '0x0', self.boot_loader, '0x8000', self.partitions, '0xe000', self.app0, '0x10000', self.main_file]
        self.read_process.write((' '.join(self.command) + '\n').encode())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.setStyleSheet(style_file.readAll().data().decode())
    style_file.close()
    sys.exit(app.exec())
