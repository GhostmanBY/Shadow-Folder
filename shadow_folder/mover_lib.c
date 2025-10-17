#include <stdio.h>

// Función que retorna 0 si éxito, -1 si error
int mover_archivo(const char *origen, const char *destino) {
    if (rename(origen, destino) == 0) {
        return 0;  // Éxito
    } else {
        return -1;  // Error
    }
}