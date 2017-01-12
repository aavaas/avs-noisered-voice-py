import sys
from PyQt4 import QtCore, QtGui, uic
import recorder

class MyWidget(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)
		uic.loadUi('avsui.ui', self)
		
		#signals connect
		self.startButton.clicked.connect(self.recordButton_clicked)
		self.stopButton.clicked.connect(self.stopButton_clicked)
		self.playButton.clicked.connect(self.playButton_clicked)
		self.noiseButton.clicked.connect(self.noiseButton_clicked)

	def recordButton_clicked(self):
		self.statLabel.setText("Recording...")
		# self.progressBar.setValue(100)		
		recorder.startrecord()

			

	def stopButton_clicked(self):
		self.statLabel.setText("IDLE")
		recorder.stoprecord()
		recorder.savefile()
		recorder.removenoise()
		self.textEdit.append("my name is aavaas") 

	def playButton_clicked(self):
		self.statLabel.setText("Playing") 

	def noiseButton_clicked(self):
		self.statLabel.setText("Updating noise profile") 		
		recorder.buildnoiseprofile()



app = QtGui.QApplication(sys.argv)
myWidget =MyWidget()
myWidget.show()
app.exec_() 