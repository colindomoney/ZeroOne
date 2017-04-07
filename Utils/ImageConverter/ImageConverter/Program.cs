using System;
using System.Collections.Generic;
using System.ComponentModel.Design;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Runtime.Remoting.Messaging;
using System.Text.RegularExpressions;

namespace ImageConverter
{
    internal class Program
    {
        private const int BytesPerPixel = 3;

        public static void Main(string[] args)
        {
            Console.WriteLine("ImageConverter starting ...");

            string[] allLines = System.IO.File.ReadAllLines("../../../../../Graphics/01/01_38x29_asc.ppm");

            Console.WriteLine("Line count: {0}", allLines.Length);

            // Check the file makes sense
            int colsX, rowsY, maxColorValue;
            bool fileOK = GetFileInfo(ref allLines, out colsX, out rowsY, out maxColorValue);
            Console.WriteLine("File OK : {0}", fileOK);

            int rgbVal = 0;
            int[,] rgbValues = new int[colsX, rowsY];

            for (int i = 0; i < allLines.Length; i++)
            {
                string line = allLines[i];

                int cmpVal = Int32.Parse(line);

                // R
                if (i % BytesPerPixel == 0)
                {
                    rgbVal = cmpVal << 16;
                }

                // G
                if (i % BytesPerPixel == 1)
                {
                    rgbVal |= cmpVal << 8;
                }

                // B
                if (i % BytesPerPixel == 2)
                {
                    int rgbi = i / BytesPerPixel;
                    rgbVal |= cmpVal;
                    //Console.WriteLine("[{0}] = {1:X08}", rgbi, rgbVal);

                    // Now write it to the output array
                    rgbValues[rgbi % colsX, rgbi / colsX] = rgbVal;
                }
            }

            Console.WriteLine("Done!");
        }


        private static bool GetFileInfo(ref string[] allLines, out int colsX, out int rowsY, out int maxColorValue)
        {
            colsX = 0;
            rowsY = 0;

            // First clean up the input data
            allLines = allLines.Where(l => String.IsNullOrEmpty(l) == false).ToArray();

            int firstLine = 1;

            // First check we have at least one line
            if (allLines.Length < 1)
            {
                throw new FileLoadException("File contains no data");
            }

            // Check the file starts with 'P3'
            if (allLines[0].StartsWith("P3") == false)
            {
                throw new FileLoadException("File does not contain PPM identifier");
            }

            // Get the X and Y co-ords
            while (true)
            {
                string line = allLines[firstLine++];
                Regex rgx = new Regex(@"^(\d+)\s(\d+)");
                Match mtc = rgx.Match(line);

                if (mtc.Success)
                {
                    colsX = Int32.Parse(mtc.Groups[1].Value);
                    rowsY = Int32.Parse(mtc.Groups[2].Value);

                    maxColorValue = Int32.Parse(allLines[firstLine++]);

                    // Remember to skip the maximum color value byte
                    allLines = allLines.Skip(firstLine).ToArray();

                    // Now check the size line up correctly
                    if (allLines.Length != (rowsY * colsX * BytesPerPixel))
                    {
                        throw new FileLoadException("File size error (dimensions do not match data size)");
                    }

                    return true;
                }
            }

            return false;
        }
    }
}