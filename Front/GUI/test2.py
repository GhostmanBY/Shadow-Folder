if event.key() == Qt.Key.Key_C and event.modifiers() & Qt.KeyboardModifier.ControlModifier: # type: ignore
        self.cut_copy = False # type: ignore
else event.key() == Qt.Key.Key_X and event.modifiers() & Qt.KeyboardModifier.ControlModifier: # type: ignore
        self.cut_copy = False # type: ignore
try:
    index = self.currentIndex().data() # type: ignore
    self.copy_full_path = f"{self.path + "/" + index}" # type: ignore
    self.copy_cut_path = self.path # type: ignore
    mode = "copio" if self.cut_copy == False else "corto" # type: ignore
    self.copy_accion_sig.emit(f"El archivo {index} se {mode}") # type: ignore
except Exception as e:
    print(f"Error: {e}") # type: ignore
    self.copy_accion_sig.emit(f"No se puedo copiar el archivo {index}") # type: ignore