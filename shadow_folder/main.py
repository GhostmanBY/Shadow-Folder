import sys
from .Utils import CustomFileSystemModel
from .backend import FileSystemManager
from .logic import LogicHandler

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTreeView,
    QListView,
    QSplitter,
    QStatusBar,
    QLineEdit,
    QPushButton,
    QFileSystemModel,
)
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt, QDir, QSize, Signal, QModelIndex


class Milist_View(QListView):
    def __init__(self, logic_handler):
        super().__init__()
        print("[DEBUG] Inicializando Milist_View")
        print(f"[DEBUG] logic_handler recibido: {logic_handler}")
        self.logic = logic_handler
        print(f"[DEBUG] self.logic establecido: {self.logic}")
        # Verificar que los métodos existen
        print(f"[DEBUG] Métodos disponibles en logic: {dir(self.logic)}")

    def keyPressEvent(self, event: QKeyEvent):
        print(f"[DEBUG] KeyPressEvent - self.logic: {self.logic}")
        if event.key() == Qt.Key.Key_Return:
            print(f"[DEBUG] Intentando llamar handle_selection")
            self.logic.handle_selection(self.currentIndex())
            
        elif (
            event.key() == Qt.Key.Key_C
            and event.modifiers() & Qt.KeyboardModifier.ControlModifier
        ):
            print(f"[DEBUG] Intentando llamar copy_item")
            self.logic.copy_item()

        elif (
            event.key() == Qt.Key.Key_X
            and event.modifiers() & Qt.KeyboardModifier.ControlModifier
        ):
            self.logic.cut_item()

        elif (
            event.key() == Qt.Key.Key_V
            and event.modifiers() & Qt.KeyboardModifier.ControlModifier
        ):
            self.logic.paste_item()

        elif event.key() == Qt.Key.Key_Delete:
            self.logic.delete_item()
        else:
            super().keyPressEvent(event)


class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Archivos")
        self.setGeometry(100, 100, 900, 600)

        self.fs_manager = FileSystemManager()
        self.path = self.fs_manager.get_home_path()
        self.root = self.fs_manager.get_root_path()
        self.list_nav = []

        self.logic = LogicHandler(self, self.fs_manager)

        self.init_ui()
        self.logic.change_directory(self.path)

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        splitter_Line_Finde = QSplitter(Qt.Orientation.Horizontal)
        splitter_Tree_Filed = QSplitter(Qt.Orientation.Horizontal)

        self.bar_find = QLineEdit()
        self.bar_find.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bar_find.returnPressed.connect(
            lambda: self.logic.change_directory(self.bar_find.text())
        )

        self.botton_back = QPushButton("◄")
        self.botton_back.setFixedSize(25, 25)
        self.botton_back.clicked.connect(self.logic.navigate_back)

        self.botton_next = QPushButton("►")
        self.botton_next.setFixedSize(25, 25)
        self.botton_next.clicked.connect(self.logic.navigate_next)

        self.botton_home = QPushButton("🏠")
        self.botton_home.setFixedSize(25, 25)
        self.botton_home.clicked.connect(
            lambda: self.logic.change_directory(self.fs_manager.get_home_path())
        )

        self.botton_finde = QPushButton("🔍")
        self.botton_finde.setFixedSize(25, 25)
        self.botton_finde.clicked.connect(
            lambda: self.logic.change_directory(self.bar_find.text())
        )

        self.dir_model = QFileSystemModel()
        self.dir_model.setRootPath(self.root)
        self.dir_model.setFilter(QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot)

        self.dir_tree = QTreeView()
        self.dir_tree.setModel(self.dir_model)
        self.dir_tree.setHeaderHidden(True)
        self.dir_tree.doubleClicked.connect(self.logic.handle_selection)

        for col in range(1, self.dir_model.columnCount()):
            self.dir_tree.setColumnHidden(col, True)

        self.file_model = CustomFileSystemModel()
        self.file_view = Milist_View(self.logic)
        self.file_view.setModel(self.file_model)
        self.file_view.setViewMode(QListView.ViewMode.IconMode)
        self.file_view.setIconSize(QSize(64, 64))
        self.file_view.setGridSize(QSize(100, 100))
        self.file_view.setSpacing(10)
        self.file_view.setDragEnabled(False)
        self.file_view.doubleClicked.connect(self.logic.handle_selection)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileManager()
    window.show()
    sys.exit(app.exec())
