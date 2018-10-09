"""
    A helper file to do useful things with images
"""
import colorsys

import numpy, os, pprint
from . import zero_one, ZO_PIXEL_COUNT, ZeroOneException
from PIL import Image, ImageColor, ImageDraw

# Now pay attention - the location of the NPY file is relative to where the ZO folder resides
# Use this one trick to find that path and make the reference relative to that
this_directory = os.path.dirname(os.path.realpath(__file__))
ZERO_ONE_MASK_FILE = os.path.join(this_directory, './zero_one.npy')

# TODO : Uuuuugghhhh look at all this hardcoded stuff !
TEST_PATTERN_FILE = '/Users/colind/Documents/Projects/ZeroOne/ZeroOne/Graphics/Images/RGBW.png'
UNION_JACK_FILE = '/Users/colind/Documents/Projects/ZeroOne/ZeroOne/Graphics/Images/UnionJack.png'
SOUTH_AFRICA_FILE = '/Users/colind/Documents/Projects/ZeroOne/ZeroOne/Graphics/Images/SouthAfrica.png'
EUROPEAN_UNION_FILE = '/Users/colind/Documents/Projects/ZeroOne/ZeroOne/Graphics/Images/EU.png'
RED_TEST_PATTERN_FILE = '/Users/colind/Documents/Projects/ZeroOne/ZeroOne/Graphics/Images/Red_Left.png'
GREEN_TEST_PATTERN_FILE = '/Users/colind/Documents/Projects/ZeroOne/ZeroOne/Graphics/Images/Green_Centre.png'
BLUE_TEST_PATTERN_FILE = '/Users/colind/Documents/Projects/ZeroOne/ZeroOne/Graphics/Images/Blue_Right.png'

class ZO_Mask:
    # This tag values in the CSV pattern file
    class ZoneTags:
        NoTag = 0
        ZeroOutlineTag = 11
        ZeroInteriorTag = 1
        OneOutlineTag = 22
        OneInteriorTag = 2

    '''
    A simple class to manage the '01' pixel mask.
    '''
    def __init__(self):
        self._load_mask_data()

    def _load_mask_data(self):
        ''' Loads the pixel data from the file '''
        # print('cwd = ', os.getcwd())
        # print('path = ', )
        self._data = list(numpy.load(ZERO_ONE_MASK_FILE).flatten())

        if len(self._data) != zero_one.ZO_X_SIZE * zero_one.ZO_Y_SIZE:
            raise zero_one.ZeroOneException('Mask data not the correct size')

    #  Returns it as a flattened list
    @property
    def flat(self):
        return list(numpy.load(ZERO_ONE_MASK_FILE).flatten())

    # Returns it as a 2D array
    @property
    def array(self):
        return numpy.load(ZERO_ONE_MASK_FILE).tolist()

