import random

# =========================
# STACK
# =========================
class Stack:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)

    def pop(self):
        return self.data.pop()

    def peek(self):
        return self.data[-1]

    def isEmpty(self):
        return len(self.data) == 0


# =========================
# CELL
# =========================
class Cell:
    def __init__(self, r, c):
        self.row = r
        self.col = c


# =========================
# MAZE
# =========================
class Maze:
    MAZE_WALL = "*"
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = [[None for _ in range(cols)] for _ in range(rows)]
        self.start = None
        self.exit = None

    def setWall(self, r, c):
        self.maze[r][c] = self.MAZE_WALL

    def setStart(self, r, c):
        self.start = Cell(r, c)

    def setExit(self, r, c):
        self.exit = Cell(r, c)

    def _validMove(self, r, c):
        return (0 <= r < self.rows and
                0 <= c < self.cols and
                self.maze[r][c] is None)

    def _exitFound(self, r, c):
        return (r == self.exit.row and c == self.exit.col)

    def findPath(self):
        stack = Stack()
        stack.push((self.start.row, self.start.col))
        self.maze[self.start.row][self.start.col] = self.PATH_TOKEN

        while not stack.isEmpty():
            r, c = stack.peek()

            if self._exitFound(r, c):
                return True

            moved = False
            for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
                nr, nc = r + dr, c + dc

                if self._validMove(nr, nc):
                    self.maze[nr][nc] = self.PATH_TOKEN
                    stack.push((nr, nc))
                    moved = True
                    break

            if not moved:
                self.maze[r][c] = self.TRIED_TOKEN
                stack.pop()

        return False

    def draw(self):
        for r in range(self.rows):
            row = ""
            for c in range(self.cols):
                if self.start and r == self.start.row and c == self.start.col:
                    row += "S "
                elif self.exit and r == self.exit.row and c == self.exit.col:
                    row += "E "
                elif self.maze[r][c] is None:
                    row += ". "
                else:
                    row += self.maze[r][c] + " "
            print(row)
        print()


# =========================
# BUILD MAZE ACAK
# =========================
def buildMaze(rows, cols):
    m = Maze(rows, cols)

    # set start & exit
    m.setStart(0, 0)
    m.setExit(rows-1, cols-1)

    # buat jalur yang pasti dulu (diagonal random)
    r, c = 0, 0
    path = [(r, c)]

    while (r, c) != (rows-1, cols-1):
        if random.choice([True, False]):
            if c < cols-1:
                c += 1
        else:
            if r < rows-1:
                r += 1
        path.append((r, c))

    # isi maze
    for i in range(rows):
        for j in range(cols):
            if (i, j) in path:
                continue  # jalur aman
            if random.random() < 0.35:
                m.setWall(i, j)

    return m


# =========================
# MAIN
# =========================
maze = buildMaze(10, 10)

print("=== MAZE AWAL ===")
maze.draw()

if maze.findPath():
    print("=== MAZE SOLVED ===")
    maze.draw()
else:
    print