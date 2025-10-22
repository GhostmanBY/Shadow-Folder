import os
import httpx
from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker
from PySide6.QtGui import QIcon, QPixmap

# === CONFIGURACIÓN GLOBAL ===
ICON_CACHE_DIR = "assets/icons_cache"
os.makedirs(ICON_CACHE_DIR, exist_ok=True)

# Cliente HTTPX global compartido por todos los hilos
_shared_http_client = httpx.Client(http2=True, timeout=10.0, follow_redirects=True)

# Mutex global para acceso a disco
_cache_mutex = QMutex()


class IconDownloader(QThread):
    """
    Hilo para descargar íconos de forma asíncrona y cachearlos localmente.
    Si el ícono ya está cacheado, lo carga instantáneamente.
    """

    icon_downloaded = Signal(str, str, QIcon)  # file_path, icon_url, QIcon

    def __init__(self, icon_url: str, extension_file: str, file_path: str):
        super().__init__()
        self.icon_url = icon_url
        self.extension_file = extension_file if extension_file else "default"
        self.file_path = file_path
        print(f"[IconDownloader] Created for {self.icon_url}")

    def run(self):
        print(f"[IconDownloader] Starting thread for {self.icon_url}")
        try:
            icon = self.load_from_cache()
            if icon:
                print(f"[IconDownloader] Icon loaded from cache: {self.icon_url}")
                self.icon_downloaded.emit(self.file_path, self.icon_url, icon)
                return

            # Si no está cacheado, descargarlo
            print(f"[IconDownloader] Downloading icon: {self.icon_url}")
            data = self.download_icon()
            if data:
                self.save_to_cache(data)
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                print(
                    f"[IconDownloader] Icon downloaded and loaded into pixmap: {self.icon_url}"
                )
                self.icon_downloaded.emit(self.file_path, self.icon_url, QIcon(pixmap))

        except httpx.RequestError as e:
            print(f"[HTTPX] Error al descargar {self.icon_url}: {e}")
        except Exception as e:
            print(f"[IconDownloader] Error inesperado ({self.extension_file}): {e}")
        finally:
            print(f"[IconDownloader] Thread finished for {self.icon_url}")

    def cache_path(self):
        first_letter = self.extension_file[0].lower()
        folder = os.path.join(ICON_CACHE_DIR, first_letter)
        os.makedirs(folder, exist_ok=True)
        return os.path.join(folder, f"{self.extension_file}.svg")

    def load_from_cache(self):
        path = self.cache_path()
        if os.path.exists(path):
            pixmap = QPixmap()
            if pixmap.load(path):
                return QIcon(pixmap)
        return None

    def save_to_cache(self, data: bytes):
        path = self.cache_path()
        with QMutexLocker(_cache_mutex):
            try:
                with open(path, "wb") as f:
                    f.write(data)
            except Exception as e:
                print(f"[Cache] Error al guardar ícono {path}: {e}")

    def download_icon(self) -> bytes | None:
        r = _shared_http_client.get(self.icon_url)
        r.raise_for_status()
        return r.content
