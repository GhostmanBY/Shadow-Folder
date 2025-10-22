#include "backend.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <windows.h>
#include <shlobj.h>
#else
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#endif

const char* get_home_path() {
#ifdef _WIN32
    return getenv("USERPROFILE");
#else
    return getenv("HOME");
#endif
}

const char* get_root_path() {
#ifdef _WIN32
    return "C:\\";
#else
    return "/";
#endif
}

int path_exists(const char* path) {
#ifdef _WIN32
    return GetFileAttributesA(path) != INVALID_FILE_ATTRIBUTES;
#else
    struct stat buffer;
    return (stat(path, &buffer) == 0);
#endif
}

int copy_item(const char* source_path, const char* destination_path) {
    FILE *source, *destination;
    char buffer[1024];
    size_t n;

    source = fopen(source_path, "rb");
    if (source == NULL) {
        return -1;
    }

    destination = fopen(destination_path, "wb");
    if (destination == NULL) {
        fclose(source);
        return -1;
    }

    while ((n = fread(buffer, 1, sizeof(buffer), source)) > 0) {
        if (fwrite(buffer, 1, n, destination) != n) {
            fclose(source);
            fclose(destination);
            return -1;
        }
    }

    fclose(source);
    fclose(destination);
    return 0;
}

int move_item(const char* source_path, const char* destination_path) {
    if (rename(source_path, destination_path) != 0) {
        // If rename fails, it might be across different filesystems. 
        // A move is a copy then delete.
        int result = copy_item(source_path, destination_path);
        if (result == 0) {
            delete_item(source_path);
        }
        return result;
    }
    return 0;
}

int delete_item(const char* path) {
#ifdef _WIN32
    if (RemoveDirectoryA(path)) {
        return 0;
    }
    if (DeleteFileA(path)) {
        return 0;
    }
    return -1;
#else
    return remove(path);
#endif
}

int open_file(const char* path) {
#ifdef _WIN32
    // Using ShellExecuteA for ANSI strings
    HINSTANCE result = ShellExecuteA(NULL, "open", path, NULL, NULL, SW_SHOWNORMAL);
    // The result of ShellExecuteA is a HINSTANCE, which is a pointer. 
    // If the value is greater than 32, the function was successful.
    return ((intptr_t)result > 32) ? 0 : -1;
#else
    char command[1024];
    snprintf(command, sizeof(command), "xdg-open %s", path);
    return system(command);
#endif
}
