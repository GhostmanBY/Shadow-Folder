import sys
from pathlib import Path

from .Utils import CustomFileSystemModel
from . import backend

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTreeView, QListView, QSplitter, QStatusBar, QLineEdit,
    QPushButton, QFileSystemModel, QMessageBox
)
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt, QDir, QSize, Signal, QModelIndex

class Milist_View(QListView):
    exe_accion_sig = Signal(QModelIndex)
    copy_accion_sig = Signal(str)
    delet_accion_sig = Signal(str, str)

    def __init__(self):
        super().__init__()
        if not hasattr(self, 'ya'):
            self.path = ''
            self.copy_full_path = ''
            self.copy_cut_path = ''
            self.cut_copy = False
            self.flag = False
            self.ya = True

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return:
            self.exe_accion_sig.emit(self.currentIndex())
        
        if event.key() == Qt.Key.Key_C and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.cut_copy = False
            self.flag = True

        elif event.key() == Qt.Key.Key_X and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.cut_copy = True
            self.flag = True
        
        if self.flag:
            try:
                index = self.currentIndex().data()
                self.copy_full_path = f"{self.path}/{index}"
                self.copy_cut_path = self.path
                mode = "copio" if not self.cut_copy else "corto"
                self.copy_accion_sig.emit(f"El archivo {index} se {mode}")
            except Exception as e:
                print(f"Error: {e}")
                mode = "copio" if not self.cut_copy else "corto"
                self.copy_accion_sig.emit(f"No se pudo {mode} el archivo {index}")
            self.flag = False
        
        if event.key() == Qt.Key.Key_V and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if self.path != self.copy_cut_path and self.copy_cut_path != '':
                if self.cut_copy:
                    message, success = backend.move_item(self.copy_full_path, self.path)
                else:
                    message, success = backend.copy_item(self.copy_full_path, self.path)
                
                self.copy_accion_sig.emit(message)
                if success:
                    self.copy_full_path = ''
                    self.copy_cut_path = ''
                    self.cut_copy = None

        if event.key() == Qt.Key.Key_Delete:
            try:
                index = self.currentIndex().data()
                self.delet_accion_sig.emit(f"El archivo {index} se va a eliminar", index)
            except Exception as e:
                print(f"Error: {e}")
                self.delet_accion_sig.emit(f"No se pudo eliminar el archivo", '')
        else:
            super().keyPressEvent(event)

