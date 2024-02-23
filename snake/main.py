from tkinter import *
from PIL import Image, ImageTk
import random

Game_width = 700
Game_height = 700
speed = 300
space_size = 50
body_parts = 3
snake_clr = "#6d071a"
food_clr = "#18255c"
bg_clr = "white"
food_images = ["apple.png", "sandwich.png", "cake.png","donut.png","pizza.png","ananas.png","strawberry.png"]  

class Snake:
    def __init__(self):
        self.body_size = body_parts
        self.coordinates = []
        self.squares = []
        
        for i in range(body_parts):
            self.coordinates.append([0, 0])
        
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_clr, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        food_image_path = random.choice(food_images)
        image = Image.open(food_image_path)
        image = image.resize((space_size, space_size), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)
      
        x = random.randint(0, (Game_width // space_size) - 1) * space_size
        y = random.randint(0, (Game_height // space_size) - 1) * space_size
        self.coordinates = [x, y]
        
        self.food_image = canvas.create_image(x, y, image=self.image, anchor=NW, tag="food")

def next_turn(snake, food):
    global speed
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= space_size
    elif direction == "down":
        y += space_size
    elif direction == "left":
        x -= space_size
    elif direction == "right":
        x += space_size
    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_clr)
    snake.squares.insert(0, square)
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 2
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()
        if score % 20 == 0:
            speed -= 50
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    if check_collisions(snake):
        game_over()
    else:
        window.after(speed, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction in ("up", "down", "left", "right"):
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= Game_width or y < 0 or y >= Game_height:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False



def game_over():
    canvas.delete(ALL)
    game_over_text = canvas.create_text(Game_width // 2, Game_height // 2, font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    restart_button = Button(window, text="Restart", command=restart_game,bg="#18255c",fg="white",width=20)
    quit_button = Button(window, text="Quit", command=window.quit,bg="#6d071a",fg="white",width=20)
    canvas.create_window(Game_width // 2, Game_height // 2 + 100, window=restart_button)
    canvas.create_window(Game_width // 2, Game_height // 2 + 150, window=quit_button)

    
def restart_game():
    global score, direction, speed
    score = 0
    direction = "down"
    speed = 500
    label.config(text="Score: {}".format(score))
    canvas.delete("all")
    snake = Snake()
    food = Food()
    next_turn(snake, food)

window = Tk()
window.title("Snake Game")
window.resizable(False, False)
score = 0
direction = "down"
label = Label(window, text="Score: {}".format(score), font=("consolas", 40))
label.pack()
canvas = Canvas(window, bg=bg_clr, height=Game_height, width=Game_width)
canvas.pack()
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("<Up>", lambda event: change_direction("up"))
snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()
