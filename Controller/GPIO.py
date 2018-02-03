import RPi.GPIO as GPIO
import time, threading

pin2state = 0
pin3state = 0

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT) # Green LED
    GPIO.setup(27, GPIO.OUT) # Red LED
    GPIO.setup(2, GPIO.IN)  # Black button
    GPIO.setup(3, GPIO.IN)  # Red button

    def pin2_callback(self):
        time.sleep(.075)

        global pin2state
        if (GPIO.input(2) != 0 and pin2state != 0):
            print("<U>")
            pin2state = 0
        elif (GPIO.input(2) == 0 and pin2state == 0):
            print("<D>")
            pin2state = 1

    GPIO.add_event_detect(2, GPIO.BOTH, callback = pin2_callback)

ledState = 0

def toggle_led():
    print(". ")

    global ledState
    if (ledState):
        ledState = 0
        GPIO.output(17, 0)
    else:
        ledState = 1
        GPIO.output(17, 1)

    global tickTimer
    tickTimer = threading.Timer(0.2, toggle_led)
    tickTimer.start()

if __name__ == "__main__":
    try:
        print('Running main')

        print("Setup GPIO")
        setup_gpio()

        toggle_led()

        for i in range(1, 200):

            # if (GPIO.input(3) != 0):
            #     GPIO.output(27, 0)
            # else:
            #     GPIO.output(27, 1)

            # GPIO.output(17, 0)
            # GPIO.output(27, 0)
            time.sleep(0.2)
            # GPIO.output(17, 1)
            # GPIO.output(27, 1)
            # time.sleep(0.2)

    except KeyboardInterrupt:
        print("Aborted")
        pass

    finally:
        print("Exiting")
        GPIO.cleanup()
        tickTimer.cancel()
