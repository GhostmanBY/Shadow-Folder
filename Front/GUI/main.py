import sys, os, subprocess, shutil
from pathlib import Path

from Utils import CustomFileSystemModel

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTreeView, QListView, QSplitter, QStatusBar, QLineEdit,
    QPushButton, QFileSystemModel,
)
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt, QDir, QSize, Signal, QModelIndex

class Milist_View(QListView):
    exe_accion_sig = Signal(QModelIndex)
    copy_accion_sig = Signal(str)

    def __init__(self):
        super().__init__()
        """
        Esta clase puede ser inicializada varias veces debido a la sobreescritura de QListView.
        Para evitar que las variables de instancia se reinicialicen en cada llamada al constructor,
        se utiliza hasattr para comprobar si ya existen antes de inicializarlas.
        """
        if not hasattr(self, 'ya'):
            self.path = ''
            self.copy_full_path = ''
            self.copy_cut_path = ''
            self.ya = True

    def keyPressEvent(self, event: QKeyEvent):
        """
            Modificacion del metodo de KeyPressEvent para que haga las funciones de copiar, cortar, pegar y abrir/ejecutar archivos
            1. Enter: abrir/ejecutar
            2. Ctrl+C: Copiar
            3. Ctrl+X: Cortar
            4. Ctrl+V: Pegar     
        """
        #1: abrir/ejecutar
        if event.key() == Qt.Key.Key_Return:
            self.exe_accion_sig.emit(self.currentIndex())
        
        #2: Copiar
        if event.key() == Qt.Key.Key_C and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.cut_copy = False 

        #2: Cortar
        elif event.key() == Qt.Key.Key_X and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.cut_copy = True 
        
        #Extra: Como la logia de copiar y pegar es lo mismo se reutiliza el codigo manejado con la condicion de boleanos
        #Ex: Se utilizan condificonales ternarios para modificar los valores por su retoriedad
        if hasattr(self, 'cut_copy'):
            try:
                index = self.currentIndex().data() 
                self.copy_full_path = f"{self.path + "/" + index}" 
                self.copy_cut_path = self.path 
                mode = "copio" if self.cut_copy == False else "corto" 
                self.copy_accion_sig.emit(f"El archivo {index} se {mode}") 
            except Exception as e:
                print(f"Error: {e}") 
                mode = "copio" if self.cut_copy == False else "corto" 
                self.copy_accion_sig.emit(f"No se puedo {mode} el archivo {index}") 
        
        #4: Pegar
        if event.key() == Qt.Key.Key_V and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            try:
                #Ex: Se mantienen los condicionale ternarios por los cambios del boleano retorico
                if self.path != self.copy_cut_path and self.copy_cut_path != '':
                    shutil.copy(self.copy_full_path, self.path) if self.cut_copy == False else shutil.move(self.copy_full_path, self.path)
                    mode = "copio" if self.cut_copy == False else "corto"
                    self.copy_accion_sig.emit(f"Su archivo se {mode} de {self.copy_cut_path} a {self.path} correctamente") 
                    #Se limpian las variables de rutas guardadas
                    self.copy_full_path = ''
                    self.copy_cut_path = ''
            except Exception as e:
                print(f"Error: {e}")
                self.copy_accion_sig.emit(f"Su archivo no se puedo copio de {self.copy_cut_path} a {self.path} correctamente")
        else:
            super().keyPressEvent(event)

class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Archivos")
        self.setGeometry(100, 100, 900, 600)

        self.path = "/home/ghost/Descargas"
        self.copy_full_path = ''
        self.copy_cut_path = ''
        self.list_nav = []

        self.init_ui()      

    def _copy_file(self, text):
        self.file_view.path = self.path
        self.status.showMessage(text)

    def init_ui(self):
        # Widget central
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
         
        layout = QVBoxLayout(main_widget)

        splitter_Line_Finde = QSplitter(Qt.Orientation.Horizontal)
        splitter_Tree_Filed = QSplitter(Qt.Orientation.Horizontal)

        #Barra de busqueda
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
        # Conexión de selección
        self.botton_home.setFixedSize(25, 25)
        self.botton_home.clicked.connect(lambda: self.send_dir_finde("/home/ghost"))

        self.botton_finde = QPushButton("🔍")
        self.botton_finde.setFixedSize(25, 25)
        self.botton_finde.clicked.connect(lambda: self.send_dir_finde(self.bar_find.text()))


        # Modelo de sistema de archivos para directorios
        self.dir_model = QFileSystemModel()
        self.dir_model.setRootPath("/")
        self.dir_model.setFilter(QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot)

        # Vista de árbol (directorios)
        self.dir_tree = QTreeView()
        self.dir_tree.setModel(self.dir_model)
        self.dir_tree.setRootIndex(self.dir_model.index(self.path))
        self.dir_tree.setHeaderHidden(True)

        # Ocultar columnas extra si están
        for col in range(1, self.dir_model.columnCount()):
            self.dir_tree.setColumnHidden(col, True)

        # Vista de archivos en formato grid
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
        self.file_view.doubleClicked.connect(self.on_dir_selected)

        # Conexión de selección
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

        # Barra de estado
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Listo")

    def back_dir_next(self, index: None, accion: bool):
        if os.path.exists(index):
            try:
                if accion: 
                    new_path = '/'
                    part_path = index.split("/")
                    rang_path = len(part_path)
                    for dir in part_path:
                        if dir != '' and dir != part_path[rang_path-1]:
                            new_path = os.path.join(new_path, dir)
                        elif dir != '':
                            self.list_nav.insert(0, dir)

                else:
                    if self.list_nav == index:
                        return
                    else:
                        new_path = f"{index}" + f"/{self.list_nav[0]}" if index != "/" else f"{index}" + f"{self.list_nav[0]}"
                        self.list_nav.pop(0)
            except Exception:
                return
        self.path = new_path
        self.send_dir_finde(self.path)

    def on_dir_selected(self, index):
        if not index.isValid():
            return

        dir_path = self.dir_model.filePath(index)
        if Path(dir_path).exists() and Path(dir_path).is_file():
            subprocess.Popen(['gio', 'open', dir_path], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            return
        
        self.send_dir_finde(dir_path)
        view_index = self.file_view.rootIndex()
        for row in range(self.file_model.rowCount(view_index)):
            index = self.file_model.index(row, 0, view_index)
            file_name = self.file_model.fileName(index)
        self.dir_tree.setRootIndex(self.dir_model.index(dir_path))
        self.list_nav = []

    def send_dir_finde(self, dir):
        if os.path.exists(dir):
            self.path_prev = self.path
            self.path = dir
            self.status.showMessage(f"Directorio ingresada: Validad ({dir})")
            self.file_view.setRootIndex(self.file_model.setRootPath(dir))
            self.dir_tree.setRootIndex(self.dir_model.index(f"{dir}"))
            self.bar_find.setText(f"{dir}")
            self.file_view.path = dir
        else:
            self.status.showMessage(f"Direccion ingresada: Invalidad")
            self.bar_find.setText(f"{self.path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileManager()
    window.show()
    sys.exit(app.exec())
