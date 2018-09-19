from PIL import Image

def process_images():
    print("process_images() :", 55)

    im = Image.open('./test.gif')

    print('Done ',  im.info['duration'])

if __name__ == '__main__':
    print('__main__')
    process_images()