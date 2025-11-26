import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

class JokeTeller:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joke Teller")
        self.root.geometry("500x300")
        root.resizable(0, 0)

        self.bg_image = ImageTk.PhotoImage(Image.open("Exercise 2/Background.png"))
        bg_label = tk.Label(root, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.jokes = self.load_jokes()
        self.current_joke = None
        
        self.create_buttons()
    
    def load_jokes(self):
        try:
            with open("Exercise 2/randomJokes.txt", "r") as file:
                return [line.strip() for line in file if line.strip()]
        except:
            return ["Resource Jokes not Loading..."]
    
    def create_buttons(self):
        # Tell Joke button
        self.tell_btn = tk.Button(self.root, text="Tell me the Joke", font=("Arial", 10), 
                                  bg="white", activebackground="white", bd=0,
                                  command=self.tell_joke)
        self.tell_btn.place(x=43, y=40)
        
        
        # Show Punchline button
        self.punch_btn = tk.Button(self.root, text="Show Punchline", 
                                  font=("Arial", 9),
                                  command=self.show_punchline, 
                                  state="disabled",
                                  bg="#c0c0c0", bd=1, relief="raised")
        self.punch_btn.place(x=200, y=20, width=100)
        
        # Next Joke button
        self.next_btn = tk.Button(self.root, text="Next Joke", 
                                 font=("Arial", 9),
                                 command=self.next_joke, 
                                 state="disabled",
                                 bg="#c0c0c0", bd=1, relief="raised")
        self.next_btn.place(x=310, y=20, width=80)
        
        # Quit button
        self.quit_btn = tk.Button(self.root, text="Quit", 
                                 font=("Arial", 9),
                                 command=self.root.quit,
                                 bg="#c0c0c0", bd=1, relief="raised")
        self.quit_btn.place(x=400, y=20, width=60)
        
        # Setup label
        self.setup_label = tk.Label(self.root, text="Click the text bubble for a joke!", 
                                   font=("Arial", 10), wraplength=285, 
                                   bg="#fddf87", fg="black", justify="center", bd=1)
        self.setup_label.place(x=125, y=120, width=285, height=60)
        
        # Punchline label
        self.punchline_label = tk.Label(self.root, text="", 
                                       font=("Arial", 10, "italic"), 
                                       wraplength=285, bg="#fddf87", 
                                       fg="red", justify="center", bd=1)
        self.punchline_label.place(x=125, y=200, width=285, height=40)
    
    def tell_joke(self):
        if self.jokes:
            self.current_joke = random.choice(self.jokes)
            if "?" in self.current_joke:
                setup, punchline = self.current_joke.split("?", 1)
                self.setup_label.config(text=setup + "?")
                self.current_punchline = punchline
            else:
                self.setup_label.config(text=self.current_joke)
                self.current_punchline = "No punchline"
            
            self.punchline_label.config(text="")
            self.punch_btn.config(state="normal")
            self.next_btn.config(state="normal")
            self.tell_btn.config(state="disabled")
    
    def show_punchline(self):
        self.punchline_label.config(text=self.current_punchline)
        self.punch_btn.config(state="disabled")
    
    def next_joke(self):
        self.setup_label.config(text="Click the button for another joke!")
        self.punchline_label.config(text="")
        self.punch_btn.config(state="disabled")
        self.next_btn.config(state="disabled")
        self.tell_btn.config(state="normal")

root = tk.Tk()
app = JokeTeller(root)
root.mainloop()