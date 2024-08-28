#MODULES
from tkinter import *
import random
import csv
import os

#GAME SETTING
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100  
SPACE_SIZE = 40
BODY_PARTS = 3
SNAKE_COLOR = "#80AF81"
FOOD_COLOR = "#FF4191"
BACKGROUND_COLOR = "#373A40"
HIGH_SCORE_FILE = "high_score.csv"

#CLASS SNAKE THAT DRAWS THE SNAKE BODY AND DEFINES IT'S BODY
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
            self.squares.append(square)

#FOR RANDOM GENERATION OF FOOD ANYWHERE IN THE CANVAS
class Food:
    def __init__(self, snake_coordinates):
        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            self.coordinates = [x, y]

            if self.coordinates not in snake_coordinates:
                break

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags="food")
        print(f"New food created at {self.coordinates}")  # Debug print

#SNAKE CONTROL
def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        print(f"Score updated: {score}")  
        canvas.delete("food")
        food = Food(snake.coordinates)
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        print("Collision with wall detected.")  # Debug print
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("Collision with self detected.")  # Debug print
            return True

    return False

def game_over():
    global high_score

    if score > high_score:
        high_score = score
        save_high_score(high_score)

    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2, text="GAME OVER", font=('consolas', 70), fill="red", tags="gameover")
    window.update()
    window.bind('<r>', restart_game)

def restart_game(event):
    global score, direction, snake, food
    score = 0
    direction = "down"
    canvas.delete("all")
    label.config(text="Score:{}".format(score))
    snake = Snake()
    food = Food(snake.coordinates)
    window.unbind('<r>')
    next_turn(snake, food)

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                return int(row[0])
    return 0

def save_high_score(high_score):
    with open(HIGH_SCORE_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([high_score])

window = Tk()
window.title("Snake")
window.resizable(False, False)

score = 0
direction = "down"
high_score = load_high_score()

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

high_score_label = Label(window, text="High Score:{}".format(high_score), font=('consolas', 20))
high_score_label.pack()

#KEYBINDS FOR THE KEEB
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food(snake.coordinates)

next_turn(snake, food)

window.mainloop()
