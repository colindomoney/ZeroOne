import fnmatch, os
import ZO
from tkinter import *
from PIL import ImageTk, Image

PIXEL_MULTIPLIER = 10
IMAGE_PATH = '/Users/colind/Documents/Projects/ZeroOne/ZeroOne/Graphics/Images'

def get_images():
    return fnmatch.filter(os.listdir(IMAGE_PATH), '*.png')

# This will open the socket connection
def open_connection():
    print("open_connection")
    root.after(500, process_connection())

# This will process the incoming data from the socket
def process_connection():
    print("process_connection")

# Exit button handler
def exitButtonClick():
    print('exitButtonClick')

# Clear button handler
def clearButtonClick():
    print('clearButtonClick')

# Build the app
root = Tk()
root.title("ZeroOne DisplayEmulator")
# window.geometry('350x200')

canvasX = PIXEL_MULTIPLIER * ZO.zero_one.ZO_X_SIZE
canvasY = PIXEL_MULTIPLIER * ZO.zero_one.ZO_Y_SIZE

# canvasX = ZO.zero_one.ZO_X_SIZE
# canvasY = ZO.zero_one.ZO_Y_SIZE

# Add the top frame for the buttons
frame = Frame(root, bg='white', width=canvasX + 20, height=40)
frame.pack(fill='x')
exitButton = Button(frame, text='Exit', command=exitButtonClick)
exitButton.pack(side='left', padx=10)
clearButton = Button(frame, text='Clear', command=clearButtonClick)
clearButton.pack(side='left')
root.bind(exitButton, exitButtonClick)

# Add the canvas with a black border and a bit of padding
canvas = Canvas(root, width=canvasX, height=canvasY, bg='black')
canvas.pack(pady=(10, 10), padx=(10,10))

try:
    files = get_images()

    if len(files) != 0:
        pilImg = Image.open(os.path.join(IMAGE_PATH, files[5]))

        # Now save the byte array and import it again
        rawData = pilImg.tobytes()
        size = len(rawData)

        # TODO: This resampling thing makes the images all fuzzy. Ideally we want
        # the pixels copied up as they are without interpolation but this is OK
        pilImg = pilImg.resize((canvasX, canvasY), Image.BILINEAR)
        # pilImg.show()

        importPilImage = Image.frombytes('RGBA', (ZO.zero_one.ZO_X_SIZE, ZO.zero_one.ZO_Y_SIZE), rawData, 'raw')
        importPilImage = importPilImage.resize((canvasX, canvasY), Image.BILINEAR)
        # importPilImage.show()

        importRawData = pilImg.tobytes()

        # TODO : Try and understand why we have to add this offset here !!
        # It looks like the canvas is a bit too big for the image
        img = ImageTk.PhotoImage(pilImg)
        canvas.create_image(3, 3, anchor=NW, image=img)

    root.after(500, open_connection())
    root.mainloop()

except KeyboardInterrupt as ex:
    print('Forcing a quit')
    pass