import os, httpx
import json

from collections import defaultdict
from pathlib import Path

from PySide6.QtWidgets import QFileSystemModel, QListView
from PySide6.QtGui import QIcon, QPixmap, QKeyEvent
from PySide6.QtCore import QFileInfo, Qt, QThread, Signal, QMutexLocker, QMutex

from quicksee import quicksee
from Dic_Extensiones import ICONS_TYPE_FILES_ICONIFY, ICONS_TYPE_FOLDER_ICONIFY

json_file_mutex = QMutex()

DISC_OFF_NET_ICONS = 'Front/GUI/assets/Json/Dowload_Icons.json'

class IconDownloader(QThread):
    """
    Un hilo para descargar un icono de forma asíncrona.
    Emite una señal cuando la descarga se completa.
    """
    icon_downloaded = Signal(str, QIcon) # URL del icono, QIcon

    def __init__(self, icon_url, extension_file, json_mutex):
        super().__init__()
        self.icon_url = icon_url
        self.json_file_mutex = json_mutex
        self.extension_file = extension_file if extension_file != '' else 'default'
        self.exits_letter = False

    def request_icons(self):
        with httpx.Client() as client:
            response = client.get(self.icon_url)
            response.raise_for_status()
            data = response.content
            self.save_off_net(data)
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            icon = QIcon(pixmap)
            self.icon_downloaded.emit(self.icon_url, icon)

    def run(self):
        try:
            if os.path.exists(DISC_OFF_NET_ICONS):
                with open(DISC_OFF_NET_ICONS, 'r', encoding='utf-8') as f:
                    content_Icons = json.load(f)
                try:
                    letter = self.extension_file[0]
                    type_dict = content_Icons[letter]            
                    svg_raw = type_dict[self.extension_file]   
                    svg_raw = svg_raw[2:-1]
                    svg_bytes = svg_raw.encode('utf-8').decode('unicode_escape').encode('utf-8')
                    pixmap = QPixmap(32, 32)
                    pixmap.loadFromData(svg_bytes)
                    icon = QIcon(pixmap)
                    self.icon_downloaded.emit(self.icon_url, icon)
                    return
                except KeyError:
                    self.request_icons()
            else:
                self.request_icons()
        except httpx.RequestError as e:
            print(f"Error al guardar el icon: {self.extension_file} url: {self.icon_url} \nexepcion: {e}")
        except httpx.HTTPStatusError as e:
            print(f"Respuesta no exitosa: {e.response.status_code}")
                    
    
    def save_off_net(self, icon_svg):
        with QMutexLocker(self.json_file_mutex):
            letter = self.extension_file[0]
            dic_model = {}
            
            if os.path.exists(DISC_OFF_NET_ICONS):
                with open(DISC_OFF_NET_ICONS, 'r', encoding="utf-8") as f:
                    dic_load = json.load(f)

                for letters_disc in dic_load:
                    if letters_disc == letter:
                        if not dic_load[letter] == {self.extension_file: f'{icon_svg}'}:
                            dic_load[letter].update({self.extension_file: f'{icon_svg}'})
                            self.exits_letter = True
                            break
                        else:        
                            return
                if not self.exits_letter:
                    dic_load[letter] = {
                        self.extension_file: f'{icon_svg}'
                    }
                with open(DISC_OFF_NET_ICONS, 'w', encoding="utf-8") as f:
                    json.dump(dic_load, f, indent=4)
            else:
                dic_model[letter] = {
                    self.extension_file: f'{icon_svg}'
                }
                with open(DISC_OFF_NET_ICONS, 'w', encoding="utf-8") as f:
                    json.dump(dic_model, f, indent=4)

class CustomFileSystemModel(QFileSystemModel):
    def __init__(self):
        super().__init__()

        self.json_file_mutex = QMutex()

        self.DIC_LETTER_ICONS_TYPE_FILES_ICONIFY = defaultdict(dict)

        for clave, valor in ICONS_TYPE_FILES_ICONIFY.items():
            primera_letra = clave[0].lower() # Convertir a minúscula para manejo uniforme
            self.DIC_LETTER_ICONS_TYPE_FILES_ICONIFY[primera_letra][clave] = valor
        
        self.icon_cache = {}
        self.active_downloads = {}

    def data(self, index, role):
        if role == Qt.ItemDataRole.DecorationRole:
            file_path = self.filePath(index)
            info = QFileInfo(file_path)
            icon_url = None

            if Path(file_path).is_dir():
                icon_url = f"https://api.iconify.design/vscode-icons:default-folder.svg"
                
                letter_type = "default_folder"
            else:
                # Icono de archivo
                name_file = info.fileName().split(".")
                letter_file_type = name_file[-1] if len(name_file) > 1 else "default_file"
                disc = self.DIC_LETTER_ICONS_TYPE_FILES_ICONIFY

                if len(letter_file_type) > 0:
                    letra = letter_file_type[0].lower()
                    if letra in disc and letter_file_type in disc[letra]:
                        Pre_Diccionario = disc[letter_file_type[0].lower()][letter_file_type]
                        icon_url = Pre_Diccionario
                    else:
                        icon_url = "https://api.iconify.design/vscode-icons:default-file.svg"
                
                letter_type = letter_file_type
            
            if icon_url:
                if icon_url in self.icon_cache:
                    return self.icon_cache[icon_url] 
                 
                if icon_url not in self.active_downloads:
                    downloader = IconDownloader(icon_url, letter_type, json_file_mutex)
                    downloader.icon_downloaded.connect(self._icon_loaded)
                    downloader.finished.connect(downloader.deleteLater)
                    self.active_downloads[icon_url] = downloader
                    downloader.start()
                
                return QIcon() 
        return super().data(index, role)
    
    def _icon_loaded(self, icon_url, icon):
        """
        Slot que se llama cuando un icono ha sido descargado.
        Almacena el icono en caché y notifica a la vista para que se actualice.
        """
        self.icon_cache[icon_url] = icon
        if icon_url in self.active_downloads:
            del self.active_downloads[icon_url]
        
        top_left = self.index(0, 0)
        bottom_right = self.index(self.rowCount() - 1, self.columnCount() - 1)
        if top_left.isValid() and bottom_right.isValid():
            self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.DecorationRole])

    
if __name__ == "__main__":
    """icon_url = "https://api.iconify.design/vscode-icons:file-type-python.svg"
    response = requests.get(icon_url)   
    print(response.content)"""
