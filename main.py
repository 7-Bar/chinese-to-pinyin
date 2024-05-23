'''
chinese to pinyin converter (v2)
By Bar Hibel (Ye Xi)
2024/5/22
'''
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from sys import argv, exit
from pypinyin import pinyin # chinese to pinyin
import hanzidentifier # chinese identifier
from pyperclip import copy # simple clipboard access




class MyWindow(QMainWindow):
    def __init__(self) -> None:
        super(MyWindow, self).__init__()
        #self.initAPP()
        self.initUI()
        self.chinese = "" # variable to store chinese NOTE: NOT IN A LIST
        self.pinyin = "" # variable to store pinyin
        self.DEFAULT_ERROR_MESSAGE = "Something went wrong. Please try again later."
        #self.status_message_state = 0 # variable to store the state of status_message


    def copy_to_clipboard(self, input):
        '''function to copy something to the clipboard'''
        copy(input)


    def evaluate_chinese_to_pinyin(self, input: list) -> str:
        '''function to find out proper pinyin without lists (the "pinyin" function returns a nested list)'''
        output = ""
        pinyin_conversion_result = pinyin(input) # gets the nested list of pinyin from input
        for item in pinyin_conversion_result:
            output = output + " " + (item[0]) # goes into each element and adds it to "output" in front of a space
        return output[1:]
    

    def set_status_message(self, message: str, color: int):
        '''function for setting status_message status'''
        '''color codes: 0=black, 1=green, 2=red'''
        if color == 0:
            color = "black"
        elif color == 1:
            color = "green"
        elif color == 2:
            color = "red"
        
        self.status_message.setText(message)
        self.status_message.setStyleSheet(f"color: {color};")
        self.status_message.adjustSize()
    
    
    def _on_convert_button_pressed(self):
        '''button for converting chinese pressed'''
        if hanzidentifier.identify(self.chinese_input.text()) > 0: # 1 = traditional chinese,2 = not sure what type of chinese, 3 = simplified chinese
            # if input is chinese
            try:
                self.pinyin = self.evaluate_chinese_to_pinyin(self.chinese_input.text())
                self.chinese = self.chinese_input.text()
                self.set_status_message("chinese converted successfully", 1)
            except:
                # if there is an error
                self.set_status_message(self.DEFAULT_ERROR_MESSAGE, 2)

            self.pinyin_output.setText(self.pinyin) # updates self.pinyin

        else:
            # not chinese
            self.set_status_message("Input is not chinese", 2)

    
    def _on_copy_chinese_button_pressed(self):
        '''button for copying chinese pressed'''
        if self.chinese: # if something in self.chinese
            try:
                self.copy_to_clipboard(self.chinese)
                self.set_status_message("chinese copied successfully", 1)
            except:
                self.set_status_message(self.DEFAULT_ERROR_MESSAGE, 2)
        else:
            self.set_status_message("Please input chinese", 2)
            


    def _on_copy_pinyin_button_pressed(self):
        '''button for copying pinyin pressed'''
        if self.pinyin: # if something in self.chinese
            try:
                self.copy_to_clipboard(self.pinyin)
                self.set_status_message("pinyin copied successfully", 1)
            except:
                self.set_status_message(self.DEFAULT_ERROR_MESSAGE, 2)
        else:
            self.set_status_message("Please input pinyin", 2)
    

    def initUI(self):
        '''ui initialization'''
        # basic window setup
        self.setGeometry(700, 300, 300, 180) # x (location of startup), y (location of startup), x size (width), y size (height)
        self.setFixedSize(300, 180) # x and y unresizeable
        self.setWindowTitle("Chinese to Pinyin")

        # labels setup
        self.status_message = QtWidgets.QLabel(self) # label for status messages
        self.status_message.setText("waiting for input...")
        #self.status_message.setStyleSheet("color: red;") # making label red
        self.status_message.move(5, 160)
        self.status_message.adjustSize()

        # textedit setup
        self.pinyin_output = QtWidgets.QTextEdit(self) # textedit for displaying pinyin
        #self.pinyin_output.setPlainText("This is a scrollable text area.\n" * 50)
        self.pinyin_output.setPlaceholderText("(Pinyin goes here)Waiting for chinese...")
        self.pinyin_output.setReadOnly(True)
        self.pinyin_output.setFixedSize(290, 100)
        self.pinyin_output.move(5, 30)
        self.pinyin_output.adjustSize()

        # textbox setup
        self.chinese_input = QtWidgets.QLineEdit(self) # textbox for chinese input
        self.chinese_input.setPlaceholderText("Input chinese here...")
        self.chinese_input.resize(215, 20) # 280
        self.chinese_input.move(5, 5)

        # buttons setup
        self.convert_button = QtWidgets.QPushButton(self) # "convert" button
        self.convert_button.setText("Convert")
        self.convert_button.resize(80, 30)
        self.convert_button.move(220, 0)
        self.convert_button.clicked.connect(self._on_convert_button_pressed)

        self.copy_chinese_button = QtWidgets.QPushButton(self) # button for copying chinese
        self.copy_chinese_button.setText("Copy Chinese")
        self.copy_chinese_button.resize(155, 30)
        self.copy_chinese_button.move(0, 130)
        self.copy_chinese_button.clicked.connect(self._on_copy_chinese_button_pressed)

        self.copy_pinyin_button = QtWidgets.QPushButton(self) # button for copying pinyin
        self.copy_pinyin_button.setText("Copy Pinyin")
        self.copy_pinyin_button.resize(155, 30)
        self.copy_pinyin_button.move(145, 130)
        self.copy_pinyin_button.clicked.connect(self._on_copy_pinyin_button_pressed)




# final setup & running
def window():
    app = QApplication(argv) # sys.argv
    win = MyWindow()
    win.show()
    exit(app.exec_()) # sys.exit

window()
