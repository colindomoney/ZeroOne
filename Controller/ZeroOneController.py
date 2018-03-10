import opc, time
import ZO

numLEDs = 591
client = opc.Client('localhost:7890')

black = [ (0, 0, 0) ] * numLEDs
white = [ (0, 255, 0) ] * numLEDs

if client.can_connect():
    print("Connected to server")
else:
    print("FAILED to connect to server")
    exit(1)

try:

    while True:
        z = ZO.ZeroOne()

        print('. ')
        client.put_pixels(white)
        time.sleep(0.25)
        client.put_pixels(black)
        time.sleep(0.25)

except KeyboardInterrupt:
    print('Exiting ...')
    client.put_pixels(black)

