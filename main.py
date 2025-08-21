import sys
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog,
    QComboBox, QFormLayout, QLineEdit, QMessageBox, QTextEdit
)
from app import main_execute  # tu script principal

# ---- Redirección de stdout y stderr ----
class EmittingStream(QObject):
    textWritten = pyqtSignal(str)
    def write(self, text):
        self.textWritten.emit(str(text))
    def flush(self):
        pass

# ---- Hilo para ejecutar procesos sin congelar la UI ----
class WorkerThread(QThread):
    def __init__(self, param1, param2, param3):
        super().__init__()
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3

    def run(self):
        # Aquí se ejecuta el proceso pesado
        main_execute(self.param1, self.param2, self.param3)

# ---- Interfaz principal ----
class ReportSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Redirigir stdout y stderr a la ventana
        sys.stdout = EmittingStream(textWritten=self.normal_output_written)
        sys.stderr = EmittingStream(textWritten=self.normal_output_written)

    def initUI(self):
        self.setWindowTitle('Breacking Changes')
        self.setGeometry(300, 200, 500, 500)

        self.label = QLabel("Selecciona los parámetros y genera el reporte", self)

        self.combo1 = QComboBox()
        self.combo1.addItems(["Seleccione...", "Colombia", "Mexico", "Argentina", "Peru"])

        self.input2 = QLineEdit()

        self.combo2 = QComboBox()
        self.combo2.addItems(["Seleccione...", "3.0.0", "3.0.1"])

        form_layout = QFormLayout()
        form_layout.addRow("Pais:", self.combo1)
        form_layout.addRow("Token consola LRBA:", self.input2)
        form_layout.addRow("Versión objetivo:", self.combo2)

        self.btn_generate = QPushButton('Generar Reporte', self)
        self.btn_generate.clicked.connect(self.generate_report)

        self.btn_open = QPushButton('Abrir Reporte', self)
        self.btn_open.clicked.connect(self.open_report)

        # Área para mostrar logs
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(form_layout)
        layout.addWidget(self.btn_generate)
        layout.addWidget(self.btn_open)
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def generate_report(self):
        param1 = self.combo1.currentText()
        param2 = self.input2.text()
        param3 = self.combo2.currentText()

        if "Seleccione..." in [param1, param3] or not param2:
            QMessageBox.warning(self, "Validación", "Debe seleccionar un valor para todos los parámetros.")
            return

        # Ejecutar en hilo para no congelar UI
        self.worker = WorkerThread(param1, param2, param3)
        self.worker.finished.connect(lambda: self.label.setText("Proceso ejecutado."))
        self.worker.start()

    def open_report(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir Reporte", "", "Archivos Excel (*.xlsx);;Todos (*.*)")
        if file_name:
            self.label.setText(f"Reporte abierto: {file_name}")

    def normal_output_written(self, text):
        self.log_output.append(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReportSystem()
    window.show()
    sys.exit(app.exec_())
