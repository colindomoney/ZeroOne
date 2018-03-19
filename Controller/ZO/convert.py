""" A pretty dumb class to do some graphic file conversion stuff """
import argparse
import csv
import glob

import numpy
import os

from ZO import ZeroOneException, ZO_PIXEL_COUNT


def GetArgs():
    """
    Supports the command-line arguments listed below.
    """

    parser = argparse.ArgumentParser(description='A utility to perform various conversions for the ZeroOne project')
    parser.add_argument('-i', '--input', required=True, action='store', help='Specify the name of the input file')
    parser.add_argument('-o', '--output', required=False, action='store', default='./zero_one.npy',
                        help='Specify the name of the output file')

    # parser.add_argument('-s', '--host', required=True, action='store', help='Remote host to connect to')
    # parser.add_argument('-o', '--port', type=int, default=443, action='store', help='Port to connect on')
    # parser.add_argument('-u', '--user', required=True, action='store', help='User name to use when connecting to host')
    # parser.add_argument('-p', '--password', required=False, action='store',
    #                     help='Password to use when connecting to host')
    # parser.add_argument('-v', '--vmname', required=True, action='append',
    #                     help='Names of the Virtual Machines to power on')
    # parser.add_argument('-c', '--command', required=True, action='store',
    #                     help='Specify on to power on, off to power off')

    args = parser.parse_args()
    return args

def _map_image_to_pixels(self, opImage):
    from . import ZO_Mask

    maskData = ZO_Mask().flat

    # Zip the data
    combinedData = list(zip(list(opImage.getdata()), maskData))

    # Get everything that isn't a zero in the mask
    outputFrame = [x[0] for x in combinedData if x[1] != 0]

    if len(outputFrame) != ZO_PIXEL_COUNT:
        raise ZeroOneException('Pixel count not the expected length after masking')

    # TODO : This can throw an exception if the input format ia wrong
    pixels = [(x[0], x[1], x[2]) for x in outputFrame]

    print("Length: {0}".format(len(pixels)))


def ConvertZeroOneFile(inputFile, outputFile='./zero_one.npy'):
    try:
        data = []

        with open(inputFile) as cvsFile:
            readCSV = csv.reader(cvsFile, delimiter=',')
            for row in readCSV:
                vals = [int(r) for r in row]
                data.append(vals)
    except FileNotFoundError as ex:
        # print('File not found')
        # TODO : Not really sure why we're bothering to catch this exception anyway
        raise

    # Here we have an 'array' as a list of lists so convert it to an array and save it in .npy format
    numpy.save(outputFile, numpy.array(data, dtype=numpy.uint8))

    ar = numpy.array(data)
    print(ar)

def ResizeImageFileToZeroOne(inputFile, outputFile=None):
    from PIL import Image
    from ZO import zero_one

    img = Image.open(inputFile)

    size = (zero_one.ZO_X_SIZE, zero_one.ZO_Y_SIZE)
    img.convert(mode="RGB")
    img.thumbnail(size)

    if outputFile is None:
        outputFile, extension = os.path.splitext(inputFile)
        outputFile += '_zo'
        outputFile += '.png'

    img.save(outputFile, format="PNG")

def DoConversion(input):
    import os

    if os.path.isdir(input):
        for f in os.listdir(input):
            ResizeImageFileToZeroOne(os.path.join(input, f))
    else:
        ResizeImageFileToZeroOne(input)

def main():
    print('convert()')

    args = GetArgs()

    DoConversion(args.input)

if __name__ == '__main__':
    main()
