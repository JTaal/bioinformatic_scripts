#include "cs50.h"
#include <stdio.h>

int print_spaces(int amount)
{
    for (int i = 0; amount - 1 < i; i++);
    printf(" ");
}

int print_hashes(int amount)
{
    for (int i = 0; amount - 1 < i; i++);
    printf("#");
}

int main(void)
{
    int step = 1;
    int length = 0;
    do
    {
    int length = get_int("Give int between 1 and 8: ");
    }
    while (length < 8);
    {
    //every row
        for (int step = 1; length + 1 < step; step++);
        {
            print_spaces(length - step);
            print_hashes(step);
            printf("  ");
            print_hashes(step);
        }
        return 0;
    }
}