using System;
using System.Collections.Generic;

namespace ElfCode
{
    class Program
    {
        static void ElfCode()
        {
            long[] r = new long[] { 0, 0, 0, 0, 0, 0 };  // initial values for registers
            Dictionary<long, int> prev = new Dictionary<long, int>();  // values for r0 for which the sequence breaks
            int iterations = 0;  // keeping track of iterations
            long part1 = 0;  // keeping track of pt 1 solution

            r[5] = r[3] | 65536;
            r[3] = 15028787;  // first few commands in the script
            while (true)
            {
                iterations++;
                r[2] = r[5] & 255;
                r[3] += r[2];
                r[3] &= 16777215;
                r[3] *= 65899;
                r[3] &= 16777215;

                if (256 > r[5])
                {
                    // keeping track
                    if (iterations % 1000 == 0)
                    {
                        // report iterations
                        Console.WriteLine(iterations.ToString() + " iterations so far");
                    }
                    if (part1 == 0)
                    {
                        // solution for part 1
                        part1 = r[3];
                    }
                    try
                    {
                        // try to add value for r0
                        prev.Add(r[3], iterations);
                    }
                    catch (ArgumentException)
                    {
                        // if we have found this value before, we assume the cycle is repeating, thus we can stop
                        long max = part1;  // this is a value for r0 that we know of, we wish to find the value with the most iterations
                        foreach (long p in prev.Keys) {
                            if (prev[p] > prev[max]){
                                max = p;
                            }
                        }
                        // report solutions and stop
                        Console.WriteLine("PART 1: " + part1.ToString());
                        Console.WriteLine("PART 2: " + max.ToString());
                        Console.WriteLine("After " + iterations.ToString() + " iterations");
                        break;
                    }
                    // actual program

                    if (r[3] == r[0])
                    {
                        // breaking condition: this is why we are looking for values of r[0] by looking at r[3] when we arrive at this point
                        break;
                    }
                    r[5] = r[3] | 65536;
                    r[3] = 15028787;
                }
                else
                {
                    r[2] = 0;
                    r[4] = r[2] + 1;
                    r[4] *= 256;

                    r[4] = r[4] > r[5] ? 1 : 0;

                    while (r[4] == 0)
                    {
                        r[2]++;
                        r[4] = r[2] + 1;
                        r[4] *= 256;

                        r[4] = r[4] > r[5] ? 1 : 0;
                    }

                    r[5] = r[2];

                }
            }  
        }

        static void Main(string[] args)
        {
            ElfCode();
            Console.ReadKey();
        }
    }
}
