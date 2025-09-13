import os
import json
import httpx
from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker
from PySide6.QtGui import QIcon, QPixmap

DISC_OFF_NET_ICONS = 'assets/Json/Dowload_Icons.json'

class IconDownloader(QThread):
    """
    Un hilo para descargar un icono de forma asíncrona.
    Emite una señal cuando la descarga se completa.
    """
    icon_downloaded = Signal(str, QIcon)  # URL del icono, QIcon

    def __init__(self, icon_url, extension_file, json_mutex):
        super().__init__()
        self.icon_url = icon_url
        self.json_file_mutex = json_mutex
        self.extension_file = extension_file if extension_file != '' else 'default'

    def run(self):
        try:
            icon = self.load_from_cache()
            if icon:
                self.icon_downloaded.emit(self.icon_url, icon)
                return

            icon = self.download_icon()
            if icon:
                self.icon_downloaded.emit(self.icon_url, icon)

        except httpx.RequestError as e:
            print(f"Error al solicitar el icono: {self.extension_file} url: {self.icon_url} \nexepcion: {e}")
        except httpx.HTTPStatusError as e:
            print(f"Respuesta no exitosa: {e.response.status_code}")

    def load_from_cache(self):
        with QMutexLocker(self.json_file_mutex):
            if not os.path.exists(DISC_OFF_NET_ICONS):
                return None
            
            with open(DISC_OFF_NET_ICONS, 'r', encoding='utf-8') as f:
                content_icons = json.load(f)
            
            letter = self.extension_file[0]
            if letter in content_icons and self.extension_file in content_icons[letter]:
                svg_raw = content_icons[letter][self.extension_file]
                svg_raw = svg_raw[2:-1]
                svg_bytes = svg_raw.encode('utf-8').decode('unicode_escape').encode('utf-8')
                pixmap = QPixmap(32, 32)
                pixmap.loadFromData(svg_bytes)
                return QIcon(pixmap)
        return None

    def download_icon(self):
        with httpx.Client() as client:
            response = client.get(self.icon_url)
            response.raise_for_status()
            data = response.content
            self.save_to_cache(data)
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            return QIcon(pixmap)

    def save_to_cache(self, icon_svg):
        with QMutexLocker(self.json_file_mutex):
            letter = self.extension_file[0]
            dic_model = {}

            if os.path.exists(DISC_OFF_NET_ICONS):
                with open(DISC_OFF_NET_ICONS, 'r', encoding="utf-8") as f:
                    dic_load = json.load(f)
            else:
                dic_load = {}

            if letter not in dic_load:
                dic_load[letter] = {}
            
            if self.extension_file not in dic_load[letter]:
                dic_load[letter][self.extension_file] = f'{icon_svg}'
                with open(DISC_OFF_NET_ICONS, 'w', encoding="utf-8") as f:
                    json.dump(dic_load, f, indent=4)
