 # mazes are 6 by 6 grids
# should be representable using adjacency matrix

# 0 1 2 3
# up right down left

# f c dot
# paragraph star b


# mazes are identifiable using 2 dots
# 9 mazes exist

from collections import deque
import time

class MazeDisplayer:
	def __init__(self, highlights={}):
		self.v_wall = "|" # vertical wall
		self.h_wall = "-" # horizontal wall
		self.gap    = "." # lack of a wall
		self.cross  = "+" # for display purposes, to space between horizontal 'lack of walls'
		self.tile   = "*" # a floor tile in the maze
		self.header = "="
		self.header_size = 40
		self.header_end  = 5
		self.highlights = highlights

	def addHighlight(pos, char):
		if len(char) > 1:
			char = char[0]
		if len(char) < 1:
			char = " "
		self.highlights[pos] = char

	def mazeHeader(self, maze):
		return self.header * (self.header_size-len(maze.getName())-self.header_end) + maze.getName() + self.header * (self.header_end)

	def mazeFooter(self, maze):
		return self.header * (self.header_size)

	def mazeCap(self, maze):
		return self.cross + (self.h_wall * (maze.getSize() * 2 - 1)) + self.cross

	def getTile(self, pos):
		if pos in self.highlights:
			return self.highlights[pos]
		return self.tile

	def mazeBody(self, maze, rulers=False, highlight=True):
		out = ""
		out += self.mazeCap(maze) + (" v row" if rulers else "") + "\n"
		for i in range(0, maze._size + maze._size - 1):
			rowout = ""
			row = i // 2
			if i % 2 == 0:
				rowout = self.v_wall
				for col in range(0, maze._size):
					rowout += self.getTile((row, col)) if highlight else self.tile
					if col < maze._size-1:
						if maze.hasAdjacent((row, col), (row, col+1)):
							rowout += self.gap
						else:
							rowout += self.v_wall
					else: # right wall
						rowout += self.v_wall + ((" " + str(row)) if rulers else "")
			else:
				rowout = self.v_wall
				for col in range(0, maze._size):
					if maze.hasAdjacent((row, col), (row+1, col)):
						rowout += self.gap
					else: 
						rowout += self.h_wall
					if col < maze._size-1:
						rowout += self.cross
					else: # right wall
						rowout += self.v_wall
			out += rowout + "\n"
		out += self.mazeCap(maze)
		return out

	def show(self, maze, rulers=True, highlight=True):
		print(self.mazeHeader(maze))
		if rulers:
			print( ' ' + ' '.join([str(x) for x in range(0,maze.getSize())]) + "  < column" )
		print(self.mazeBody(maze, rulers, highlight))
		print(self.mazeFooter(maze))

class MazeIdentifier:
	def __init__(self):
		self.mazes = {}

	def putMaze(self, dot1, dot2, maze):
		if self.getMaze(dot1, dot2):
			print("Overwriting maze (" + maze.getName() + ") in maze identifier")
		self.mazes[(dot1, dot2)] = maze

	def getMaze(self, dot1, dot2):
		if (dot1, dot2) in self.mazes:
			return self.mazes[(dot1, dot2)]
		elif (dot2, dot1) in self.mazes:
			return self.mazes[(dot2, dot1)]
		else:
			return None

	def getMazeAt(self, index):
		mazecount = len(self.mazes.keys())
		if index < mazecount:
			return self.mazes[list(self.mazes.keys())[index]]
		return None

class MazeSolver:
	@staticmethod
	def makePath(prev, src, dst):
		path = deque([dst])
		while path[0] != src:
			path.appendleft( prev[path[0]] )
		return list(path)

	@staticmethod
	def pathAsEdges(path):
		edges = []
		for i in range(len(path)-1):
			edges.append( (path[i], path[i+1]) )
		return edges
		
	@staticmethod
	def buildInstructions(solution):
		return [ Maze.dirs[Maze.direction(edge[0], edge[1])] for edge in MazeSolver.pathAsEdges( solution ) ]

	def id(self):
		raise NotImplementedError("MazeSolver is abstract, provide an ID")

	def solve(self, maze, src, dst):
		# find a series of edges that go from src to dst
		# should return list of edges (pairs of vertices)
		# OR return as a list of vertices
		# first should be src, last should be dst
		# with an existing edge from each to the following list element
		raise NotImplementedError("MazeSolver is abstract, use an implementation of it")

	def readablySolve(self, maze, src, dst):
		return MazeSolver.buildInstructions( self.solve(maze, src, dst) )


