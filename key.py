import sys
import pyautogui
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow,QWidget,QPushButton,QLineEdit,QApplication,QVBoxLayout,QInputDialog,QLabel,QComboBox,QRadioButton,QHBoxLayout,QGroupBox,QCheckBox, QStyleFactory
from PyQt5.QtGui import QPixmap, QFont
from PyQt5 import uic
from win32api import GetKeyState, GetSystemMetrics
import time
import os.path
import pynput
from pynput.keyboard import Key, KeyCode, Listener
import subprocess as sp
import base64

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

my_font = QFont("Arial", 12)

def volup():
    pyautogui.press("volumeup")
def volmute():
    pyautogui.press("volumemute")
def voldown():
    pyautogui.press("volumedown")
def printscr():
    pyautogui.press("prtsc")
def sleep():
    print("Sleep") 
def prevtrack():
    pyautogui.press("prevtrack")    
def nexttrack():
    pyautogui.press("nexttrack")   
def op_progg():
    print("Open program")   
def pl_pa():
    pyautogui.press("playpause")
def nothing():
    pass
    
functions = [nothing, pl_pa, op_progg, nexttrack, prevtrack, volup, voldown, volmute, printscr, sleep]

if os.path.isfile('settings.txt') == True:          
    imp = open('settings.txt', 'r')
    c_i = imp.read()
    combination_to_function = {
        frozenset([Key.f20, KeyCode(vk=0x83)]): functions[int(c_i[0])],
        frozenset([Key.f19, KeyCode(vk=0x82)]): functions[int(c_i[1])],
        frozenset([Key.f18, KeyCode(vk=0x81)]): functions[int(c_i[2])]
    }
elif os.path.isfile('settings.txt') == False:
    combination_to_function = {
        frozenset([Key.f20, KeyCode(vk=0x83)]): functions[0],
        frozenset([Key.f19, KeyCode(vk=0x82)]): functions[0],
        frozenset([Key.f18, KeyCode(vk=0x81)]): functions[0]  
    }

pressed_vks = set()

def get_vk(key):
    return key.vk if hasattr(key, 'vk') else key.value.vk

def is_combination_pressed(cobination):
    return all([get_vk(Key) in pressed_vks for Key in cobination])

def on_press(key):
    vk = get_vk(key)
    pressed_vks.add(vk)
    for combination in combination_to_function: 
        if is_combination_pressed(combination):
            combination_to_function[combination]()
            pressed_vks.remove(vk)
            
def cb5(index):
    combination_to_function[frozenset([Key.f20, KeyCode(vk=0x83)])] = functions[index]
def cb6(index):
    combination_to_function[frozenset([Key.f19, KeyCode(vk=0x82)])] = functions[index]
def cb7(index):
    combination_to_function[frozenset([Key.f18, KeyCode(vk=0x81)])] = functions[index]

