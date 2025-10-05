#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <string.h>

#define MAX 256

int main(){
    struct termios old_termios, new_termios;
    char key[MAX];
    int i = 0;
    char c;

    tcgetattr(STDIN_FILENO, &old_termios);

    new_termios = old_termios;
    new_termios.c_lflag &= ~(ECHO | ICANON);
    tcsetattr(STDIN_FILENO, TCSANOW, &new_termios);

    printf("[] Key: ");
    fflush(stdout);

    while (i < MAX - 1 && read(STDIN_FILENO, &c, 1) == 1){
        if (c == '\n' || c == '\r'){
	    break;
	}
        else if (c == 8 || c == 127){
	    if (i > 0){
	        i--;
    		printf("\b \b");
		fflush(stdout);
	    }
	}
	else{
	    key[i] = c;
	    i++;
            printf("*");
	    fflush(stdout);
	}
    }
    key[i] = '\0';
    tcsetattr(STDIN_FILENO, TCSANOW, &old_termios);

    printf("\n");

    FILE *archivo;
    archivo = fopen(".tmp.txt", "w");

    if (archivo == NULL){
	perror("error key temp file");
	return 1;
    }

    fprintf(archivo, "%s", key);
    fclose(archivo);
    return 0;
}
