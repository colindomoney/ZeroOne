import getopt, json
import time, logging, os, sys
import ZO
import opc


def setup_logging():
    print("setup_logging")

    logging.basicConfig(
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.FileHandler("./ZeroOneController.log"),
            logging.StreamHandler(sys.stdout)
        ])

    global log
    log = logging.getLogger('ZeroOneController')
    log.setLevel(logging.INFO)


def destroy_logging():
    print("destroy_logging")

# numLEDs = 591
# client = opc.Client('localhost:7890')
#
# black = [ (0, 0, 0) ] * numLEDs
# white = [ (0, 255, 0) ] * numLEDs
#
# if client.can_connect():
#     print("Connected to server")
# else:
#     print("FAILED to connect to server")
#     exit(1)
#
# try:
#
#     while True:
#         z = ZO.ZeroOne()
#
#         print('. ')
#         client.put_pixels(white)
#         time.sleep(0.25)
#         client.put_pixels(black)
#         time.sleep(0.25)
#
# except KeyboardInterrupt:
#     print('Exiting ...')
#     client.put_pixels(black)

def parse_config():
    with open('config.json', 'r') as f:
        config = json.load(f)

    secret_key = config['DEFAULT']['SECRET_KEY']  # 'secret-key-of-myapp'
    ci_hook_url = config['CI']['HOOK_URL']  # 'web-hooking-url-from-ci-service'

# if __name__ == '__main__'
def main(argv):
    print('ZeroOneController running ...')

    setup_logging()

    config_file = './config.ini'
    try:
        opts, args = getopt.getopt(argv, "hc:", ["config="])
    except getopt.GetoptError:
        print('ZeroOneController.py --config <configfile>')
        raise ZO.ZeroOneException()

    for opt, arg in opts:
        if opt in ('-c', '--config'):
            config_file = arg

    # Test the config file exists
    print('Using config from', config_file)
    if os.path.exists(config_file) == False:
        raise ZO.ZeroOneException("Config file {0} does not exist".format(config_file))

    try:
        # while True:
            time.sleep(0.1)
            # print('.')
    except KeyboardInterrupt:
        print('Exiting ...')
    except ZO.ZeroOneException as ex:
        print("\n>>> EXCEPTION : {} <<<\n".format(ex.message))
        log.error(ex.message, exc_info=True)

    finally:
        destroy_logging()
        print('Done!')

if __name__ == '__main__':
    main(sys.argv[1:])