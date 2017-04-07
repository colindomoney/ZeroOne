using System;
using System.Collections.Generic;

namespace ImageConverter
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("ImageConverter starting ...");

            string[] allLines = System.IO.File.ReadAllLines("../../../../../Graphics/01/01_38x29_asc.ppm");

            Console.WriteLine("Line count: {0}", allLines.Length);

            Console.WriteLine("Line 1 = '{0}'", allLines[0]);

            Console.WriteLine("Done!");
        }
    }
}