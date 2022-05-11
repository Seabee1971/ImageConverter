import sys
from os import path

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QComboBox


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        # declare image file types
        self.extensions = ["bmp", "gif", "jpg", "jfif", "png"]
        # Load the ui file
        uic.loadUi("imageConverter.ui", self)

        # Define our widgets
        self.buttonOpenFile = self.findChild(QPushButton, "Button_Open_File")
        self.buttonConvert = self.findChild(QPushButton, "Button_Convert")
        self.buttonQuit = self.findChild(QPushButton, "Button_Quit")
        self.comboBox = self.findChild(QComboBox, "comboBox_imageFormat")
        self.label = self.findChild(QLabel, "Label_Open_File")

        # Modify attributes of widgets
        self.buttonConvert.hide()

        # Add Items to ComboBox
        for ext in self.extensions:
            self.comboBox.addItem(ext)

        # set file type valid variable
        self.valid = None
        # Click the Dropdown Box
        self.buttonOpenFile.clicked.connect(self.select_file)
        self.buttonConvert.clicked.connect(self.convert)
        self.buttonQuit.clicked.connect(self.quit)
        # Show The App
        self.show()

    def quit(self):
        exit()

    def convert(self):
        name = self.fname[0].split('.')
        self.label.setText(f'{self.label.text()}\nConvert: {self.fname[0]} to {name[0]}.{self.comboBox.currentText()}')

        for ext in self.extensions:
            if name[1].endswith(ext):
                self.valid = True
                break

        if self.valid:
            from PIL import Image
            try:
                image = Image.open(f'{self.fname[0]}')
            except Exception as e:
                self.label.setText(
                    f'{self.label.text()}\nUnable to load {self.fname[0]}\nPlease select another image file\n{e}')
                self.fname = ""
            else:
                if image.mode in ("RGBA", "P"):
                    print("Alpha")
                    image = image.convert("RGB")
                    self.label.setText(f'{self.label.text()}\nRemoving Alpha Layer')
                try:
                    image.save(f'{name[0]}.{self.comboBox.currentText()}')
                except Exception as e:
                    self.label.setText(f'{self.label.text()}\nConversion Failed\n{e}')
                    self.success = "Failed"
                else:
                    if path.exists(f'{name[0]}.{self.comboBox.currentText()}'):
                        self.success = "Successful!"
                    else:
                        self.success = "Failed!"
                    self.label.setText(f'{self.label.text()}\nConversion {self.success}')
        else:
            self.label.setText(f'{self.label.text()}\n\n{self.fname[0]} is not a valid image file please try again!')
            self.fname = ""

    def select_file(self):
        # Open FileDialog
        self.fname = QFileDialog.getOpenFileName(self, "Select File to Convert", "c:\\Users\splatt\\Pictures",
                                                 "jpeg Files (*.jpg);;"
                                                 "png files (*.png);;"
                                                 "bmp files(*.bmp);;"
                                                 "jfif files (*.jfif);;"
                                                 "gif files (*.gif)")
        # Output Filename to Label
        if self.fname[0]:
            self.label.setText(f'File to Convert = {self.fname[0]}')
            self.buttonConvert.show()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec()
