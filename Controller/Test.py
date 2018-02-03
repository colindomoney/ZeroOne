import time, threading

# def toggle_led():
#     print(". ")
#     global timer
#     timer = threading.Timer(1, toggle_led)
#     timer.start()


def main():
    # toggle_led()

    try:
        print('Running main')
        cnt = 0

        while True:
            time.sleep(0.2)
            print('x')
            time.sleep(0.2)

            cnt = cnt + 1
            # if (cnt > 4):
            #     timer.cancel()

    except KeyboardInterrupt:
        print("Exiting")
        # timer.cancel()

if __name__ == "__main__":
    main()