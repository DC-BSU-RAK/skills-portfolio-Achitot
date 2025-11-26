from tkinter import *
from tkinter import font
from PIL import ImageTk, Image
import random

root = Tk()
root.title("ArithMix")
root.geometry('595x842')
root.resizable(0, 0)

difficulty = None
question_count = 0
score = 0
first_attempt = True
current_answer = 0

frame1 = Frame(root) #Starting Screen
frame2 = Frame(root) #Next Screen
menu_frame = Frame(root) #Difficulty Selection
game_frame = Frame(root) #Game Section
result_frame = Frame(root)  # Results Frame

for frame in (frame1, frame2, menu_frame, game_frame, result_frame):
    frame.place(x=0, y=0, relwidth=1, relheight=1)

# ------------------- Frame 1 - Starting Screen ------------------- 

image1 = Image.open('Exercise 1/Images/1.png')
image1 = image1.resize((595, 842), Image.LANCZOS)
bg1 = ImageTk.PhotoImage(image1)
bg_label1 = Label(frame1, image=bg1)
bg_label1.place(x=0, y=0, relwidth=1, relheight=1)

def go_to_frame2():
    frame2.tkraise()

start_button = Button(frame1,
                      text="Start",
                      font=("Arial", 25),
                      bg="#74a050",
                      activebackground="#74a050",
                      bd=0,
                      command=go_to_frame2)
start_button.place(x=255, y=318)

# ------------------- Frame 2 - Next Screen -------------------
image2 = Image.open('Exercise 1/Images/2.png')
image2 = image2.resize((595, 842), Image.LANCZOS)
bg2 = ImageTk.PhotoImage(image2)
bg_label2 = Label(frame2, image=bg2)
bg_label2.place(x=0, y=0, relwidth=1, relheight=1)

def displayMenu():
    menu_frame.tkraise()

next_button = Button(frame2,
                     text="Next",
                     width=10, 
                     height=1,
                     font=("Arial", 9),
                     bg="#c0c0c0",
                     activebackground="#c0c0c0",
                     bd=0,
                     command=displayMenu)
next_button.place(x=408, y=510)

# ------------------- Menu Frame -------------------
menu_img = Image.open('Exercise 1/Images/3.png')
menu_img = menu_img.resize((595, 842), Image.LANCZOS)
menu_bg = ImageTk.PhotoImage(menu_img)
menu_bg_label = Label(menu_frame, image=menu_bg)
menu_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def start_quiz(selected_difficulty):
    global difficulty, score, question_count
    difficulty = selected_difficulty
    score = 0
    question_count = 0
    score_label.config(text=f"Score: {score}")
    generate_question()
    game_frame.tkraise()

Button(menu_frame, text="1. Easy (1-digit)", 
            font=("Arial", 10),
            bg="#74a050",
            activebackground="#74a050",
            bd=0,
            command=lambda: start_quiz("Easy")).place(x=246, y=264)

Button(menu_frame, text="2. Moderate (2-digit)",
       font=("Arial", 10),
            bg="#74a050",
            activebackground="#74a050",
            bd=0,
            command=lambda: start_quiz("Moderate")).place(x=238, y=345)

Button(menu_frame, text="3. Advanced (4-digit)",
       font=("Arial", 10),
            bg="#74a050",
            activebackground="#74a050",
            bd=0,
            command=lambda: start_quiz("Advanced")).place(x=238, y=425)


def randomInt(min_value, max_value):
    return random.randint(min_value, max_value)

def decideOperation():
    return random.choice(["+", "-"])

def displayProblem(num1, num2, operation):
    question_label.config(text=f"{num1} {operation} {num2} = ?")

def isCorrect(user_answer, correct_answer):
    if user_answer == correct_answer:
        feedback_label.config(text="Correct!")
        return True
    else:
        feedback_label.config(text="Wrong!")
        return False

def displayResults(score):
    result_label.config(text=f"Score: {score}/100")
    result_frame.tkraise()

def get_digit_range():
    if difficulty == "Easy":
        return 1, 9
    elif difficulty == "Moderate":
        return 10, 99
    else:
        return 1000, 9999

def generate_question():
    global current_answer, first_attempt, question_count

    if question_count == 10:
        displayResults(score)
        return

    first_attempt = True
    question_count += 1
    question_number_label.config(text=f"Question {question_count}/10")

    # Get digits based on difficulty
    min_value, max_value = get_digit_range()

    num1 = randomInt(min_value, max_value)
    num2 = randomInt(min_value, max_value)

    operation = decideOperation()

    # Compute answer
    if operation == "+":
        current_answer = num1 + num2
    else:
        current_answer = num1 - num2

    # Display problem
    displayProblem(num1, num2, operation)

    answer_entry.delete(0, END)

def check_answer():
    global score, first_attempt

    try:
        user_answer = int(answer_entry.get())
    except:
        feedback_label.config(text="Enter a valid number!")
        return

    correct = isCorrect(user_answer, current_answer)

    if correct:
        if first_attempt:
            score += 10
        else:
            score += 5

        score_label.config(text=f"Score: {score}")
        root.after(800, generate_question)

    else:
        if first_attempt:
            first_attempt = False
            feedback_label.config(text="Wrong! Try again.")
            answer_entry.delete(0, END)
        else:
            feedback_label.config(text=f"Wrong again! Answer: {current_answer}")
            root.after(1200, generate_question)

# ------------------- Game Frame -------------------
image3 = Image.open('Exercise 1/Images/4.png')
image3 = image3.resize((595, 842), Image.LANCZOS)
game_bg = ImageTk.PhotoImage(image3)
game_bg_label = Label(game_frame, image=game_bg)
game_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

score_label = Label(game_frame, text="Score: 0", font=("Arial", 20), bg="#abd4ef")
score_label.place(x=365, y=160)

question_number_label = Label(game_frame, text="Question 1/10", font=("Arial", 22), bg="#fddf87")
question_number_label.place(x=210, y=250)

question_label = Label(game_frame, text="", font=("Arial", 28), bg="#fddf87")
question_label.place(x=215, y=300)

answer_entry = Entry(game_frame, font=("Arial", 22), width=10, justify="center")
answer_entry.place(x=245, y=430)

submit_btn = Button(game_frame, text="Submit Answer", font=("Arial", 8), 
                    bg="#c0c0c0", activebackground="#c0c0c0", bd=0,
                    command=check_answer)
submit_btn.place(x=330, y=510)

feedback_label = Label(game_frame, text="", font=("Arial", 12), bg="#fddf87")
feedback_label.place(x=220, y=350)

Button(game_frame, text="Back to Menu", font=("Arial", 8), bg="#c0c0c0",
       activebackground="#c0c0c0", bd=0,
       command=displayMenu).place(x=120, y=510)

# ------------------- Results Frame -------------------
result_bg = Image.open('Exercise 1/Images/5.png')
result_bg = result_bg.resize((595, 842), Image.LANCZOS)
result_bg_img = ImageTk.PhotoImage(result_bg)
result_bg_label = Label(result_frame, image=result_bg_img)
result_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

result_label = Label(result_frame, text="", font=("Arial", 32, "bold"), bg="white")
result_label.place(x=145, y=205)

Button(result_frame, text="Return to Menu", font=("Arial", 9), bg="#c0c0c0",
                    activebackground="#c0c0c0", bd=0, 
                    command=displayMenu).place(x=395, y=510)

frame1.tkraise()

root.mainloop()