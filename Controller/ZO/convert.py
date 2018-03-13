""" A pretty dumb class to do some graphic file conversion stuff """
import argparse
import csv
import numpy


def GetArgs():
    """
    Supports the command-line arguments listed below.
    """

    parser = argparse.ArgumentParser(description='A utility to perform various conversions for the ZeroOne project')
    parser.add_argument('-i', '--input', required=True, action='store', help='Specify the name of the input file' )
    parser.add_argument('-o', '--output', required=False, action='store', default='./zero_one.npy', help='Specify the name of the output file' )



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

def ConvertZeroOneFile(inputFile, outputFile ='./zero_one.npy'):
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

def main():
    print('convert()')

    args = GetArgs()

    ConvertZeroOneFile(args.input, args.output)

if __name__ == '__main__':
    main()