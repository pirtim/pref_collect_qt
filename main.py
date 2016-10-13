# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from sortowanie import Ui_MainWindow

class MyFirstGuiProgram(Ui_MainWindow):
    def __init__(self, window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)        
        self.path_load = None
        self.data = None
        self.result = None
        self.data_gen = None
        self.first_item = None
        self.second_item = None
        self.line_gen = None
        self.bt_list = [self.pushButton_save, self.pushButton_reload, self.pushButton_save_as,        self.toolButton_left, self.toolButton_draw, self.toolButton_right]
        for bt in self.bt_list:
            bt.setEnabled(False)        
        self.pushButton_load.clicked.connect(self.selectFile)
        self.pushButton_save.clicked.connect(self.saveFile)
        self.pushButton_reload.clicked.connect(self.reloadFile)
        self.toolButton_left.clicked.connect(self.chooseLeft)
        self.toolButton_right.clicked.connect(self.chooseRight)

    def reloadFile(self):
        with open(self.path_load) as f:
            self.data = [line.rstrip() for line in  f.readlines()]
        self.data_gen = enumerate((line for line in self.data))                     
        self.result = []
        self.first_item = next(self.data_gen)[1]     
        self.second_item = next(self.data_gen)[1]          
        self.result.append(self.first_item)
        self.line_gen = insort_left(self.result, self.second_item)
        print('1: ', next(self.line_gen))
        
        self.label_left.setText(self.first_item)
        self.label_right.setText(self.second_item)
        
        self.label_item_edited.setText("0")
        self.label_item_all.setText(str(len(self.data)))
        self.progressBar.setValue(1*100//len(self.data))
        for bt in self.bt_list:
            bt.setEnabled(True)
        self.toolButton_draw.setEnabled(False)
        self.pushButton_save.setEnabled(False)

    def selectFile(self):
        file_info_load = QtWidgets.QFileDialog.getOpenFileName(filter = "Data (*.json);;Text files (*.txt)")
        path_load = file_info_load[0]
        if path_load != '':
            self.path_load = path_load
            self.label_load.setText(path_load)
            self.reloadFile()
    
    def saveFile(self):    
        export = self.result
        with open(self.path_load, 'w') as f:
            f.writelines([line+'\n' for line in  export])
        
    def chooseLeft(self):        
        self.updatePref('left')
    def chooseRight(self):
        self.updatePref('right')
    
    def updatePref(self, side):        
        print('2: ', self.line_gen.send(side == 'right'))
        new = next(self.line_gen)
        print('3: ', new)
        if type(new) == int:
            print('4: ', self.result)
            try: 
                new_data = next(self.data_gen)
            except StopIteration:
                for bt in self.bt_list:
                    bt.setEnabled(False) 
                    
                self.pushButton_save.setEnabled(True)
                self.pushButton_save_as.setEnabled(True)
                self.pushButton_reload.setEnabled(True)
                self.label_item_edited.setText(str(len(self.data)))
                self.progressBar.setValue(100)
                
                QtWidgets.QMessageBox.about(self.centralwidget, "Koniec", "Koniec zbierania preferencji\nWynik to:\n{}".format(self.result))
                print (self.result)
                return

            print('5:', new_data)
            self.second_item = new_data[1]  
            self.label_item_edited.setText(str(new_data[0]))
            self.progressBar.setValue(new_data[0]*100//len(self.data))
            self.line_gen = insort_left(self.result, self.second_item)   
            self.label_right.setText(self.second_item)
            self.first_item = next(self.line_gen)[0]
            self.label_left.setText(self.first_item)
        else:
            self.first_item = new[0]
            self.label_left.setText(self.first_item)

def insort_left(a, x, lo=0, hi=None):
    'Edited insort_left from: https://docs.python.org/3.5/library/bisect.html'
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        yield (a[mid], mid, x)
        por = yield
        if por: lo = mid+1
        else: hi = mid 
    a.insert(lo, x)
    yield lo
 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow() 
    prog = MyFirstGuiProgram(window)
    
    window.show()
    sys.exit(app.exec_())
