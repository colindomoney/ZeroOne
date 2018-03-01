# from tkinter import *

from PIL import Image

arr1 = ([[12.3, 2.3, 5.2],
            [22.3, 23.2, 86.],
            [-2, .3, 33]])

# root = Tk()
# root.geometry('400x400')
# canvas = Canvas(root, width = 399, height = 399)
# canvas.pack()

image = Image.open("./Test.png")

data = list(image.getdata());

print(data)

print(arr1)

print(arr1[0][0])

# image.show()

# image = ImageTk.PhotoImage(pilImage)
# imagesprite = canvas.create_image(200, 200, image=image)
# root.mainloop()
