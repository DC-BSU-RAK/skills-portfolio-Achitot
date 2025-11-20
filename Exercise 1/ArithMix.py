from tkinter import *
from tkinter import font
from PIL import ImageTk, Image

root = Tk()
root.title("ArithMix")
root.geometry('595x842')
root.resizable(0, 0)


frame1 = Frame(root)
frame2 = Frame(root)

for frame in (frame1, frame2):
    frame.place(x=0, y=0, relwidth=1, relheight=1)


image1 = Image.open('Images/1.png')
image1 = image1.resize((595, 842), Image.LANCZOS)
bg1 = ImageTk.PhotoImage(image1)

bg_label1 = Label(frame1, image=bg1)
bg_label1.place(x=0, y=0, relwidth=1, relheight=1)

def go_to_frame2():
    frame2.tkraise()

def go_to_frame1():
    frame1.tkraise()

start_button = Button(frame1,
                      text="Start",
                      font=("Arial", 25),
                      bg="#74a050",
                      activebackground="#74a050",
                      bd=0,
                      command=go_to_frame2)
start_button.place(x=255, y=318)


image2 = Image.open('Images/2.png')
image2 = image2.resize((595, 842), Image.LANCZOS)
bg2 = ImageTk.PhotoImage(image2)

bg_label2 = Label(frame2, image=bg2)
bg_label2.place(x=0, y=0, relwidth=1, relheight=1)

next_button = Button(frame2,
                     text="Next",
                     width=10, 
                     height=1,
                     font=("Arial", 9),
                     bg="#c0c0c0",
                     activebackground="#c0c0c0",
                     bd=0,
                     command=go_to_frame1)
next_button.place(x=408, y=510)

frame1.tkraise()

root.mainloop()
