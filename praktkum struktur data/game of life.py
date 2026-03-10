import time
import copy

# Ukuran grid
ROWS = 5
COLS = 5

# Membuat grid awal (0 = mati, 1 = hidup)
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

# Fungsi untuk menampilkan grid
def print_grid(grid):
    for row in grid:
        for cell in row:
            if cell == 1:
                print("■", end=" ")
            else:
                print(".", end=" ")
        print()
    print()

# Fungsi menghitung tetangga hidup
def count_neighbors(grid, row, col):
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1)
    ]

    count = 0
    for dr, dc in directions:
        r = row + dr
        c = col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            count += grid[r][c]
    return count

# Fungsi untuk membuat generasi berikutnya
def next_generation(grid):
    new_grid = copy.deepcopy(grid)

    for row in range(ROWS):
        for col in range(COLS):
            neighbors = count_neighbors(grid, row, col)

            if grid[row][col] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[row][col] = 0
            else:
                if neighbors == 3:
                    new_grid[row][col] = 1

    return new_grid

# Menjalankan simulasi
for generation in range(5):
    print("Generasi:", generation)
    print_grid(grid)
    grid = next_generation(grid)
    time.sleep(1)