class BDFSSolver(MazeSolver):
	def __init__(self, bfs=True):
		self._bfs = bfs

	def id(self):
		if(self._bfs):
			return "BFS"
		else:
			return "DFS"

	def solve(self, maze, src, dst):
		if not maze.valid(src):
			print("[err] Start was not inside maze.")
			return None
		if not maze.valid(dst):
			print("[err] End was not inside maze.")
			return None

		adj = maze.getAdjacency()
		visited = set() # where have we looed / enqueued?
		prev = {} # where did we come from to get to the index?
		toCheck = deque([src]) # queue
		curr = src
		while curr != dst:
			if self._bfs:
				curr = toCheck.popleft() # one line difference
			else:
				curr = toCheck.pop()

			if curr in adj:
				for nxt in adj[curr]:
					if nxt not in visited:
						visited.add( nxt )
						toCheck.append( nxt )
						if nxt not in prev:
							prev[nxt] = curr
			else:
				continue
		return MazeSolver.makePath(prev, src, dst)

class Maze:
	# this is static or something idk
	dirs = {0:"center", 1:"up", 2:"right", 3:"down", 4:"left"}

	def __init__(self, to_parse="",empty=False, size=6, name="MAAAAZE"):
		self._name = name
		self._size = size
		self._adjacency = {}

		if len(to_parse) > 0:
			self._parse(to_parse)

		if empty: # no walls between any cells
			for i in range(self._size):
				for j in range(self._size):
					self.addToAdjacency((i, j), (i+1, j))
					self.addToAdjacency((i, j), (i, j+1))
		return

	@staticmethod
	def nextTo(pos1, pos2): # is pos1 physically / geometrically bordering pos2?
		# returns True if pos1 is pos2
		if abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) > 1:
			return False
		return True

	def getName(self):
		return self._name

	def getSize(self):
		return self._size

	def getAdjacency(self):
		return self._adjacency

	def addToAdjacency(self, pos1, pos2):
		if (not self.valid(pos1)) or (not self.valid(pos2)):
			print("[err] failed to add adjacency: invalid tile position")
			return
		if not Maze.nextTo(pos1, pos2):
			print("[wrn] trying to add adjacency for non-touching maze tiles")
		if pos1 not in self._adjacency:
			self._adjacency[pos1] = []
		if pos2 not in self._adjacency:
			self._adjacency[pos2] = []
		self._adjacency[pos1].append(pos2)
		self._adjacency[pos2].append(pos1)

	def _parse(self, stronk, AIR="."):
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

	def valid(self, pos):
		return 0 <= pos[0] < self._size and 0 <= pos[1] < self._size

	def hasAdjacent(self, pos1, pos2):
		if pos1 not in self._adjacency:
			return False
		return pos2 in self._adjacency[pos1]

	@staticmethod
	def direction(pos1, pos2):
		if not Maze.nextTo(pos1, pos2):
			return None
		if pos1 == pos2:
			return 0
		d1 = pos1[0] - pos2[0]
		if d1 == 1:
			return 1 # up
		if d1 == -1:
			return 3 # down
		d2 = pos1[1] - pos2[1]
		if d2 == 1:
			return 4 # right
		if d2 == -1:
			return 2 # left
		print("[wrn] this shouldn't happen (couldn't determine direction of tile)")
		return None

	def showAdjacency(self):
		for i in range(self._size):
			for j in range(self._size):
				if (i, j) in self._adjacency:
					print( str((i, j)) + ": " + str( self._adjacency[(i, j)] ))
				else:
					print( str((i, j)) + ": No adjacent vertices. :(")
	
	def show(self, displayer=MazeDisplayer(), rulers=False, highlight=False):
		displayer.show(self)

def compare_solvers(maze, solver1, solver2):
	wins_1 = 0
	wins_2 = 0

	time_1 = 0
	time_2 = 0

	ties = 0

	print("starting test showdown between " + solver1.id() + " and " + solver2.id())
	for x1 in range(6):
		for x2 in range(6):
			for y1 in range(6):
				for y2 in range(6):
					s1_start = time.clock()
					s1 = solver1.solve(maze, (x1, y1), (x2, y2))
					s_middle = time.clock()
					s2 = solver2.solve(maze, (x1, y1), (x2, y2))
					s2_end = time.clock()

					time_1 += s_middle - s1_start
					time_2 += s2_end - s_middle

					#print(len(s1),s1)
					#print(len(s2),s2)
					if len(s1) != len(s2):
						if len(s1) < len(s2):
							wins_1 += 1
						else:
							wins_2 += 1
					else:
						ties += 1
	print("done")
	print(solver1.id() + " won " + str(wins_1) + " times, taking " + str(round(time_1,10)) + " arbitrary time units (seconds)")
	print(solver2.id() + " won " + str(wins_2) + " times, taking " + str(round(time_2,10)) + " arbitrary time units (seconds)")
	print("Solvers tied " + str(ties) + " times.")


def build_m1_identifier():
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
*.*.*|*.*.*
-+.+-+.+.+-
*.*|*.*|*.*
.+-+.+-+-+.
*|*.*|*.*.*
.+.+-+.+-+.
*.*|*.*|*|*
.+-+.+-+.+.
*|*|*|*.*|*
.+.+.+.+-+.
*|*.*|*.*.*
'''

	m3 = '''