class ZO_Image:
    class Patterns:
        ZeroOutline = 0x01
        ZeroInterior = 0x02
        ZeroBoth = 0x03
        OneOutline = 0x10
        OneInterior = 0x20
        OneBoth = 0x30
        BothInterior = ZeroInterior | OneInterior
        BothOutline = ZeroOutline | OneOutline
        BothBoth = BothInterior | BothOutline

    def __init__(self):
        super().__init__()
        self._show_pattern = False

        self._image = Image.new('RGBA', (zero_one.ZO_X_SIZE, zero_one.ZO_Y_SIZE))
        self._pattern = None

        self._black_image = Image.new('RGBA', (zero_one.ZO_X_SIZE, zero_one.ZO_Y_SIZE),
                                      color=(0, 0, 0, 0))

        self._mask = Image.new('L', (zero_one.ZO_X_SIZE, zero_one.ZO_Y_SIZE),
                                  color=0xff)

        img_draw = ImageDraw.Draw(self._mask)

        img_draw.rectangle([0,0,10,10], 0x20, 0x20)



        # pprint.pprint(self._mask.tobytes())
        # print(len(self._mask.tobytes()))

        print('Done')

    def __str__(self):
        return "ZO_Image() -> Filename: {0}, Format: {1}, Mode: {2}, Size: {3}".format(
            self.image.filename, self.image.format, self.image.mode,  self.image.size)

    # This is the main access method to accees the image - don't use the internal _image value
    # since this won't show the mask value
    @property
    def image(self):
        img = self._image

        if self._show_pattern == True:
            img = Image.alpha_composite(self._image, self._pattern)

        return img

    # TODO : What's the point of this method ?
    @property
    def raw_data(self):
        return self.image.getdata()

    # Get the 591 raw pixel data for the 01 shape (in RGB tuples)
    @property
    def zero_one_raw_data(self):
        return self._map_image_to_pixels()

    def test_image(self):
        # res = Image.blend(self._image, self._black_image, alpha=0)

        newImg = Image.new('RGB', (zero_one.ZO_X_SIZE, zero_one.ZO_Y_SIZE),
                                       color=(0, 0, 0))

        res = self.image
        res.putalpha(self._mask)


        # TODO : The plan with this piece of code was to use the intensity (Y) value
        # from the YIG co-ordinates to adjust the brightness but it didn't seem to work
        # pixels = self.image.load()
        # mask = self._mask.load()

        # pixels = res.load()
        #
        # for i in range(res.size[0]):  # for every col:
        #     for j in range(res.size[1]):  # For every row
        #         pixel = pixels[i, j]
        #         yiq = colorsys.rgb_to_yiq(float(pixel[0])/0xff, float(pixel[1])/0xff, float(pixel[2])/0xff)
        #
        #         rgb = colorsys.yiq_to_rgb(0.1, yiq[1], yiq[2])
        #         pixels[i, j] = (int(rgb[0]*0xff), int(rgb[1]*0xff), int(rgb[2]*0xff))


        # TODO : this was the actual bit of magic that made it work
        # Use the res image (which is a copy of the original), then paste in
        # the mask using putalpha(), then do the fact split thing to remove the alpha
        # into a new image and then show that. Voila.
        newImg.paste(res, mask=res.split()[3])
        newImg.show()

        # res.show()
        return newImg

    # This is the function that converts the full image to a 01 shape
    def _map_image_to_pixels(self):
        from . import ZO_Mask

        maskData = ZO_Mask().flat

        # Zip the data
        combinedData = list(zip(list(self.image.getdata()), maskData))

        # Get everything that isn't a zero in the mask
        outputFrame = [x[0] for x in combinedData if x[1] != 0]

        if len(outputFrame) != ZO_PIXEL_COUNT:
            raise ZeroOneException('Pixel count not the expected length after masking')

        # TODO : This can throw an exception if the input format ia wrong
        pixels = [(x[0], x[1], x[2]) for x in outputFrame]

        return pixels

    # Not the most widely used method but maybe useful
    # Take the 01 raw data (as a 591 long set of tuple RGB values) and covert to a PIL image
    def get_image_from_zero_one_data(self, zero_one_raw_data=None):
        # If we don't get an input then point to ourselves
        if zero_one_raw_data == None:
            zero_one_raw_data = self.zero_one_raw_data

        if len(zero_one_raw_data) != ZO_PIXEL_COUNT:
            raise ZeroOneException('ZeroOne raw data is not of the expected length')

        bg = ImageColor.getcolor('black', 'RGBA')
        bg = (bg[0], bg[1], bg[2], 255)

        mask = ZO_Mask().array

        # Build up a 28 x 38 list of lists
        idx = 0
        op = []
        for r in mask:
            row = []
            for c in r:
                if c != 0:
                    # Meehhh
                    r, g, b = zero_one_raw_data[idx]
                    row.append((r, g, b, 255))
                    idx = idx+1
                else:
                    row.append(bg)

            op.append(row)

        op = numpy.asarray(op, dtype=numpy.dtype('uint8,uint8,uint8,uint8'))
        image = Image.fromarray(op, 'RGBA')

        return image

    @property
    def show_pattern(self):
        return self._show_pattern

    @show_pattern.setter
    def show_pattern(self, value):
        self._show_pattern = value

    def show(self):
        self._pattern.show()

    def set_to_color(self, rgb='white', alpha=255):
        fg = ImageColor.getcolor(rgb, 'RGBA')

        # Build an array and pull it in as RGBA
        arr = numpy.array([[fg for x in  range(zero_one.ZO_X_SIZE)] for y in range(zero_one.ZO_Y_SIZE)], dtype=numpy.dtype('uint8,uint8,uint8,uint8'))
        self._image = Image.fromarray(arr, 'RGBA')

    def load_from_file(self, filename=None):
        img = Image.open(filename)
        backing_img = Image.new('RGBA', (zero_one.ZO_X_SIZE, zero_one.ZO_Y_SIZE))

        size = (zero_one.ZO_X_SIZE, zero_one.ZO_Y_SIZE)
        img.convert(mode="RGBA")
        res = img.thumbnail(size)

        if img.width != zero_one.ZO_X_SIZE or img.height != zero_one.ZO_Y_SIZE:
            x_pos = y_pos = 0
            if img.width != zero_one.ZO_X_SIZE:
                x_pos = int((zero_one.ZO_X_SIZE - img.width)/2)
            if img.height != zero_one.ZO_Y_SIZE:
                y_pos = int((zero_one.ZO_Y_SIZE - img.height)/2)

            print('x, y', x_pos, y_pos)
            backing_img.paste(img, (x_pos, y_pos))
            img = backing_img
            # img.show()

        if img.width != zero_one.ZO_X_SIZE or img.height != zero_one.ZO_Y_SIZE:
            raise zero_one.ZeroOneException('Invalid image size, not loaded')

        self._image = img

    def clear_pattern(self):
        # Create a new blank/black image in RGBA with (width, height)
        self._pattern = Image.new('RGBA', (zero_one.ZO_X_SIZE, zero_one.ZO_Y_SIZE))

    def set_pattern(self, pattern=None, rgb='red', alpha=255):
        mask = ZO_Mask().array

        if self._pattern is None:
            self.clear_pattern()

        bg = ImageColor.getcolor('white', 'RGBA')
        bg = (bg[0], bg[1], bg[2], 0)  # Set a transparent background
        fg = ImageColor.getcolor(rgb, 'RGBA')
        fg = (fg[0], fg[1], fg[2], alpha)  # Set a solid foreground

        op = []
        for r in mask:
            row = []
            for c in r:
                if c == ZO_Mask.ZoneTags.NoTag:
                    row.append(bg)
                elif c == ZO_Mask.ZoneTags.OneInteriorTag:
                    row.append(fg if pattern & ZO_Image.Patterns.OneInterior else bg)
                elif c == ZO_Mask.ZoneTags.OneOutlineTag:
                    row.append(fg if pattern & ZO_Image.Patterns.OneOutline else bg)
                elif c == ZO_Mask.ZoneTags.ZeroOutlineTag:
                    row.append(fg if pattern & ZO_Image.Patterns.ZeroOutline else bg)
                elif c == ZO_Mask.ZoneTags.ZeroInteriorTag:
                    row.append(fg if pattern & ZO_Image.Patterns.ZeroInterior else bg)

            op.append(row)

        # Some clever fannying around to make sure we keep the tuple data correctly
        op = numpy.asarray(op, dtype=numpy.dtype('uint8,uint8,uint8,uint8'))
        wcImg = Image.fromarray(op, 'RGBA')

        # Now paste the temporary image over the pattern
        self._pattern =  Image.alpha_composite(self._pattern, wcImg)
