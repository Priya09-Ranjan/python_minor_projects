import turtle
import time

# Sample Sudoku Puzzle (0 represents empty cells)
GRID = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Keep track of original puzzle numbers so they don't change
ORIGINAL = [[GRID[r][c] for c in range(9)] for r in range(9)]

CELL_SIZE = 50
START_X = -225
START_Y = 225

selected_row = -1
selected_col = -1

# Screen Setup
screen = turtle.Screen()
screen.title("🧩 REAL Interactive Sudoku Game & AI Visual Solver")
screen.bgcolor("#1E1E2E")  # Dark Catppuccin theme background
screen.setup(width=650, height=750)
screen.tracer(0)  # Turns off screen updates for smoother manual rendering

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)

def draw_grid():
    """Draws the main Sudoku board with stylized sub-grid borders."""
    pen.clear()
    
    # Highlight the selected cell visually
    if selected_row != -1 and selected_col != -1:
        x = START_X + selected_col * CELL_SIZE
        y = START_Y - selected_row * CELL_SIZE
        pen.penup()
        pen.goto(x, y)
        pen.color("#F5E0DC")  # Light highlight color
        pen.begin_fill()
        for _ in range(4):
            pen.forward(CELL_SIZE)
            pen.right(90)
        pen.end_fill()

    # Draw grid lines
    for i in range(10):
        # Line thickness/color differentiation for 3x3 blocks
        if i % 3 == 0:
            pen.pensize(4)
            pen.color("#89B4FA")  # Bright cyan-blue for block borders
        else:
            pen.pensize(1)
            pen.color("#45475A")  # Faded blue-gray for internal borders

        # Horizontal lines
        pen.penup()
        pen.goto(START_X, START_Y - i * CELL_SIZE)
        pen.pendown()
        pen.goto(START_X + 9 * CELL_SIZE, START_Y - i * CELL_SIZE)

        # Vertical lines
        pen.penup()
        pen.goto(START_X + i * CELL_SIZE, START_Y)
        pen.pendown()
        pen.goto(START_X + i * CELL_SIZE, START_Y - 9 * CELL_SIZE)

    # Draw all the numbers with color differentiation
    for r in range(9):
        for c in range(9):
            val = GRID[r][c]
            if val != 0:
                x = START_X + c * CELL_SIZE + 18  # Center text offset
                y = START_Y - r * CELL_SIZE - 40  # Center text offset
                pen.penup()
                pen.goto(x, y)
                
                # Original puzzle numbers in clear light blue, solver numbers in bright green
                if ORIGINAL[r][c] != 0:
                    pen.color("#89B4FA")
                else:
                    pen.color("#A6E3A1")
                    
                pen.write(str(val), font=("Verdana", 22, "bold"))

    # UI Controls Info
    pen.penup()
    pen.goto(0, -280)
    pen.color("#CDD6F4")
    pen.write("🎮 REAL Interactive Sudoku Game\nClick a cell & press [1-9] to guess | [BackSpace] to clear\nPress [S] for AI Auto-Solve Visualization", 
              align="center", font=("Verdana", 11, "bold"))

    screen.update()

# --- BACKTRACKING AI ALGORITHM (Validation & Solver) ---

def is_valid_guess(grid, r, c, val):
    """Checks if the number 'val' is valid at grid[r][c] per Sudoku rules."""
    # Check Row & Column
    for i in range(9):
        if grid[r][i] == val or grid[i][c] == val:
            return False
            
    # Check the 3x3 Sub-Grid block
    start_r, start_c = (r // 3) * 3, (c // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[start_r + i][start_c + j] == val:
                return False
    return True

def solve_sudoku_visual():
    """AI Backtracking Solver with visual updates (Watch it Solve!)."""
    for r in range(9):
        for c in range(9):
            if GRID[r][c] == 0:
                for val in range(1, 10):
                    if is_valid_guess(GRID, r, c, val):
                        GRID[r][c] = val
                        draw_grid()  # Force screen update to show animation
                        time.sleep(0.02)  # Delay makes the solving visual/understandable
                        
                        if solve_sudoku_visual():
                            return True
                            
                        # If guessing val didn't work, backtrack (undo)
                        GRID[r][c] = 0
                        draw_grid()
                return False
    return True

# --- INPUT HANDLING EVENTS ---

def handle_click(x, y):
    """Calculates cell coordinates based on screen click."""
    global selected_row, selected_col
    if START_X <= x <= START_X + 9 * CELL_SIZE and START_Y - 9 * CELL_SIZE <= y <= START_Y:
        selected_col = int((x - START_X) // CELL_SIZE)
        selected_row = int((START_Y - y) // CELL_SIZE)
    else:
        # Clicked outside the grid, clear selection
        selected_row, selected_col = -1, -1
    draw_grid()

def enter_number(val):
    """Processes keyboard input for number entry."""
    if selected_row != -1 and selected_col != -1:
        # Only allow user/solver to change numbers that are NOT original
        if ORIGINAL[selected_row][selected_col] == 0:
            # If valid (or zero to clear), set the number
            if val == 0 or is_valid_guess(GRID, selected_row, selected_col, val):
                GRID[selected_row][selected_col] = val
                draw_grid()

def trigger_ai_solve():
    """Resets interface focus and starts the visual solver."""
    global selected_row, selected_col
    selected_row, selected_col = -1, -1
    draw_grid()  # Refresh display
    solve_sudoku_visual()  # Start solver

# --- BIND INPUTS & START GAME ---

screen.listen()
screen.onclick(handle_click)

# Key bindings for numbers 1-9 and clearing (BackSpace)
for num in range(1, 10):
    screen.onkeypress(lambda n=num: enter_number(n), str(num))

screen.onkeypress(lambda: enter_number(0), "BackSpace")

# AI Auto-Solve trigger key
screen.onkeypress(trigger_ai_solve, "s")
screen.onkeypress(trigger_ai_solve, "S")

# Initial rendering
draw_grid()

try:
    screen.mainloop()
except (turtle.Terminator, Exception):
    print("\n🧩 Sudoku Game & Visual Solver Closed!")
