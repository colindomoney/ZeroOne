import fnmatch, os, socket
import pickle, timer_cm, dill

import ZO
from threading import *
from tkinter import *
from PIL import ImageTk, Image

PIXEL_MULTIPLIER = 10
IMAGE_PATH = '/Users/colind/Documents/Projects/ZeroOne/ZeroOne/Graphics/Images'


def get_images():
    return fnmatch.filter(os.listdir(IMAGE_PATH), '*.png')


class DisplayEmulatorApplication(Thread):
    POLL_INTERVAL = 20

    def __init__(self, root):
        self._port = 6999
        self._host = socket.gethostname()
        self._client = None
        self._socket = None
        self._canvas = None
        self._closing = False
        self._root = root
        self._render_image = None

        self._canvasX = PIXEL_MULTIPLIER * ZO.zero_one.ZO_X_SIZE
        self._canvasY = PIXEL_MULTIPLIER * ZO.zero_one.ZO_Y_SIZE

        Thread.__init__(self)

        # Add the top frame for the buttons
        button_frame = Frame(root, bg='white', width=self._canvasX + 10, height=40)
        button_frame.pack(fill='x')
        exit_button = Button(button_frame, text='Exit', command=self._exit_button_click)
        exit_button.pack(side='left', padx=10)
        clear_button = Button(button_frame, text='Clear', command=self._clear_button_click)
        clear_button.pack(side='left')

        # Add the canvas with a black border and a bit of padding
        self._canvas = Canvas(root, width=self._canvasX, height=self._canvasY, bg='black')
        self._canvas.pack(pady=(10, 10), padx=(10, 10))

        # Add the top frame for the buttons
        self._status_frame = Frame(root, bg='red', width=self._canvasX + 10, height=20)
        self._status_frame.pack(fill='x')

        self._root.after(self.POLL_INTERVAL, self._process_messages)

    # Exit button handler
    def _exit_button_click(self):
        print('exit_button_click()')
        self._root.destroy()

    # Clear button handler
    def _clear_button_click(self):
        print('clear_button_click()')
        self._canvas.delete('all')
        self._canvas.update_idletasks()

    def _process_messages(self):
        if self._render_image != None:
            pil_img = self._render_image.resize((self._canvasX, self._canvasY), Image.BILINEAR)
            self._img = ImageTk.PhotoImage(pil_img)
            self._canvas.create_image(3, 3, anchor=NW, image=self._img)
            self._canvas.update_idletasks()
            self._render_image = None

        self._root.after(self.POLL_INTERVAL, self._process_messages)

    def set_connected_state(self, is_connected = False):
        if is_connected == True:
            self._status_frame.config(bg='green')
        else:
            self._status_frame.config(bg='red')

    def close(self):
        # This is called when the main loop wants to shut down
        print('close()')
        self._closing = True

        # Kill the mofo - not sure if we should be using the server or the client ...
        if self._client != None:
            # TODO : this is still flakey
            # self._client.shutdown(socket.SHUT_WR)
            self._client.close()

        self._server.close()
        # print('done close()')

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

        # Loop until the app is shutdown
        while self._closing == False:

            # Await a connection if the socket is closed or None
            if self._client == None or self._client._closed == True:
                try:
                    print('accept()')
                    self._client, info = self._server.accept()
                    print('CONNECTED !')
                    self.set_connected_state(True)
                except Exception as ex:
                    print("\n>>> EXCEPTION : {} <<<\n".format(ex))

            # Now try get some data
            try:
                # print('recv()')
                data_string = self._client.recv(8192)
                # print('after recv()')

                if not data_string:
                    # If we hit this point the socket is broken and we can close it and await a new connection
                    print('... incomplete ... closing ...')
                    self._client.close()
                    self.set_connected_state(False)
                else:
                    # print('len = ', len(data_string))
                    # print(data_string)
                    try:
                        # This is prone to shitting itself so guard it with kid gloves
                        emulator_command = dill.loads(data_string)
                        print(emulator_command.command)

                        self._handle_command(emulator_command)

                    except Exception as ex:
                        print("\n>>> EXCEPTION : {} <<<\n".format(ex))
            except Exception as ex:
                print("\n>>> EXCEPTION : {} <<<\n".format(ex))

        print('exit run()')

        # Quit TKinter
        self._root.destroy()

    def _handle_command(self, emulator_command):
        print('_handle_command', emulator_command.command)

        if emulator_command.command == 'DisplayAll':
            self._render_image = Image.frombytes('RGB', (ZO.zero_one.ZO_X_SIZE, ZO.zero_one.ZO_Y_SIZE), emulator_command.data,
                                      'raw')

        elif emulator_command.command == 'DisplayZeroOne':
            zo_image = ZO.ZO_Image()
            self._render_image = zo_image.get_image_from_zero_one_data(emulator_command.data)

        elif emulator_command.command == 'ClearDisplay':
            self._canvas.delete('all')
            self._canvas.update_idletasks()

        else:
            print('Unknown command')


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
    # print('before mainloop()')
    root.mainloop()
    # print('after mainloop()')

except KeyboardInterrupt as ex:
    print('Forcing a quit')
    pass

finally:
    print('Done!')