*.*.*|*|*.*
.+-+.+.+.+.
*|*|*|*.*|*
-+.+.+-+-+.
*.*|*|*.*|*
.+.+.+.+.+.
*|*|*|*|*|*
.+.+.+.+.+.
*|*.*|*|*|*
.+-+-+.+.+.
*.*.*.*|*.*
'''

	m4 = '''
*.*|*.*.*.*
.+.+-+-+-+.
*|*|*.*.*.*
.+.+.+-+-+.
*|*.*|*.*|*
.+-+-+.+-+.
*|*.*.*.*.*
.+-+-+-+-+.
*.*.*.*.*|*
.+-+-+-+.+.
*.*.*|*.*|*
'''

	m5 = '''
*.*.*.*.*.*
-+-+-+-+.+.
*.*.*.*.*|*
.+-+-+.+-+-
*.*|*.*|*.*
.+.+-+-+.+.
*|*.*.*|*|*
.+-+-+.+-+.
*|*.*.*.*|*
.+.+-+-+-+.
*|*.*.*.*.*
'''

	m6 = '''
*|*.*|*.*.*
.+.+.+-+.+.
*|*|*|*.*|*
.+.+.+.+-+.
*.*|*|*|*.*
.+-+-+.+.+-
*.*|*.*|*|*
-+.+.+.+.+.
*.*|*|*|*.*
.+-+-+.+-+.
*.*.*.*|*.*
'''

	m7 = '''
*.*.*.*|*.*
.+-+-+.+.+.
*|*.*|*.*|*
.+.+-+-+-+.
*.*|*.*|*.*
-+-+.+-+.+-
*.*|*.*.*|*
.+.+.+-+-+.
*|*|*.*.*|*
.+-+-+-+.+.
*.*.*.*.*.*
'''

	m8 = '''
*|*.*.*|*.*
.+.+-+.+.+.
*.*.*|*.*|*
.+-+-+-+-+.
*|*.*.*.*|*
.+.+-+-+.+.
*|*.*|*.*.*
.+-+.+-+-+-
*|*|*.*.*.*
.+.+-+-+-+-
*.*.*.*.*.*
'''

	m9 = '''
*|*.*.*.*.*
.+.+-+-+.+.
*|*|*.*|*|*
.+.+.+-+.+.
*.*.*|*.*|*
.+-+-+.+-+.
*|*|*.*|*.*
.+.+.+-+-+.
*|*|*|*.*|*
.+.+.+.+.+-
*.*|*.*|*.*
'''

	midf = MazeIdentifier()
	midf.putMaze( (1, 0), (2, 5), Maze(m1, name="maze1") )
	midf.putMaze( (3, 1), (1, 4), Maze(m2, name="maze2") )
	midf.putMaze( (3, 3), (3, 5), Maze(m3, name="maze3") )
	midf.putMaze( (0, 0), (3, 0), Maze(m4, name="maze4") )
	midf.putMaze( (2, 4), (5, 3), Maze(m5, name="maze5") )
	midf.putMaze( (0, 4), (4, 2), Maze(m6, name="maze6") )
	midf.putMaze( (0, 1), (5, 1), Maze(m7, name="maze7") )
	midf.putMaze( (0, 3), (3, 2), Maze(m8, name="maze8") )
	midf.putMaze( (1, 2), (4, 0), Maze(m9, name="maze9") )
	return midf

# Shows maze, then gets solution to the maze in easy readable form.
# maze: the Maze object to solve
# start: start position, integer coordinate tuple
# end:	ending position, integer coordinate tuple
# solver: MazeSolver to use
def getSolutionInstructions(maze, start, end, solver=BDFSSolver()):
	MazeDisplayer({start:"S",end:"E"}).show(maze)
	return solver.readablySolve(maze, start, end)
	#print("unweighted distance is " + str(len(instructions)) + " from " + str(start) + " to " + str(end) + " by following directions " +str( instructions ) )

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

	t1 = '''
*.*.*|*.*.*
.+-+.+.+-+-
*|*.*|*.*.*
.+.+-+.+-+.
*.*.*|*.*.*
.+.+.+.+-+.
*|*.*.*|*.*
.+-+.+-+-+.
*.*.*|*.*|*
.+-+.+.+.+.
*.*|*.*|*.*
'''
	midf = build_m1_identifier()
	
	maze1 = midf.getMazeAt(0)#( (4, 0), (1, 2) )
	#maze1.showAdjacency()
	#MazeDisplayer().show(maze1)
	#maze1.show() # does same thing as MazeDisplayer().show(maze1)

	p1 = (1, 1)
	p2 = (4, 5)

	#print( Maze.dirs[maze1.direction( (2, 4), (2, 3) )] )
	#compare_solvers(maze1, BDFSSolver(True), BDFSSolver(False))

	instructions = getSolutionInstructions(maze1, p1, p2) #[ Maze.dirs[Maze.direction(edge[0], edge[1])] for edge in MazeSolver.pathAsEdges( BDFSSolver().solve(maze1, p1, p2) ) ]
	print("unweighted distance is " + str(len(instructions)) + " from " + str(p1) + " to " + str(p2) + " by following directions " +str( instructions ) )
