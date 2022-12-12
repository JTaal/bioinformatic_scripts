#include <stdio.h>

int main(void)
{
    int n = 3;
    //for each row
    for (int i = 0; i < n; i++)
    {
        //for each column
        for (int j = 0; j < n; j++)
        {
            //Print a brick
            printf("#");
        }
        //Move to next row
        printf("\n");
    }





    int i = 0;
    while (i <= 2)
    {
        printf("jaja\n");
        i++;
    }

    printf("Press ENTER key to Continue\n");  
    getchar(); 
}

