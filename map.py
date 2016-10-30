import sys
from fractions import gcd
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Tile():
	def __init__(self, size, tile):
		tile = "".join(tile)
		clear = tile.count(".")
		if clear == size * size:
			self.open = True
		else:
			self.open = False
		self.explored = False
		self.active = False
	def activate(self):
		self.active = True
		self.explored = True
	def deactivate(self):
		self.active = False

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

class window(QWidget):
	def __init__(self):
		super(window, self).__init__()
		self.size = 2
		self.sizeDraw = 5
		self.maps = ["arena2", "hrt201n"]
		self.tiles = []
		for m in self.maps:
			new = MakeTiles(m, self.size)
			self.tiles.append(MakeTiles(m, self.size))
		self.iMap = 0
		layout = QHBoxLayout()
		self.cb = QComboBox()
		self.cb.addItems(self.maps)
		self.cb.currentIndexChanged.connect(self.comboChange)
		#layout.addWidget(self.cb)
		self.setLayout(layout)
		self.initUI()

	def comboChange(self,i):
		self.iMap = i
        
	def initUI(self):      
		self.setWindowState(Qt.WindowMaximized)
		self.setWindowTitle('Tile Size: ' + str(self.size) + ", Map: " + self.maps[self.iMap] + " " + str(len(self.tiles[0][0])) + "x" + str(len(self.tiles[0])))
		self.show()

	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		self.drawRectangles(qp)
		qp.end()
	    
	def drawRectangles(self, qp):  
		color = QColor(0, 0, 0)
		color.setNamedColor('#d4d4d4')
		qp.setPen(color)

		for y in range(0, len(self.tiles[self.iMap])):
			for x in range(0, len(self.tiles[self.iMap][0])):
				if self.tiles[self.iMap][y][x].open:
					qp.setBrush(QColor(200, 0, 0, 0))
				else:
					qp.setBrush(QColor(25, 80, 90, 200))
				qp.drawRect(x * self.sizeDraw, y * self.sizeDraw, self.sizeDraw, self.sizeDraw)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = window()
	sys.exit(app.exec_())