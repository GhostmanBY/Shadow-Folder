#include <stdio.h>

int borrar_archivo(const char *ruta) {
    if (remove(ruta) == 0) {
        return 0;  // Éxito
    } else {
        return -1;  // Error
    }
}