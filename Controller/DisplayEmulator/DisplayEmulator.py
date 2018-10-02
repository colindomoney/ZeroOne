import ZO
from tkinter import *

# Create a task to actually do the image loading
def open_connection():
    print("open_connection")
    root.after(500, open_connection)

def process_connection():
    print("process_connection")

root = Tk()
root.title("ZeroOne DisplayEmulator")
# window.geometry('350x200')

# ZO.zero_one.ZO_X_SIZE
# ZO.zero_one.ZO_Y_SIZE

lbl = Label(root, text="Hello", fg='red')
lbl.grid(column=0, row=0)
# btn = Button(window, text="Click Me", fg='black', bg='black')
btn = Button(root, fg='black', bg='white', text="Click Me")
btn.grid(column=1, row=0)

root.after(500, open_connection())
root.mainloop()

