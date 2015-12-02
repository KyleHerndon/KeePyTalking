# mazes are 6 by 6 grids
# should be representable using adjacency matrix

# 0 1 2 3
# up right down left

# f c dot
# paragraph star b


# mazes are identifiable using 2 dots
# 9 mazes exist



MAZE_SIZE = 6
# mazeCap = "|=|=|=|=|=|=|=|"
borderChar = "="
vWallChar = "|"
hWallChar = "-"
gapChar = "."
crossChar = "+"

mazeCap = vWallChar + (borderChar + vWallChar) * MAZE_SIZE


class MazeIdentifier():
	def __init__(self):
		self.mazes = {}

	def putMaze(self, dot1, dot2, maze):
		self.mazes[(dot1, dot2)] = maze

	def getMaze(self, dot1, dot2):
		if (dot1, dot2) in self.mazes:
			return self.mazes[(dot1, dot2)]
		elif (dot2, dot1) in self.mazes:
			return self.mazes[(dot2, dot1)]
		else:
			return None

class Maze:
	def __init__(self, parseable="",empty=False):
		self._adjacency = {}

		if len(parseable) > 0:
			self._parse(parseable)

		if empty: # no walls between any cells
			for i in range(MAZE_SIZE):
				for j in range(MAZE_SIZE):
					self.addToAdjacency((i, j), (i+1, j))
					self.addToAdjacency((i, j), (i, j+1))

	def addToAdjacency(self, pos1, pos2):
		if (not Maze.valid(pos1)) or (not Maze.valid(pos2)):
			return

		if pos1 not in self._adjacency:
			self._adjacency[pos1] = []
		if pos2 not in self._adjacency:
			self._adjacency[pos2] = []
		self._adjacency[pos1].append(pos2)
		self._adjacency[pos2].append(pos1)

	def _parse(self, stronk, AIR="."):
		# do stuff
		slines = stronk.strip().split('\n')

		for i in range(len(slines)):
			row = i // 2
			for j in range(len(slines[i])):
				col = j // 2
				if slines[i][j] == AIR:
					if (i % 2) == 0 and (j % 2) == 1:
					#	print("used " + slines[i][j] + " of coords " + str((i, j)) + " at " + str( (row, col)) + "'s right" )
						self.addToAdjacency( (row, col), (row, col+1) )
					elif (i % 2) == 1 and (j % 2) == 0:
					#	print("used " + slines[i][j] + " of coords " + str((i, j)) + " at " + str( (row, col)) + "'s bottom" )
						self.addToAdjacency( (row, col), (row+1, col) )
		return


	@staticmethod
	def valid(pos):
		return pos[0] < MAZE_SIZE and pos[1] < MAZE_SIZE

	#def removeWalls(self, pos, walls):
	#	if valid(pos):

	def hasAdjacent(self, pos1, pos2):
		if pos1 not in self._adjacency:
			return False
		return pos2 in self._adjacency[pos1]

	def showAdjacency(self):
		for i in range(MAZE_SIZE):
			for j in range(MAZE_SIZE):
				if (i, j) in self._adjacency:
					print( str((i, j)) + ": " + str( self._adjacency[(i, j)] ))
				else:
					print( str((i, j)) + ": No adjacent vertices. :(")
def hasGap(maze, pos1, pos2):
	return maze.hasAdjacent(pos1, pos2)

def showMaze(maze):
	print("==========MAAAAAZE")
	print(mazeCap)
	for i in range(0, MAZE_SIZE + MAZE_SIZE - 1):
		rowout = ""
		row = i // 2
		if i % 2 == 0:
			rowout = "="
			for col in range(0, MAZE_SIZE):
				rowout += str(col)
				if col < MAZE_SIZE-1:
					if hasGap(maze, (row, col), (row, col+1)):
						rowout += "."
					else:
						rowout += vWallChar
				else: # right wall
					rowout += borderChar
		else:
			rowout = "|"
			for col in range(0, MAZE_SIZE):
				if hasGap(maze, (row, col), (row+1, col)):
					rowout += "."
				else: 
					rowout += "-"
				if col < MAZE_SIZE-1:
					rowout += "+"
				else: # right wall
					rowout += "|"
		print(rowout)
		

	print(mazeCap)
	print("==================")
	return


if __name__ == '__main__':

	what = '''
*.*.*.*.*.*
.+.+.+.+.+.
*.*.*.*.*.*
.+.+.+.+.+.
*.*.*.*.*.*
.+.+.+.+.+.
*.*.*.*.*.*
.+.+.+.+.+.
*.*.*.*.*.*
.+.+.+.+.+.
*.*.*.*.*.*
'''

	m1 = '''
*.*.*|*.*.*
.+-+.+.+-+-
*|*.*|*.*.*
.+.+-+-+-+.
*|*.*|*.*.*
.+-+.+.+-+.
*|*.*.*|*.*
.+-+-+-+-+.
*.*.*|*.*|*
.+-+.+.+-+.
*.*|*.*|*.*
'''

	m2 = '''

'''

	midf = MazeIdentifier()
	midf.putMaze( (1, 0), (2, 5), Maze(m1) )
	midf.putMaze(  )


	#midf.getMaze( (2, 5), (1, 0) ).showAdjacency()
	#mazepool = [m1, m2]
	#Maze(empty=True).showAdjacency()
	#for m in mazepool:
	#	print("=====================THIS IS A BAR=====================")
	#	wowmaze=Maze(m)
	#	wowmaze.showAdjacency()

