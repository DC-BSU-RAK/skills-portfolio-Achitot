from tkinter import * 
root = Tk()
root.title('ArithMix')
root.geometry('360x640')
root.config(bg='#234567')
root.resizable(0,0)

Title = Label(root, text="ArithMix",
             font=('Roboto', 25),
             bg='#234567', fg='white')
Title.place(relx=0.5, rely=0.2, anchor=CENTER)

start_button = Button(root, text = "Start", fg="yellow", bg="#001111"
,font=("tahoma",12), command = sum)
start_button.place(relx=0.5, rely=0.5, anchor=CENTER)

root.mainloop()