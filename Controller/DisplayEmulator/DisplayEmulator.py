import fnmatch, os, socket
import pickle

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


class EmulatorCommand():
    def __init__(self, command='None', data=None):
        self.Command = command
        self.Data = data


class DisplayEmulatorApplication(Thread):
    def __init__(self, root):
        self._port = 6999
        self._host = socket.gethostname()
        self._client = None
        self._socket = None
        self._closing = False
        self._root = root

        self._canvasX = PIXEL_MULTIPLIER * ZO.zero_one.ZO_X_SIZE
        self._canvasY = PIXEL_MULTIPLIER * ZO.zero_one.ZO_Y_SIZE

        Thread.__init__(self)

        # Add the top frame for the buttons
        button_frame = Frame(root, bg='white', width=self._canvasX + 10, height=40)
        button_frame.pack(fill='x')
        exit_button = Button(button_frame, text='Exit', command=exitButtonClick)
        exit_button.pack(side='left', padx=10)
        clear_button = Button(button_frame, text='Clear', command=clearButtonClick)
        clear_button.pack(side='left')

        # Add the canvas with a black border and a bit of padding
        canvas = Canvas(root, width=self._canvasX, height=self._canvasY, bg='black')
        canvas.pack(pady=(10, 10), padx=(10, 10))

        # Add the top frame for the buttons
        self._status_frame = Frame(root, bg='red', width=self._canvasX + 10, height=20)
        self._status_frame.pack(fill='x')

    def set_connected_state(self, is_connected = False):
        if is_connected == True:
            self._status_frame.config(bg='green')
        else:
            self._status_frame.config(bg='red')

    def close(self):
        # This is called when the main loop wants to shut down
        print('close()')
        self._closing = True
        self._server.close()

    def run(self):
        # This is the main listening thread
        print('run()')

        # Open the socket
        self._server = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

        # self._server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        # Bind and listen
        self._server.bind((self._host, self._port))
        self._server.listen(5)

        # TODO : I think we'll have to have this a bit more sophisticatted than this
        # i.e. we'll need to loop back to accept a new connection

        # Loop until the app is shutdown
        while self._closing == False:

            # Await a connection if the socket is closed or None
            if self._client == None or self._client._closed == True:
                try:
                    self._client, info = self._server.accept()
                    print('CONNECTED !')
                    self.set_connected_state(True)
                except Exception as ex:
                    print('>> ', ex)

            # Now try get some data
            try:
                data_string = self._client.recv(8192)

                if not data_string:
                    # If we hit this point the socket is broken and we can close it and await a new connection
                    print('... incomplete ... closing ...')
                    self._client.close()
                    self.set_connected_state(False)
                else:
                    print('len = ', len(data_string))
                    try:
                        # This is prone to shitting itself so guard it with kid gloves
                        emulator_command = pickle.loads(data_string)
                        print(emulator_command.Command)
                    except:
                        pass
            except Exception as ex:
                print("\n>>> EXCEPTION : {} <<<\n".format(ex))

        print('exit run()')

        # Quit TKinter
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


try:
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

except KeyboardInterrupt as ex:
    print('Forcing a quit')
    pass

finally:
    print('exiting ...')
