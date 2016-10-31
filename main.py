#!/usr/bin/env python3
import sys
import time
from a_star import a_star_pathfind
from TileGraph import TileGraph
# import MainWindow
from fractions import gcd
from PyQt4 import QtCore, QtGui
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *

class Tile():
	def __init__(self, size, tile):
		tile = "".join(tile)
		clear = tile.count(".")
		if clear == size * size:
			self.open = True
		else:
			self.open = False
		self.explored = False
		self.final = False

def FormatInfo(raw):
	info = raw.pop(0)
	info = info.split(" ")
	info = info[1]
	return info
	


def MakeTiles(filename, size):
	# Open the file & read in the data
	mapFile = open(filename + ".map", "r")
	raw = list(mapFile)
	mapFile.close()

	# Clean up the data & seperate out non-map values
	for i in range(0, len(raw)):
		raw[i] = raw[i].replace("\n", "")
	mapType = FormatInfo(raw)
	height = int(FormatInfo(raw))
	width = int(FormatInfo(raw))
	raw.pop(0)	# line between info & the map itself

	# Pad the map, if necessary
	left = True
	bottom = True
	while gcd(width, height) < size:
		if (width%size > height%size):
			for i in range(0, height):
				if left:
					raw[i] = "@" + raw[i]
				else:
					raw[i] = raw[i] + "@"
			left = not left
			width += 1
		else:
			if bottom:
				raw.append("@" * width)
			else:
				raw = ["@" * width] + raw
			bottom = not bottom
			height += 1

	# Make the tiles
	width = int(width / size)
	height = int(height / size)
	tiles = []
	for y in range(0, height):
		col = raw[y * size:y * size + size]
		row = []
		for x in range(0, width):
			tile = []
			for c in col:
				tile.append(c[x * size: x * size + size])
			row.append(Tile(size, tile))
		tiles.append(row)
	return tiles

class mapView(QtGui.QWidget):
	def __init__(self, parent = None):
		super(mapView, self).__init__(parent)
		self.app = None
		self.setStart = True
		self.setEnd = True
		self.start = (10, 19)
		self.end = (50, 50)
		self.size = 2
		self.sizeDraw = 5
		self.maps = ["arena2", "hrt201n"]
		self.tiles = []
		for m in self.maps:
			new = MakeTiles(m, self.size)
			self.tiles.append(MakeTiles(m, self.size))
		self.iMap = 0
		# layout = QtGui.QHBoxLayout()
		# self.setLayout(layout)
		self.initUI()
	def mousePressEvent(self, event):
		x = event.x() // self.sizeDraw
		y = event.y() // self.sizeDraw
		if y < len(self.tiles[self.iMap]) and x < len(self.tiles[self.iMap][0]):
			if self.setStart:
				self.start = (x, y)
				self.tiles[self.iMap][y][x].explored = True
				self.setStart = False
			elif self.setEnd:
				self.end = (x, y)
				self.tiles[self.iMap][y][x].explored = True
				self.setEnd = False
			self.update()
		# print("({}, {}) -> ({}, {})".format(event.x(), event.y(), x, y))
			
	def getTiles(self):
		return self.tiles[self.iMap]
		
	def markExplored(self, pos):
		self.tiles[self.iMap][pos[1]][pos[0]].explored = True
		self.tiles[self.iMap][pos[1]][pos[0]].final = False
		self.update()
		
	def markFinal(self, pos_list):
		for pos in pos_list:
			self.tiles[self.iMap][pos[1]][pos[0]].explored = False
			self.tiles[self.iMap][pos[1]][pos[0]].final = True
		self.update()
	def reset_state(self):
		for row in self.tiles[self.iMap]:
			for elem in row:
				elem.explored = False
				elem.final = False
		self.setStart = True
		self.setEnd = True
		self.update()

	def a_star_on_tiles(self):
		tiled_graph = TileGraph(self.getTiles())
		i = 0
		for pos in a_star_pathfind(tiled_graph, self.start, self.end):
			if type(pos) is not list:
				self.markExplored(pos)
			else:
				self.markFinal(pos)
			# time.sleep(0.1)
			# self.repaint()
			app.processEvents()
			# app.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents)
			if i % 5 == 0:
				app.processEvents()
				i = 0
			i += 1

	def comboChange(self,i):
		self.reset_state()
		self.iMap = i
		self.update()
        
	def initUI(self):      
		self.setWindowState(QtCore.Qt.WindowMaximized)
		self.setWindowTitle('Tile Size: ' + str(self.size) + ", Map: " + self.maps[self.iMap] + " " + str(len(self.tiles[0][0])) + "x" + str(len(self.tiles[0])))
		self.show()

	def paintEvent(self, e):
		qp = QtGui.QPainter()
		qp.begin(self)
		self.drawRectangles(qp)
		qp.end()
	    
	def drawRectangles(self, qp):  
		color = QtGui.QColor(0, 0, 0)
		color.setNamedColor('#d4d4d4')
		qp.setPen(color)

		for y in range(0, len(self.tiles[self.iMap])):
			for x in range(0, len(self.tiles[self.iMap][0])):
				if self.tiles[self.iMap][y][x].open:
					a = 200
					b = 0
					c = 0
					d = 0
				else:
					a = 25
					b = 80
					c = 90
					d = 200
				if self.tiles[self.iMap][y][x].final:
					d = 200
				elif self.tiles[self.iMap][y][x].explored:
					d = 100
				qp.setBrush(QtGui.QColor(a, b, c, d))
				qp.drawRect(x * self.sizeDraw, y * self.sizeDraw, self.sizeDraw, self.sizeDraw)
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.mapBox = QtGui.QComboBox(self.centralwidget)
        self.mapBox.setGeometry(QtCore.QRect(0, 0, 221, 26))
        self.mapBox.setObjectName(_fromUtf8("mapBox"))
        self.findPathButton = QtGui.QPushButton(self.centralwidget)
        self.findPathButton.setGeometry(QtCore.QRect(220, 0, 110, 32))
        self.findPathButton.setObjectName(_fromUtf8("findPathButton"))
        self.widget = mapView(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 30, 791, 521))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.waypointModeButton = QtGui.QPushButton(self.centralwidget)
        self.waypointModeButton.setGeometry(QtCore.QRect(330, 0, 141, 32))
        self.waypointModeButton.setObjectName(_fromUtf8("waypointModeButton"))
        self.resetButton = QtGui.QPushButton(self.centralwidget)
        self.resetButton.setGeometry(QtCore.QRect(471, 0, 110, 32))
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.findPathButton.setText(_translate("MainWindow", "Find Path", None))
        self.waypointModeButton.setText(_translate("MainWindow", "Waypoint Mode", None))
        self.resetButton.setText(_translate("MainWindow", "Reset", None))

# def a_star_on_tiles(graph, start, end, map_widget):
# 	for pos in a_star_pathfind(graph, start, end):
# 		if type(pos) is not list:
# 			map_widget.markExplored(pos)
# 		else:
# 			map_widget.markFinal(pos)
# 		time.sleep(0.2)
	
	
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	ui.mapBox.addItems(ui.widget.maps)
	ui.mapBox.currentIndexChanged.connect(ui.widget.comboChange)
	
	ui.widget.app = app
	ui.findPathButton.clicked.connect(ui.widget.a_star_on_tiles)
	ui.resetButton.clicked.connect(ui.widget.reset_state)
		
	MainWindow.show()
	
	
	
	sys.exit(app.exec_())