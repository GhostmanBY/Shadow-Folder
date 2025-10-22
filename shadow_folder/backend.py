import ctypes

import platform
from pathlib import Path


class FileSystemManager:
    """Gestiona las operaciones del sistema de archivos utilizando una biblioteca C."""

    def __init__(self):
        self._load_c_library()

    def _load_c_library(self):
        """Carga la biblioteca C compartida."""
        lib_name = "backend.so"
        if platform.system() == "Windows":
            lib_name = "backend.dll"  # Asumiendo que la compilarías como DLL en Windows

        # Ruta a la biblioteca relativa a este archivo
        lib_path = Path(__file__).parent / "libs" / lib_name

        if not lib_path.exists():
            raise FileNotFoundError(
                f"No se encontró la biblioteca compartida en: {lib_path}"
            )

        self.c_lib = ctypes.CDLL(str(lib_path))
        self._define_c_functions()

    def _define_c_functions(self):
        """Define los tipos de argumentos y de retorno para las funciones C."""
        self.c_lib.get_home_path.restype = ctypes.c_char_p

        self.c_lib.get_root_path.restype = ctypes.c_char_p

        self.c_lib.path_exists.argtypes = [ctypes.c_char_p]
        self.c_lib.path_exists.restype = ctypes.c_int

        self.c_lib.copy_item.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.c_lib.copy_item.restype = ctypes.c_int

        self.c_lib.move_item.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.c_lib.move_item.restype = ctypes.c_int

        self.c_lib.delete_item.argtypes = [ctypes.c_char_p]
        self.c_lib.delete_item.restype = ctypes.c_int

        self.c_lib.open_file.argtypes = [ctypes.c_char_p]
        self.c_lib.open_file.restype = ctypes.c_int

    def get_home_path(self):
        """Devuelve la ruta de inicio del usuario."""
        return self.c_lib.get_home_path().decode("utf-8")

    def get_root_path(self):
        """Devuelve la ruta raíz del sistema."""
        return self.c_lib.get_root_path().decode("utf-8")

    def path_exists(self, path: str):
        """Verifica si una ruta existe."""
        return self.c_lib.path_exists(path.encode("utf-8")) != 0

    def copy_item(self, source_path: str, destination_path: str):
        """Copia un archivo."""
        source_bytes = str(source_path).encode("utf-8")
        dest_bytes = str(destination_path).encode("utf-8")
        result = self.c_lib.copy_item(source_bytes, dest_bytes)
        if result == 0:
            return f"Se copió {Path(source_path).name} a {destination_path}", True
        else:
            return f"Error al copiar {Path(source_path).name}", False

    def move_item(self, source_path: str, destination_path: str):
        """Mueve un archivo o directorio."""
        source_bytes = str(source_path).encode("utf-8")
        dest_bytes = str(destination_path).encode("utf-8")
        result = self.c_lib.move_item(source_bytes, dest_bytes)
        if result == 0:
            return f"Se movió {Path(source_path).name} a {destination_path}", True
        else:
            return f"Error al mover {Path(source_path).name}", False

    def delete_item(self, path: str):
        """Elimina un archivo o directorio."""
        path_bytes = str(path).encode("utf-8")
        result = self.c_lib.delete_item(path_bytes)
        if result == 0:
            return "Elemento eliminado correctamente.", True
        else:
            return f"Error al eliminar {Path(path).name}", False

    def open_file(self, path: str):
        """Abre un archivo con la aplicación predeterminada."""
        path_bytes = str(path).encode("utf-8")
        result = self.c_lib.open_file(path_bytes)
        if result == 0:
            return f"Abriendo {Path(path).name}", True
        else:
            return f"Error al abrir {Path(path).name}", False


# Ejemplo de uso (opcional, para pruebas)
if __name__ == "__main__":
    fs = FileSystemManager()
    home = fs.get_home_path()
    print(f"Home path: {home}")
    print(f"Root path: {fs.get_root_path()}")

    test_file = Path(home) / "test_file.txt"
    with open(test_file, "w") as f:
        f.write("hello")

    print(f"Exists {test_file}? {fs.path_exists(str(test_file))}")

    copied_file = Path(home) / "copied_file.txt"
    print(fs.copy_item(str(test_file), str(copied_file)))

    moved_file = Path(home) / "moved_file.txt"
    print(fs.move_item(str(copied_file), str(moved_file)))

    print(fs.delete_item(str(test_file)))
    print(fs.delete_item(str(moved_file)))
