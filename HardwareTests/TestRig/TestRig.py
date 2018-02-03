import opc, time

numLEDs = 591
client = opc.Client('localhost:7890')

black = [ (0,0,0) ] * numLEDs
white = [ (0,0,255) ] * numLEDs

if client.can_connect():
    print("Connected to server")
else:
    print("FAILED to connect to server")
    exit(1)

while True:
    print('. ')
    client.put_pixels(white)
    time.sleep(0.15)
    client.put_pixels(black)
    time.sleep(0.15)