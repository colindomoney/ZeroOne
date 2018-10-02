import fnmatch, os, socket
import ZO
from threading import *
from tkinter import *
from PIL import ImageTk, Image

PIXEL_MULTIPLIER = 10
IMAGE_PATH = '/Users/colind/Documents/Projects/ZeroOne/ZeroOne/Graphics/Images'

def get_images():
    return fnmatch.filter(os.listdir(IMAGE_PATH), '*.png')

# Exit button handler
def exitButtonClick():
    print('exitButtonClick')

# Clear button handler
def clearButtonClick():
    print('clearButtonClick')

class DisplayEmulatorApplication(Thread):
    def __init__(self, root):
        self._port = 6999
        self._host = socket.gethostname()
        self._client = None
        self._socket = None
        self._root = root

        self._canvasX = PIXEL_MULTIPLIER * ZO.zero_one.ZO_X_SIZE
        self._canvasY = PIXEL_MULTIPLIER * ZO.zero_one.ZO_Y_SIZE

        Thread.__init__(self)

        # Add the top frame for the buttons
        frame = Frame(root, bg='white', width=self._canvasX + 20, height=40)
        frame.pack(fill='x')
        exitButton = Button(frame, text='Exit', command=exitButtonClick)
        exitButton.pack(side='left', padx=10)
        clearButton = Button(frame, text='Clear', command=clearButtonClick)
        clearButton.pack(side='left')

        # Add the canvas with a black border and a bit of padding
        canvas = Canvas(root, width=self._canvasX, height=self._canvasY, bg='black')
        canvas.pack(pady=(10, 10), padx=(10,10))

    def close(self):
        print('close()')
        self._server.close()

    def run(self):
        print('run()')

        self._server = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

        self._server.bind((self._host, self._port))
        self._server.listen(5)

        try:
            self._client, info = self._server.accept()

            print('CONNECTED !')

        except Exception as ex:
            print('>> ', ex)

        print('exit run()')

        self._root.destroy()

        # try:
        #     files = get_images()
        #
        #     if len(files) != 0:
        #         pilImg = Image.open(os.path.join(IMAGE_PATH, files[5]))
        #
        #         # Now save the byte array and import it again
        #         rawData = pilImg.tobytes()
        #         size = len(rawData)
        #
        #         # TODO: This resampling thing makes the images all fuzzy. Ideally we want
        #         # the pixels copied up as they are without interpolation but this is OK
        #         pilImg = pilImg.resize((canvasX, canvasY), Image.BILINEAR)
        #
        #         importPilImage = Image.frombytes('RGBA', (ZO.zero_one.ZO_X_SIZE, ZO.zero_one.ZO_Y_SIZE), rawData, 'raw')
        #         importPilImage = importPilImage.resize((canvasX, canvasY), Image.BILINEAR)
        #
        #         importRawData = pilImg.tobytes()
        #
        #         # TODO : Try and understand why we have to add this offset here !!
        #         # It looks like the canvas is a bit too big for the image
        #         img = ImageTk.PhotoImage(pilImg)
        #         canvas.create_image(3, 3, anchor=NW, image=img)        #
        #
        # except KeyboardInterrupt as ex:
        #     print('Forcing a quit')
        #     pass
        #

# Handle the window close event
def close_window():
    global app
    print('CLOSE()')
    app.close()

# Create the root Tk object
root = Tk()
root.title("ZeroOne DisplayEmulator")

# Hook the close window event
root.protocol("WM_DELETE_WINDOW", close_window)

# Now build the app and start the thread in daemon mode
app = DisplayEmulatorApplication(root)
app.daemon = True
app.start()

# Now run the main TKinter lool
print('before mainloop()')
root.mainloop()
print('after mainloop()')

# TODO : The Ctrl-C is somehow lost now, add a handler back here somewhere

print('exiting ...')

