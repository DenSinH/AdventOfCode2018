using System;

namespace ElfCode
{
    class Program
    {
        static void ElfCode()
        {
            ulong[] r = new ulong[] { 0, 1, 1, 10551348, 1, 1 };

            while (r[5] <= r[3])
            {

                if (r[3] == r[2] * r[5])
                {
                    r[0] += r[5];
                }
                r[2] += 1;

                if (r[2] > r[3])
                {
                    r[5] += 1;
                    r[2] = 1;
                }
            }

            Console.WriteLine(string.Join(",", r));
        }

        static void BetterCode()
        {
            // Got problems from overflowing, so needed to use ulongs to store the values
            ulong[] r = new ulong[] { 0, 1, 1, 10551348, 1, 1 };
            uint ticker = 0;

            while (r[5] <= r[3])
            {

                // Keeping track
                if (ticker == r[3])
                {
                    Console.WriteLine(string.Join(",", r));
                    ticker = 0;
                }
                else
                {
                    ticker += 1;
                }

                if (r[3] == r[2] * r[5])
                {
                    r[0] += r[5];
                }
                // code i inserted to speed it up myself
                // we will never encounter r[2]*r[5] == r[3] once it has been reached for this r[5], as r[2] strictly increases
                else if (r[3] <= r[2] * r[5])
                {
                    r[5] += 1;
                    r[2] = 1;
                    continue;
                }
                // code up to here is by myself
                r[2] += 1;

                if (r[2] > r[3])
                {
                    r[5] += 1;
                    r[2] = 1;
                }
            }

            Console.WriteLine(string.Join(",", r));
        }

        static void Main()
        {
            BetterCode();
            Console.ReadKey();

        }
        }
    }
