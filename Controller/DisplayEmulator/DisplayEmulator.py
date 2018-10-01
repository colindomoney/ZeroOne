import ZO

from tkinter import *

window = Tk()
window.title("ZeroOne DisplayEmulator")
# window.geometry('350x200')

ZO.zero_one.ZO_X_SIZE
ZO.zero_one.ZO_Y_SIZE

lbl = Label(window, text="Hello", fg='red')
lbl.grid(column=0, row=0)
# btn = Button(window, text="Click Me", fg='black', bg='black')
btn = Button(window, fg='black', bg='white', text="Click Me")
btn.grid(column=1, row=0)

window.mainloop()
