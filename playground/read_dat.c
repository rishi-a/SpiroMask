#include<stdio.h>
#include <stdlib.h> // For exit()
#include <stdint.h>

int32_t samples[200];


void main(){
	char *st = "Welcome to 5p1romask";
	printf("%s\n", st);

	FILE *fptr;
  
    char filename[100], c;

    fptr = fopen("external-sensors/data/datalog.dat", "r");
    if (fptr == NULL){
        printf("Cannot open file \n");
        exit(0);
    }

    fread(samples,sizeof(samples),1,fptr);

    fclose(fptr);

    for(int i = 0; i<200; i++)
    printf("%u ", samples[i]); // prints a series of bytes
  
}