class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Archivos")
        self.setGeometry(100, 100, 900, 600)

        self.path = backend.get_home_path()
        self.root = backend.get_root_path()
        self.list_nav = []

        self.init_ui()

    def _copy_file(self, text):
        self.file_view.path = self.path
        self.status.showMessage(text)

    def _delet_file(self, text, index):
        self.status.showMessage(text)
        full_path = f"{self.path}/{index}"

        is_file = Path(full_path).is_file()
        mode = f"¿Estas seguro de borrar el archivo {index}?" if is_file else f"¿Estas seguro de borrar la carpeta {index}?"
        
        reply = QMessageBox.question(self, "Borrar un Archivo", mode, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            message, success = backend.delete_item(full_path)
            if success:
                QMessageBox.information(self, "Acción correcta", message)
                self.status.showMessage("Listo")
            else:
                QMessageBox.warning(self, "Error en acción", message)
                self.status.showMessage("Error en su acción")

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        splitter_Line_Finde = QSplitter(Qt.Orientation.Horizontal)
        splitter_Tree_Filed = QSplitter(Qt.Orientation.Horizontal)

        self.bar_find = QLineEdit()
        self.bar_find.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bar_find.setText(self.path)

        self.botton_back = QPushButton("◄")
        self.botton_back.setFixedSize(25, 25)
        self.botton_back.clicked.connect(lambda: self.back_dir_next(self.path, True))

        self.botton_next = QPushButton("►")
        self.botton_next.setFixedSize(25, 25)
        self.botton_next.clicked.connect(lambda: self.back_dir_next(self.path, False))

        self.botton_home = QPushButton("🏠")
        self.botton_home.setFixedSize(25, 25)
        self.botton_home.clicked.connect(lambda: self.send_dir_finde(backend.get_home_path()))

        self.botton_finde = QPushButton("🔍")
        self.botton_finde.setFixedSize(25, 25)
        self.botton_finde.clicked.connect(lambda: self.send_dir_finde(self.bar_find.text()))

        self.dir_model = QFileSystemModel()
        self.dir_model.setRootPath(self.root)
        self.dir_model.setFilter(QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot)

        self.dir_tree = QTreeView()
        self.dir_tree.setModel(self.dir_model)
        self.dir_tree.setRootIndex(self.dir_model.index(self.path))
        self.dir_tree.setHeaderHidden(True)

        for col in range(1, self.dir_model.columnCount()):
            self.dir_tree.setColumnHidden(col, True)

        self.file_model = CustomFileSystemModel()
        self.file_model.setRootPath(self.path)
        self.file_view = Milist_View()
        self.file_view.path = self.path
        self.file_view.setModel(self.file_model)
        self.file_view.setRootIndex(self.file_model.index(self.path))
        self.file_view.setViewMode(QListView.ViewMode.IconMode)
        self.file_view.setIconSize(QSize(64, 64))
        self.file_view.setGridSize(QSize(100, 100))
        self.file_view.setSpacing(10)
        self.file_view.setDragEnabled(False)
        self.file_view.exe_accion_sig.connect(self.on_dir_selected)
        self.file_view.copy_accion_sig.connect(self._copy_file)
        self.file_view.delet_accion_sig.connect(self._delet_file)
        self.file_view.doubleClicked.connect(self.on_dir_selected)

        self.dir_tree.doubleClicked.connect(self.on_dir_selected)

        splitter_Line_Finde.addWidget(self.botton_back)
        splitter_Line_Finde.addWidget(self.botton_next)
        splitter_Line_Finde.addWidget(self.botton_home)
        splitter_Line_Finde.addWidget(self.bar_find)
        splitter_Line_Finde.addWidget(self.botton_finde)

        splitter_Tree_Filed.addWidget(self.dir_tree)
        splitter_Tree_Filed.addWidget(self.file_view)
        splitter_Tree_Filed.setSizes([300, 600])

        layout.addWidget(splitter_Line_Finde)
        layout.addWidget(splitter_Tree_Filed)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Listo")

    def back_dir_next(self, index: None, accion: bool):
        if backend.path_exists(index):
            new_path = self.path
            try:
                if accion:
                    new_path = str(Path(index).parent)
                    self.list_nav.insert(0, Path(index).name)
                else:
                    if self.list_nav:
                        new_path = str(Path(index) / self.list_nav.pop(0))
            except Exception:
                return
            self.send_dir_finde(new_path)

    def on_dir_selected(self, index):
        if not index.isValid():
            return

        dir_path = self.dir_model.filePath(index)
        if Path(dir_path).is_file():
            backend.open_file(dir_path)
            return
        
        self.send_dir_finde(dir_path)
        self.dir_tree.setRootIndex(self.dir_model.index(dir_path))
        self.list_nav = []

    def send_dir_finde(self, dir_path):
        if backend.path_exists(dir_path):
            self.path = dir_path
            self.status.showMessage(f"Directorio ingresado: Valido ({dir_path})")
            self.file_view.setRootIndex(self.file_model.setRootPath(dir_path))
            self.dir_tree.setRootIndex(self.dir_model.index(dir_path))
            self.bar_find.setText(dir_path)
            self.file_view.path = dir_path
        else:
            self.status.showMessage(f"Dirección ingresada: Inválida")
            self.bar_find.setText(self.path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileManager()
    window.show()
    sys.exit(app.exec())
