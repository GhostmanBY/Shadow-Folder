int abrir_archivo(const char *ruta) {
    char comando[256];
    sprintf(comando, "gio open %s", ruta);
    system(comando);
    return 0;
    }