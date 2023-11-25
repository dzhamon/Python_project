import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *


# класс данных
class MyProcessData:
	def __init__(self):
		self.num = 0


# класс для обработки
class MyProcessClass(QThread):
	stepChanged = pyqtSignal(int)
	
	def __init__(self):
		super().__init__()
		myProcessData = MyProcessData()
		self.data = myProcessData.num
	
	def run(self):
		for i in range(1000):
			self.data += 5
			self.stepChanged.emit(self.data)
			self.msleep(100)  # установите нужный вам интервал в мс.


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		
		self.centralwidget = QtWidgets.QWidget()
		self.centralwidget.setObjectName("centralwidget")
		self.setCentralWidget(self.centralwidget)
		
		self.title_label = QtWidgets.QLabel()
		self.title_label.setObjectName("title_label")
		self.title_label.setStyleSheet('color: #B20600; font-size: 77px;')
		
		self.pushButton = QtWidgets.QPushButton("Start")
		self.pushButton.clicked.connect(self.btn_clicked)
		
		layout = QGridLayout(self.centralwidget)
		layout.addWidget(self.title_label, 0, 0, 2, 2, alignment=Qt.AlignCenter)
		layout.addWidget(self.pushButton, 2, 1, alignment=Qt.AlignRight)
		
		self.thread = None
	
	def btn_clicked(self):
		if self.thread is None:
			self.thread = MyProcessClass()
			self.thread.stepChanged.connect(self.onStepChanged)
			self.thread.finished.connect(self.onFinished)
			self.thread.start()
			self.pushButton.setText("Stop")
		else:
			self.thread.terminate()
			self.thread = None
			self.pushButton.setText("Start")
	
	def onStepChanged(self, data):
		self.title_label.setNum(data)
	
	def onFinished(self):
		self.thread = None
		self.pushButton.setText("Start")


if __name__=="__main__":
	app = QtWidgets.QApplication(sys.argv)
	app.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
	w = MainWindow()
	w.resize(480, 360)
	w.show()
	sys.exit(app.exec_())