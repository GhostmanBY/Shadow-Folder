from collections import defaultdict
from pathlib import Path

from PySide6.QtWidgets import QFileSystemModel
from PySide6.QtGui import QIcon
from PySide6.QtCore import QFileInfo, Qt, QMutex

from .icon_manager import IconDownloader
from .Dic_Extensiones import ICONS_TYPE_FILES_ICONIFY

json_file_mutex = QMutex()

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
