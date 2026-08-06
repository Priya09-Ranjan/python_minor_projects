import turtle
import time

# Screen Setup
screen = turtle.Screen()
screen.title("⏰ Aesthetic Digital Clock & Utility")
screen.bgcolor("#1E1E2E")
screen.setup(width=500, height=350)
screen.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()
pen.penup()

stopwatch_running = False
start_time = 0
elapsed_time = 0

def draw_ui():
    """Draws current time, date, and stopwatch status."""
    global elapsed_time
    pen.clear()
    
    # 1. Main Digital Clock
    current_time = time.strftime("%I:%M:%S %p")
    current_date = time.strftime("%A, %B %d, %Y")
    
    pen.goto(0, 50)
    pen.color("#89B4FA")  # Soft blue
    pen.write(current_time, align="center", font=("Arial", 36, "bold"))
    
    pen.goto(0, 10)
    pen.color("#A6ADC8")
    pen.write(current_date, align="center", font=("Arial", 12, "bold"))
    
    # Divider line
    pen.goto(-180, -20)
    pen.color("#45475A")
    pen.pendown()
    pen.goto(180, -20)
    pen.penup()
    
    # 2. Stopwatch Section
    if stopwatch_running:
        elapsed_time = time.time() - start_time
        
    mins, secs = divmod(int(elapsed_time), 60)
    time_str = f"{mins:02d}:{secs:02d}"
    
    pen.goto(0, -60)
    pen.color("#A6E3A1" if stopwatch_running else "#F38BA8")
    pen.write(f"Stopwatch: {time_str}", align="center", font=("Arial", 18, "bold"))
    
    pen.goto(0, -100)
    pen.color("#CDD6F4")
    pen.write("Press [SPACE] to Start/Pause | Press [R] to Reset", 
              align="center", font=("Arial", 10, "normal"))
    
    screen.update()

def toggle_stopwatch():
    global stopwatch_running, start_time, elapsed_time
    if stopwatch_running:
        stopwatch_running = False
    else:
        stopwatch_running = True
        start_time = time.time() - elapsed_time

def reset_stopwatch():
    global stopwatch_running, elapsed_time
    stopwatch_running = False
    elapsed_time = 0
    draw_ui()

# Controls
screen.listen()
screen.onkeypress(toggle_stopwatch, "space")
screen.onkeypress(reset_stopwatch, "r")
screen.onkeypress(reset_stopwatch, "R")

# Refresh loop (updates every 200 ms)
def update_loop():
    draw_ui()
    screen.ontimer(update_loop, 200)

update_loop()

try:
    screen.mainloop()
except (turtle.Terminator, Exception):
    print("\n⏰ Clock Closed!")
