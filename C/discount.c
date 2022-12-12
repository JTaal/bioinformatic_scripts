#include <stdio.h>

int get_int(void)
{
    printf("Enter an integer: ");
    return scanf("%d");
}    

float discount(float price, int percentage)
{
    return price * (100 - percentage) / 100;
}



int main(void)
{
    float regular = 56;
    int percent_off = 15;
    float sale = discount(regular, percent_off);
    printf("Sale Price: %.2f\n", sale);
}

