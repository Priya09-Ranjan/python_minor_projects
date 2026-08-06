import turtle
import time
import random

delay = 0.15  # Continuous smooth speed
score = 0
high_score = 0

# Food counter for tracking 5-red to 1-gold cycle
red_eaten_count = 0
is_bonus_food = False

# Set up the screen
try:
    wn = turtle.Screen()
    wn.title("🐍 Continuous Boundary-Wrap Snake Game - Gold Edition")
    wn.bgcolor("black")
    wn.setup(width=600, height=600)
    wn.tracer(0)  # Turns off automatic screen updates
except Exception:
    pass

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 0)
head.direction = "stop"  # Continuous movement triggers on first key press

# Snake food (Default Red)
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# Score display
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 250)
pen.write("Score: 0  High Score: 0\nRed Food: 0/5", align="center", font=("Courier", 16, "normal"))

# Movement functions (Prevents 180-degree self-collision turns)
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    """Keeps the snake moving continuously in its current direction."""
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# Main Game Loop
running = True

try:
    while running:
        wn.update()

        # -------------------------------------------------------------
        # 🌐 BOUNDARY WRAP: Snake Wall se bahar jaate hi dusri taraf aayega
        # -------------------------------------------------------------
        if head.xcor() > 280:
            head.setx(-280)
        elif head.xcor() < -280:
            head.setx(280)

        if head.ycor() > 280:
            head.sety(-280)
        elif head.ycor() < -280:
            head.sety(280)

        # -------------------------------------------------------------
        # 🍎 FOOD COLLISION & 5-RED -> 1-GOLD CYCLE
        # -------------------------------------------------------------
        if head.distance(food) < 20:
            if is_bonus_food:
                points = 50  # Golden food gives 50 points
                is_bonus_food = False
                red_eaten_count = 0  # Reset counter for next 5 red cycle
                food.color("red")
                food.shapesize(1, 1)
            else:
                points = 10
                red_eaten_count += 1
                
                # Check if 5 Red Foods are eaten -> Spawn 1 Golden Food
                if red_eaten_count == 5:
                    is_bonus_food = True
                    food.color("gold")
                    food.shapesize(1.3, 1.3)

            # Move food to new random location
            x = random.randint(-260, 260)
            y = random.randint(-260, 260)
            food.goto(x, y)

            # Add body segment
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("gold" if points == 50 else "lightgreen")
            new_segment.penup()
            segments.append(new_segment)

            # Update score
            score += points
            if score > high_score:
                high_score = score
            
            pen.clear()
            status_text = "🌟 GOLDEN FOOD! (+50 Pts)" if is_bonus_food else f"Red Food: {red_eaten_count}/5"
            pen.write(f"Score: {score}  High Score: {high_score}\n{status_text}", align="center", font=("Courier", 16, "normal"))

        # Move body segments in reverse order
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)

        # Move snake head forward
        move()

        # -------------------------------------------------------------
        # 💀 SELF-COLLISION: Game Over Tabhi Hoga Jab Snake Apne Aap Se Takraye
        # -------------------------------------------------------------
        for segment in segments:
            if segment.distance(head) < 20:
                time.sleep(0.5)
                head.goto(0, 0)
                head.direction = "stop"  # Wait for next arrow key press
                
                # Reset food properties
                food.color("red")
                food.shapesize(1, 1)
                is_bonus_food = False
                red_eaten_count = 0

                for seg in segments:
                    seg.goto(1000, 1000)
                
                segments.clear()
                score = 0
                delay = 0.15
                pen.clear()
                pen.write(f"Score: {score}  High Score: {high_score}\nRed Food: {red_eaten_count}/5", align="center", font=("Courier", 16, "normal"))

        time.sleep(delay)

except (turtle.Terminator, Exception):
    print("\n🎮 Game window closed successfully!")
