using System;
using System.Collections.Generic;
using System.ComponentModel.Design;
using System.IO;
using System.Runtime.Remoting.Messaging;

namespace ImageConverter
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("ImageConverter starting ...");

            string[] allLines = System.IO.File.ReadAllLines("../../../../../Graphics/01/01_38x29_asc.ppm");

            Console.WriteLine("Line count: {0}", allLines.Length);

            // Check the file makes sense
            int colsX, rowsY;
            bool fileOK = GetFileInfo(allLines, out colsX, out rowsY);

            Console.WriteLine("File OK : {0}", fileOK);

            Console.WriteLine("Done!");
        }


        private static bool GetFileInfo(string[] allLines, out int colsX, out int rowsY)
        {
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

            colsX = 0;
            rowsY = 0;

            return false;
        }
    }
}