class Window(QtWidgets.QWidget):    
    def __init__(self):

        super().__init__()
        # self.setMinimumSize(QSize(300, 200))    
        #layout = QtWidgets.QVBoxLayout(self)
        # super(UI, self).__init__()  
        # uic.loadUi("surface2.ui", self)

        b64_data = "iVBORw0KGgoAAAANSUhEUgAAAZAAAAKgCAYAAAC1LSv8AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAErrSURBVHja7N15tF3pWd/53/u+ezxXs1RSlUolqSRVqTTV4HbZBgxOQtKLJE6CQ9pACAlTpztA0s0Qgw0uj2BnMS5CQugASaCBEKA7IQmEkCzSdDOayQ4eSyqVhqvparjj2cP77r37j73P0VWVjcsuqXQlfT9r3VUuSZZu7XPu/ekdnucxXdcJAIDPlOURAAAIEAAAAQIAIEAAAAQIAAAECACAAAEAECAAAAIEAECAAABAgAAACBAAAAECACBAAAAECAAABAgAgAABABAgAAACBABAgAAAQIAAAAgQAAABAgAgQAAABAgAAAQIAIAAAQAQIAAAAgQAQIAAAECAAAAIEAAAAQIAIEAAAAQIAAAECACAAAEAECAAAAIEAAACBABAgAAACBAAAAECACBAAAAgQAAABAgAgAABABAgAAACBAAAAgQAQIAAAAgQAAABAgAgQAAAIEAAAAQIAIAAAQAQIAAAAgQAAAIEAECAAAAIEAAAAQIAIEAAACBAAAAECACAAAEAECAAAAIEAAACBABAgAAACBAAAAECACBAAAAgQAAABAgAgAABABAgAAAQIAAAAgQAQIAAAAgQAAABAgAAAQIAIEAAAAQIAIAAAQAQIAAAECAAAAIEAECAAAAIEAAAAQIAAAECACBAAAAECACAAAEAECAAABAgAAACBABAgAAACBAAAAECAAABAgAgQAAABAgAgAABABAgAAAQIAAAAgQAQIAAAAgQAAAIEAAAAQIAIEAAAAQIAIAAAQCAAAEAECAAAAIEAECAAAAIEAAACBAAAAECACBAAAAECACAAAEAgAABABAgAAACBABAgAAACBAAAAgQAAABAgAgQAAABAgAgAABAIAAAQAQIAAAAgQAQIAAAAgQAAAIEAAAAQIAIEAAAAQIAIAAAQCAAAEAECAAAAIEAECAAABAgAAACBAAAAECACBAAAAECAAABAgAgAABABAgAAACBABAgAAAQIAAAAgQAAABAgAgQAAABAgAAAQIAIAAAQAQIAAAAgQAQIAAAECAAAAIEAAAAQIAIEAAAAQIAAAECACAAAEA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"
        self.label_pic = QtWidgets.QLabel(self)
        self.label_pic.setGeometry(QtCore.QRect(int(2*180*width/1600), int(2*(-56)*height/900), int(2*400*width/1600), int(2*300*height/900)))
        pixma = QPixmap()
        pixma.loadFromData(base64.b64decode(b64_data))
        pixma1 = pixma.scaled(int(500*width/1600), int(840*height/900), QtCore.Qt.KeepAspectRatio)
        self.label_pic.setPixmap(pixma1)
        self.label_pic.setObjectName("label")

        
        
        self.items=["Nothing", "Play/Pause", "Open program", "Next track", "Previous track", "Volume up", "Volume down", "Mute", "Screenshot", "Sleep"]
        self.combo_boxes=list(map(self.cb_gener, range(3)))
        self.comboBox5,self.comboBox6,self.comboBox7 = self.combo_boxes
        self.lables=list(map(self.label_gener, range(3)))
        self.label5,self.label6,self.label7=self.lables
        for j in range(3):
            self.lables[2].setText("Long click")
            self.lables[1].setText("Double click")
            self.lables[0].setText("Single click") 

        
        self.pushButton1 = QtWidgets.QPushButton(self)
        self.pushButton1.setGeometry(QtCore.QRect(int(2*65*width/1600), int(2*130*height/900), int(2*85*width/1600), int(2*20*height/900)))
        self.pushButton1.setText("Save")   
        self.pushButton1.clicked.connect(self.save)
        self.pushButton1.setFont(my_font)

        self.pushButton2 = QtWidgets.QPushButton(self)
        self.pushButton2.setGeometry(QtCore.QRect(int(2*160*width/1600), int(2*130*height/900), int(2*85*width/1600), int(2*20*height/900)))
        self.pushButton2.setText("Close")
        self.pushButton2.clicked.connect(lambda:exit(self))
        self.pushButton2.setFont(my_font)

        if os.path.isfile('settings.txt') == True:          
            imp = open('settings.txt', 'r')
            c_i = imp.read()            
            self.comboBox5.setCurrentIndex(int(c_i[0]))
            self.comboBox6.setCurrentIndex(int(c_i[1]))
            self.comboBox7.setCurrentIndex(int(c_i[2]))

        self.comboBox5.currentIndexChanged.connect(cb5)
        self.comboBox6.currentIndexChanged.connect(cb6)
        self.comboBox7.currentIndexChanged.connect(cb7)
        

    def cb_gener(self, x, name='comboBox'):
        combo_box = QtWidgets.QComboBox(self)
        combo_box.setGeometry(QtCore.QRect(int(2*65*width/1600), int((40*(x+2)-65)*2*height/900), int(180*2*width/1600), int(20*2*height/900)))
        combo_box.setObjectName(name)
        combo_box.setFont(my_font)
        
        for i in self.items:
            combo_box.addItem(i)
        return combo_box
    
    def label_gener(self, x):
        label = QtWidgets.QLabel(self)
        label.setGeometry(QtCore.QRect(int(2*6*width/1600), int((40*(x+2)-65)*height*2/900), int(2*60*width/1600), int(2*20*height/900)))
        label.setFont(my_font)
        return label
    def exit(self):
        quit()     
    def save(self, event):
        a = []    
        a.extend((self.comboBox5.currentIndex(), self.comboBox6.currentIndex(), self.comboBox7.currentIndex()))
        f = open('settings.txt', 'w')
        for i in range(len(a)):
            f.write(str(a[i]))
        print('Saved')
    
with Listener(on_press=on_press) as listener:
    
    if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        #app.setStyle('Fusion')
        window = Window()
        a = int(2*370*width/1600)
        b = int(2*165*height/900)
        window.resize(a,b)
        #window.setStyleSheet("background-color: white;")
        window.setMinimumSize(a,b)
        window.setMaximumSize(a,b)
        window.setWindowTitle("Surface App")


        window.show()

    sys.exit(app.exec())

    listener.join()
    


