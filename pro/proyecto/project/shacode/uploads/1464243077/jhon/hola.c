#include <stdio.h>
#include <stdlib.h>

int main(void){
    int edad = 0;
    printf("dime tu edad: ");
    scanf("%d", &edad);
    
    if (edad >= 18){
	    char *nombre = malloc(50 * sizeof(char));
	    printf("dime tu nombre: ");
	    scanf("%49s", nombre);
	    printf("hola %s\n", nombre); 
        free(nombre);
        return 0;
    }
    printf("hijo de puta\n");
    
}


