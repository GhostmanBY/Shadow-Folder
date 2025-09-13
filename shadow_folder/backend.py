import os
import platform
import shutil
import subprocess
from pathlib import Path

def get_home_path():
    """Devuelve la ruta de inicio del usuario según el sistema operativo."""
    if platform.system() == "Windows":
        try:
            path = os.environ.get('USERPROFILE')
            if not path:
                path = os.environ.get('HOMEDRIVE', '') + os.environ.get('HOMEPATH', '')
            return path
        except Exception:
            return os.path.expanduser('~')
    else:
        return os.path.expanduser('~')

def get_root_path():
    """Devuelve la ruta raíz del sistema."""
    if platform.system() == "Windows":
        drive = os.path.splitdrive(os.getcwd())[0]
        return drive + '\\' if drive else '\\'
    else:
        return '/'

def copy_item(source_path, destination_path):
    """Copia un archivo o directorio."""
    try:
        shutil.copy(source_path, destination_path)
        return f"Se copió {source_path} a {destination_path}", True
    except Exception as e:
        return f"Error al copiar: {e}", False

def move_item(source_path, destination_path):
    """Mueve un archivo o directorio."""
    try:
        shutil.move(source_path, destination_path)
        return f"Se movió {source_path} a {destination_path}", True
    except Exception as e:
        return f"Error al mover: {e}", False

def delete_item(path):
    """Elimina un archivo o directorio."""
    try:
        if Path(path).is_file():
            os.remove(path)
        elif Path(path).is_dir():
            try:
                os.rmdir(path)
            except OSError:
                shutil.rmtree(path)
        return "Elemento eliminado correctamente.", True
    except Exception as e:
        return f"Error al eliminar: {e}", False

def open_file(path):
    """Abre un archivo con la aplicación predeterminada del sistema."""
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        else:
            subprocess.Popen(['gio', 'open', path], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        return f"Abriendo {path}", True
    except Exception as e:
        return f"Error al abrir {path}: {e}", False

def path_exists(path):
    """Verifica si una ruta existe."""
    return os.path.exists(path)
