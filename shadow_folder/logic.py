from pathlib import Path
from PySide6.QtWidgets import QMessageBox


class LogicHandler:
    def __init__(self, ui, fs_manager):
        self.ui = ui
        self.fs_manager = fs_manager
        self.copy_full_path = ""
        self.copy_cut_path = ""
        self.cut_copy = False

    def copy_item(self):
        self.cut_copy = False
        self._set_copy_path()

    def cut_item(self):
        self.cut_copy = True
        self._set_copy_path()

    def _set_copy_path(self):
        try:
            index = self.ui.file_view.currentIndex().data()
            self.copy_full_path = f"{self.ui.path}/{index}"
            self.copy_cut_path = self.ui.path
            mode = "copio" if not self.cut_copy else "corto"
            self.ui.status.showMessage(f"El archivo {index} se {mode}")
        except Exception as e:
            print(f"Error al seleccionar para copiar/cortar: {e}")
            self.ui.status.showMessage(f"No se pudo seleccionar el archivo")

    def paste_item(self):
        if self.ui.path != self.copy_cut_path and self.copy_cut_path:
            if self.cut_copy:
                message, success = self.fs_manager.move_item(
                    self.copy_full_path, self.ui.path
                )
            else:
                message, success = self.fs_manager.copy_item(
                    self.copy_full_path, self.ui.path
                )

            self.ui.status.showMessage(message)
            if success:
                self.copy_full_path = ""
                self.copy_cut_path = ""
                self.cut_copy = False

    def delete_item(self):
        try:
            index = self.ui.file_view.currentIndex().data()
            full_path = f"{self.ui.path}/{index}"
        except Exception as e:
            self.ui.status.showMessage(
                "No se ha seleccionado ningún archivo para eliminar."
            )
            print(f"Error al obtener item para borrar: {e}")
            return

        is_file = Path(full_path).is_file()
        item_type = "archivo" if is_file else "carpeta"
        reply = QMessageBox.question(
            self.ui,
            "Confirmar borrado",
            f"¿Estás seguro de que quieres eliminar el {item_type} '{index}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            message, success = self.fs_manager.delete_item(full_path)
            if success:
                QMessageBox.information(self.ui, "Acción correcta", message)
            else:
                QMessageBox.warning(self.ui, "Error en acción", message)

    def handle_selection(self, index):
        if not index.isValid():
            return

        file_path = (
            self.ui.file_model.filePath(index)
            if self.ui.sender() == self.ui.file_view
            else self.ui.dir_model.filePath(index)
        )

        if Path(file_path).is_file():
            self.fs_manager.open_file(file_path)
        else:
            self.change_directory(file_path)
            if self.ui.sender() == self.ui.dir_tree:
                self.ui.list_nav = []

    def change_directory(self, path):
        if self.fs_manager.path_exists(path):
            self.ui.path = path
            self.ui.bar_find.setText(path)
            self.ui.file_view.setRootIndex(self.ui.file_model.setRootPath(path))
            self.ui.dir_tree.setRootIndex(self.ui.dir_model.index(path))
            self.ui.status.showMessage(f"Cargado: {path}")
        else:
            self.ui.status.showMessage("Ruta no válida")
            self.ui.bar_find.setText(self.ui.path)

    def navigate_back(self):
        current_path = Path(self.ui.path)
        parent_path = str(current_path.parent)
        if parent_path != self.ui.path:
            self.ui.list_nav.insert(0, current_path.name)
            self.change_directory(parent_path)

    def navigate_next(self):
        if self.ui.list_nav:
            next_folder = self.ui.list_nav.pop(0)
            new_path = str(Path(self.ui.path) / next_folder)
            self.change_directory(new_path)

if __name__ == "__main__":
    print("This module is not intended to be run directly.")