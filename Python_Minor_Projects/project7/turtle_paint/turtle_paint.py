import turtle

# Canvas setup
screen = turtle.Screen()
screen.title("🎨 Interactive GUI Paint Canvas (with Eraser Tool)")
screen.bgcolor("#2C3E50")
screen.setup(width=900, height=700)

# Main Drawing Pen
pen = turtle.Turtle()
pen.shape("circle")
pen.shapesize(0.4, 0.4)
pen.color("white")
pen.pensize(3)
pen.speed(0)

# UI Pen
ui_pen = turtle.Turtle()
ui_pen.hideturtle()
ui_pen.penup()
ui_pen.speed(0)

current_color = "white"
current_size = 3
is_eraser = False

colors = [
    ("#FFFFFF", "White", -380),
    ("#E74C3C", "Red", -320),
    ("#2ECC71", "Green", -260),
    ("#3498DB", "Blue", -200),
    ("#F1C40F", "Yellow", -140),
    ("#9B59B6", "Purple", -80),
    ("#E67E22", "Orange", -20),
]

# Eraser Button Position
ERASER_X = 50

def draw_ui():
    """Draws top toolbar with color palette and Eraser button."""
    ui_pen.clear()
    
    # Top Panel Background
    ui_pen.goto(-430, 320)
    ui_pen.color("#34495E")
    ui_pen.begin_fill()
    for _ in range(2):
        ui_pen.forward(860)
        ui_pen.right(90)
        ui_pen.forward(70)
        ui_pen.right(90)
    ui_pen.end_fill()

    # Draw Color Buttons
    for hex_code, name, x_pos in colors:
        ui_pen.goto(x_pos, 280)
        ui_pen.color(hex_code)
        ui_pen.begin_fill()
        ui_pen.circle(18)
        ui_pen.end_fill()

    # Draw Eraser Button
    ui_pen.goto(ERASER_X, 280)
    ui_pen.color("#7F8C8D" if not is_eraser else "#E74C3C")
    ui_pen.begin_fill()
    ui_pen.circle(18)
    ui_pen.end_fill()
    
    ui_pen.color("white")
    ui_pen.goto(ERASER_X - 12, 290)
    ui_pen.write("🧹", font=("Arial", 14, "normal"))

    # Active Tool Display & Controls Info
    mode_text = "MODE: ERASER 🧹" if is_eraser else "MODE: DRAW 🎨"
    ui_pen.goto(130, 285)
    ui_pen.write(f"Size: {current_size}px | {mode_text}\n[C] Clear Canvas | [+] Size Up | [-] Size Down", 
                 font=("Arial", 10, "bold"))

# Mouse Handlers
def handle_click(x, y):
    global current_color, is_eraser
    # Check if clicked inside top UI panel
    if y > 250:
        # Check Color palette clicks
        for hex_code, name, x_pos in colors:
            if (x - x_pos)**2 + (y - 298)**2 <= 20**2:
                is_eraser = False
                current_color = hex_code
                pen.color(current_color)
                draw_ui()
                return

        # Check Eraser button click
        if (x - ERASER_X)**2 + (y - 298)**2 <= 20**2:
            is_eraser = True
            pen.color("#2C3E50")  # Matches canvas background to erase
            draw_ui()
            return
    else:
        pen.penup()
        pen.goto(x, y)
        pen.pendown()

def draw_motion(x, y):
    """Triggers on dragging the pen/eraser across canvas."""
    if y < 250:
        pen.pendown()
        pen.goto(x, y)

# Key Handlers
def clear_canvas():
    pen.clear()
    draw_ui()

def increase_size():
    global current_size
    current_size = min(50, current_size + 2)
    pen.pensize(current_size)
    draw_ui()

def decrease_size():
    global current_size
    current_size = max(1, current_size - 2)
    pen.pensize(current_size)
    draw_ui()

# Bind Events
draw_ui()
screen.listen()

# Screen click moves pen to starting point or selects color/eraser
screen.onclick(handle_click)

# Pen drag draws/erases continuously on canvas
pen.ondrag(draw_motion)

# Keyboard controls
screen.onkeypress(clear_canvas, "c")
screen.onkeypress(clear_canvas, "C")
screen.onkeypress(increase_size, "plus")
screen.onkeypress(increase_size, "equal")
screen.onkeypress(decrease_size, "minus")

try:
    screen.mainloop()
except (turtle.Terminator, Exception):
    print("\n🎨 Paint Canvas Closed!")
