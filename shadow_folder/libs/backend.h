#ifndef BACKEND_H
#define BACKEND_H

// ============================
// Export / Import de símbolos
// ============================
#if defined(_WIN32) || defined(__CYGWIN__)
  #ifdef BACKEND_BUILD
    #define BACKEND_API __declspec(dllexport)
  #else
    #define BACKEND_API __declspec(dllimport)
  #endif
  // Elegí convención de llamadas si querés (por defecto cdecl)
  #ifndef BACKEND_CALL
    #define BACKEND_CALL /* __stdcall */
  #endif
#else
  // En Linux/Unix exportamos sólo lo marcado como "default"
  #define BACKEND_API __attribute__((visibility("default")))
  #ifndef BACKEND_CALL
    #define BACKEND_CALL /* cdecl */
  #endif
#endif

#ifdef __cplusplus
extern "C" {
#endif

// ============================
// Notas de contrato
// ============================
// - Las funciones que devuelven const char* (get_home_path/get_root_path)
//   devuelven punteros válidos mientras dure el proceso (por ej. getenv()).
//   No liberar (NO free()) desde el llamador.
// - Las funciones devuelven 0 en éxito, -1 en error (ver errno/GetLastError()).

// Devuelve la ruta de inicio del usuario según el sistema operativo.
// Puntero NO debe ser liberado por el llamador.
BACKEND_API const char* BACKEND_CALL get_home_path(void);

// Devuelve la ruta raíz del sistema.
// Puntero NO debe ser liberado por el llamador.
BACKEND_API const char* BACKEND_CALL get_root_path(void);

// Verifica si una ruta existe. Devuelve 1 si existe, 0 si no, -1 en error.
BACKEND_API int BACKEND_CALL path_exists(const char* path);

// Copia un archivo (o, si implementás, directorio).
// Devuelve 0 en éxito, -1 en error.
BACKEND_API int BACKEND_CALL copy_item(const char* source_path, const char* destination_path);

// Mueve un archivo o directorio.
// Devuelve 0 en éxito, -1 en error.
BACKEND_API int BACKEND_CALL move_item(const char* source_path, const char* destination_path);

// Elimina un archivo o directorio.
// Devuelve 0 en éxito, -1 en error.
BACKEND_API int BACKEND_CALL delete_item(const char* path);

// Abre un archivo con la app predeterminada del sistema.
// Devuelve 0 en éxito, -1 en error.
BACKEND_API int BACKEND_CALL open_file(const char* path);

#ifdef __cplusplus
} // extern "C"
#endif

#endif // BACKEND_H
