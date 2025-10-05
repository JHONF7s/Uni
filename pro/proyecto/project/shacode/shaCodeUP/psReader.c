#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <string.h>

#define MAX 256

int main(){
    struct termios old_termios, new_termios;
    char password[MAX];
    int i = 0;
    char c;

    // guarda la anterior configuracion del terminal
    // en la direccion de memoria de old_termios
    tcgetattr(STDIN_FILENO, &old_termios); // get terminal attributes

    // esto genera una copia de la configuracion en forma de estructura
    // ya que es una variable normal
    new_termios = old_termios;
    new_termios.c_lflag &= ~(ECHO | ICANON);
    tcsetattr(STDIN_FILENO, TCSANOW, &new_termios);

    printf("[] Password: ");
    fflush(stdout); // esta funcion fuerza a que el buffer se imprima de inmediato

    while (i < MAX - 1 && read(STDIN_FILENO, &c, 1) == 1){
        if (c == '\n' || c == '\r'){
            break;
        }
        else if (c == 127 || c == 8){
            if (i > 0){
                i--;
                printf("\b \b");
                fflush(stdout);
            }
        }
        else{
            password[i] = c;
            i++;
            printf("*");
            fflush(stdout);
        }
    }
    password[i] = '\0';
    tcsetattr(STDIN_FILENO, TCSANOW, &old_termios);

    printf("\n");

    FILE *archivo;
    archivo = fopen(".tmp.txt", "w");

    if (archivo == NULL){
        perror("Error password temp file");
        return 1;
    }

    fprintf(archivo, "%s", password);
    fclose(archivo);
    return 0;

}

