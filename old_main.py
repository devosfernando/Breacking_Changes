import sys
from scripts import constants
from PyQt5.QtCore import QObject, pyqtSignal, QThread, Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog,
    QComboBox, QGroupBox, QFrame, QMessageBox, QTextEdit, QGridLayout
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
        self.resultado = None
        self.error = None

    def run(self):
        try:
            self.resultado = main_execute(self.param1, self.param2, self.param3)
        except Exception as e:
            self.error = str(e)
        #self.resultado = main_execute(self.param1, self.param2, self.param3)


# ---- Interfaz principal ----
class ReportSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel de Ejecución")
        self.setStyleSheet("background-color: #1e1e2f; color: white; font-family: Arial;")
        self.initUI()

        sys.stdout = EmittingStream(textWritten=self.normal_output_written)
        sys.stderr = EmittingStream(textWritten=self.normal_output_written)

    def initUI(self):
        grid = QGridLayout()

        # Paneles
        config_group = self.create_config_group()
        console_group = self.create_console_group()
        stats_group = self.create_stats_group()
        pipeline_group = self.create_pipeline_group()

        # Columna izquierda
        left_layout = QVBoxLayout()
        left_layout.addWidget(config_group)
        left_layout.addWidget(stats_group)

        # Columna derecha
        right_layout = QVBoxLayout()
        right_layout.addWidget(console_group)
        right_layout.addWidget(pipeline_group)

        grid.addLayout(left_layout, 0, 0)
        grid.addLayout(right_layout, 0, 1)

        self.setLayout(grid)
        self.resize(1100, 600)

    def create_config_group(self):
        group = QGroupBox("Configuración de Ejecución")
        group.setStyleSheet(self.groupbox_style())
        layout = QVBoxLayout()

        label_pais = QLabel("Selecciona País:")
        label_pais.setStyleSheet(self.label_style())
        layout.addWidget(label_pais)
        self.cb_pais = QComboBox()
        self.cb_pais.addItems(constants.PAISES)
        self.cb_pais.setStyleSheet(self.combobox_style())
        layout.addWidget(self.cb_pais)

        label_versión = QLabel("Selecciona Versión:")
        label_versión.setStyleSheet(self.label_style())
        layout.addWidget(label_versión)
        self.cb_version = QComboBox()
        self.cb_version.addItems(constants.VERSIONES)
        self.cb_version.setStyleSheet(self.combobox_style())
        layout.addWidget(self.cb_version)

        label_cookie = QLabel("Cookie de sesión LRBA: *")
        label_cookie.setStyleSheet(self.label_style())
        layout.addWidget(label_cookie)
        self.cookie_text = QTextEdit()
        self.cookie_text.setPlaceholderText("Ingresa la cookie de sesión...")
        self.cookie_text.setFixedHeight(60)
        self.cookie_text.setStyleSheet(self.groupbox_style())
        layout.addWidget(self.cookie_text)

        btn_ejecutar = QPushButton("Ejecutar")
        btn_ejecutar.setStyleSheet(self.button_style())
        btn_ejecutar.clicked.connect(self.generate_report)
        layout.addWidget(btn_ejecutar, alignment=Qt.AlignLeft)

        # --- Botón Descargar ---
        self.btn_descargar = QPushButton("Descargar")
        self.btn_descargar.setStyleSheet(self.button_style())
        self.btn_descargar.setEnabled(False)  # Deshabilitado al inicio
        self.btn_descargar.clicked.connect(self.descargar_resultado)
        layout.addWidget(self.btn_descargar, alignment=Qt.AlignLeft)

        group.setMinimumHeight(100)
        group.setMaximumHeight(400)
        group.setFixedWidth(650)
        group.setLayout(layout)
        return group

    def create_console_group(self):
        group = QGroupBox("Consola de Ejecución")
        group.setStyleSheet(self.groupbox_style())
        layout = QVBoxLayout()

        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet(
            "background-color: black; color: #00ccff; font-family: Consolas;margin:0")
        self.log_output.setText(
            " Sistema de detección de breaking changes iniciado\n Esperando configuración de ejecución...")
        layout.addWidget(self.log_output)

        group.setMinimumHeight(100)
        group.setMaximumHeight(400)
        group.setFixedWidth(650)
        group.setLayout(layout)
        return group



    def create_stats_group(self):
        group = QGroupBox("Estadísticas")
        group.setStyleSheet(self.groupbox_style())
        layout = QGridLayout()

        # Crear tarjetas y labels
        frame_total, self.label_total = self.stat_card("0", "Total Componentes", "#ffffff")
        frame_error, self.label_error = self.stat_card("0", "Componentes con Error", "#ff4d4d")
        frame_ok, self.label_ok = self.stat_card("0", "Componentes OK", "#00cc66")
        frame_clone, self.label_clone = self.stat_card("0", "Errores en Clone", "#00cc66")

        # Agregar frames al layout
        layout.addWidget(frame_total, 0, 0)
        layout.addWidget(frame_error, 0, 1)
        layout.addWidget(frame_ok, 1, 0)
        layout.addWidget(frame_clone, 1, 1)

        group.setLayout(layout)
        self.stats_group = group
        return group

    # def stat_card(self, value, text, color):
    #     frame = QFrame()
    #     frame.setStyleSheet(f"background-color: #374151; border-radius: 8px; padding: 12px;")
    #     vbox = QVBoxLayout()
    #     label_value = QLabel(value)
    #     label_value.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: bold;")
    #     label_value.setAlignment(Qt.AlignCenter)
    #     label_text = QLabel(text)
    #     label_text.setAlignment(Qt.AlignCenter)
    #     frame.setFixedWidth(200)
    #     vbox.addWidget(label_value)
    #     vbox.addWidget(label_text)
    #     frame.setLayout(vbox)
        
    #     return label_value  # <---- Cambiado para devolver QLabel
    #    # return frame

    def stat_card(self, value, text, color):
        frame = QFrame()
        frame.setStyleSheet("background-color: #374151; border-radius: 8px; padding: 12px;")
        vbox = QVBoxLayout()

        label_value = QLabel(value)
        label_value.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: bold;")
        label_value.setAlignment(Qt.AlignCenter)

        label_text = QLabel(text)
        label_text.setAlignment(Qt.AlignCenter)

        frame.setFixedWidth(200)
        vbox.addWidget(label_value)
        vbox.addWidget(label_text)
        frame.setLayout(vbox)

        return frame, label_value  # devolvemos frame y QLabel


    def create_pipeline_group(self):
        group = QGroupBox("Pipeline de Ejecución")
        group.setStyleSheet(self.groupbox_style())
        layout = QVBoxLayout()
        steps = ["Descargas Artifactory", "Clone", "Maven", "Generación de Reporte"]
        for i, step in enumerate(steps, 1):
            lbl = QLabel(f"{i}. {step}")
            lbl.setStyleSheet("padding: 5px;")
            layout.addWidget(lbl)
        group.setMinimumHeight(200)
        group.setMaximumHeight(300)
        group.setFixedWidth(650)
        group.setLayout(layout)
        return group

    def groupbox_style(self):
        return """
        QGroupBox {
            background-color: #1F2937;
            border: 1px solid #3a3a4d;
            border-radius: 8px;
            margin-top: 10px;
            font-weight: bold;
            padding: 10px;
        }
        """

    def combobox_style(self):
        return """
        QComboBox {
            background-color: #2c2c3c;
            border: 1px solid #3a3a4d;
            border-radius: 8px;
            padding: 5px;
        }
        """

    def label_style(self):
        return """
            background-color: #1F2937;
            color: white;
            padding: 4px;
            border-radius: 4px;
        """

    def button_style(self):
        return """
        QPushButton {
            background-color: #2626d9;
            color: white;
            padding: 8px 20px;
            border-radius: 6px;
            margin-top:5px;
        }
        QPushButton:disabled {
            background-color: #3a3a4d;
            color: #888;
        }
        """

    def generate_report(self):
        param1 = self.cb_pais.currentText()
        param2 = self.cb_version.currentText()
        param3 = self.cookie_text.toPlainText()

        if "Selecciona" in param1 or "Selecciona" in param2 or not param3.strip():
            QMessageBox.warning(self, "Validación", "Debe seleccionar un valor para todos los parámetros.")
            return

        self.worker = WorkerThread(param1, param2, param3)
        self.worker.finished.connect(self.finalizar_ejecucion)
        #self.worker.finished.connect(lambda: self.log_output.append("Proceso ejecutado."))
        self.worker.start()

    def open_report(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir Reporte", "", "Archivos Excel (*.xlsx);;Todos (*.*)")
        if file_name:
            self.log_output.append(f"Reporte abierto: {file_name}")

    def normal_output_written(self, text):
        self.log_output.append(text)

    def finalizar_ejecucion(self):
        if self.worker.error:
            QMessageBox.critical(self, "Error", f"Ocurrió un error:\n{self.worker.error}")
        else:
            QMessageBox.information(self, "Éxito", "Script ejecutado correctamente")
            self.log_output.append("Proceso ejecutado.")
            self.btn_descargar.setEnabled(True)

            # Obtener resultados del worker
            datos = self.worker.resultado
            print("DATOS--------------------------",datos)

            if datos:
                self.actualizar_estadisticas(datos)

    def actualizar_estadisticas(self, datos):
        self.label_total.setText(str(datos["total"]))
        self.label_error.setText(str(datos["errores"]))
        self.label_ok.setText(str(datos["ok"]))
        self.label_clone.setText(str(datos["clone"]))


    def descargar_resultado(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar Reporte", "", "Excel (*.xlsx);;Todos (*.*)")
        if file_name:
            # Aquí agregar lógica para guardar o copiar reporte a file_name
            self.log_output.append(f"Reporte descargado en: {file_name}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReportSystem()
    window.showMaximized()
    window.show()
    sys.exit(app.exec_())
