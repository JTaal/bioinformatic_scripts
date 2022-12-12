#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//odd_multiplication(string str_number)
//{
//    int i = 0;
//    int int_answer = 0;
//    while (i < strlen(str_number))
//    {
//        string character = str_number[i];
//        int number = character;
//        int_answer += (((int)str_number[i])*2);
//        i+=2;
//    }
//    return int_answer;
//}


//char * intToString(int number, int length)
//{
//    char * output = malloc(length);
//    sprintf(output, "%i", number);
//    return output;
//    free(output);
//}

int intLength(long number)
{
    int i = 0;
    while(number > 0)
    {
        number /= 10;
        i++;
    }
    return i;
}

int main(void)
{
    long creditcard = get_long("Give creditcard number: ");
    int int_length = intLength(creditcard);

    if(int_length < 13|| int_length > 16)
    {
        printf("1 INVALID\n");
        return 0;
    }

    // int number = (int)creditcard;
    int digits[int_length];

    // for(int i = int_length; i > 0; i--)
    // {
    //     digits[i] = number % 10;
    //     number = number / 10;
    // }


    //create a digit array from long
    for(int i = int_length - 1; i >= 0; i--)
    {
        digits[i] = creditcard % 10;
        creditcard /= 10;
    }

    int first_numbers = digits[0]*10 + digits[1];
    int first_number = digits[0];

    // printf("%i", first_numbers);


    //char * str_creditcard = malloc(int_length);
    //str_creditcard = intToString(creditcard, int_length);
    //int string_length = strlen(str_creditcard);


    //printf("%lu", strlen(str_creditcard));

    //round(creditcard, 2)


    //if(str_answer[strlen(str_answer)+1] != 0)
    //{
    //    printf("INVALID\n");
    //}
    int validation = 0;
    int validation_odd = 0;

    if(int_length%2 != 0)
    {
        validation_odd += digits[0];
    }


    //iterate over the array and create validation nr
    for(int i = int_length - 1; i > 0; i-=2)
    {
        validation_odd += digits[i];
        if((digits[i-1] * 2) > 9)
        {
            int num = digits[i-1]*2;
            int uno = num%10;
            int dos = (num-uno)/10;
            validation += uno + dos;
        }
        else
        {
            validation += digits[i-1] * 2;
        }
    }

    validation = validation + validation_odd;

    //printf("%i", int_length);
    // printf("%i|%i|%i",validation, validation_odd, validation + validation_odd);

    if(validation % 10 != 0)
    {
        printf("INVALID\n");
    }
    else
    {
        if(first_numbers == 34 || first_numbers == 37)
        {
            printf("AMEX\n");
            return 0;
        }
        if(first_numbers > 50 && first_numbers < 56)
        {
            printf("MASTERCARD\n");
            return 0;
        }
        if(first_number == 4)
        {
            printf("VISA\n");
            return 0;
        }
        printf("INVALID\n");
    }
    return 0;
}