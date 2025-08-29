import sys
from PyQt5.QtCore import QObject, pyqtSignal, QThread, Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog,
    QComboBox, QGroupBox, QFrame, QMessageBox, QTextEdit, QGridLayout, QProgressBar,QHBoxLayout
)
from scripts import process, request, clone, prepare, final, ScriptArtefactory, ScriptExcel, constants
import zipfile
from datetime import datetime
import os

# ---- Redirección de stdout y stderr ----
class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        # Evitar enviar líneas vacías
        if text and not text.isspace():
            self.textWritten.emit(str(text))

    def flush(self):
        pass

# ---- Hilo para ejecutar procesos sin congelar la UI ----
class WorkerThread(QThread):
    progress = pyqtSignal(int, int)       # índice del paso, porcentaje (0-100)
    finished_step = pyqtSignal(int, bool) # índice del paso, éxito/fracaso

    def __init__(self, param1, param2, param3):
        super().__init__()
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.resultado = None
        self.error = None
        self._stopped = False

    def stop(self):
        self._stopped = True

    def run(self):
        try:
            input_filter = self.param1.lower()
            modo_latest = "latest"
            ctx = {}  # contexto para compartir datos entre pasos

            # Lista de pasos: (descripcion, callable, emitir_senales)
            steps = [
                ("Preparando entorno", lambda: prepare.init(), True),
                ("Descargas Artifactory", lambda: ScriptArtefactory.run(input_filter, modo_latest), True),
                # Grupo Excel + Request + Proceso
                ("Request LRBA", lambda: (ScriptExcel.generar_total(), 
                                        ctx.update({"data": request.create_request(input_filter, self.param3)}),
                                        process.process_data(ctx.get("data"))), True),
                ("Clone", lambda: clone.clone(), True),
                ("Compilación y generación de Reporte", lambda: ctx.update({"final": final.execute(self.param2)}) or ctx["final"], True),
            ]

            for idx, (desc, action, emit_signals) in enumerate(steps):
                if self._stopped:
                    break

                if emit_signals:
                    # progreso incremental antes de ejecutar la acción
                    for p in range(0, 60, 10):
                        if self._stopped:
                            break
                        self.progress.emit(idx, p)
                        self.msleep(80)

                if self._stopped:
                    break

                try:
                    action_result = action()
                except Exception as e:
                    if emit_signals:
                        self.progress.emit(idx, 100)
                        self.finished_step.emit(idx, False)
                    self.error = str(e)
                    return

                if emit_signals:
                    self.progress.emit(idx, 100)
                    self.finished_step.emit(idx, True)

            self.resultado = ctx.get("final", None)

        except Exception as e:
            self.error = str(e)



# ---- Interfaz principal ----
class ReportSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel de Ejecución")
        self.setStyleSheet("background-color: #1e1e2f; color: white; font-family: Arial;")
        self.initUI()

        # Redirigir stdout / stderr a la consola UI
        sys.stdout = EmittingStream(textWritten=self.normal_output_written)
        sys.stderr = EmittingStream(textWritten=self.normal_output_written)

    def initUI(self):
        grid = QGridLayout()

        # Paneles
        config_group = self.create_config_group()
        console_group = self.create_console_group()
        stats_group = self.create_stats_group()
        pipeline_group = self.create_pipeline_group()  # personalizado con barras

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

    # def create_config_group(self):
    #     group = QGroupBox("Configuración de Ejecución")
    #     group.setStyleSheet(self.groupbox_style())
    #     layout = QVBoxLayout()

    #     label_pais = QLabel("Selecciona País:")
    #     label_pais.setStyleSheet(self.label_style())
    #     layout.addWidget(label_pais)
    #     self.cb_pais = QComboBox()
    #     self.cb_pais.addItems(constants.PAISES)
    #     self.cb_pais.setStyleSheet(self.combobox_style())
    #     layout.addWidget(self.cb_pais)

    #     label_version = QLabel("Selecciona Versión:")
    #     label_version.setStyleSheet(self.label_style())
    #     layout.addWidget(label_version)
    #     self.cb_version = QComboBox()
    #     self.cb_version.addItems(constants.VERSIONES)
    #     self.cb_version.setStyleSheet(self.combobox_style())
    #     layout.addWidget(self.cb_version)

    #     label_cookie = QLabel("Cookie de sesión LRBA: *")
    #     label_cookie.setStyleSheet(self.label_style())
    #     layout.addWidget(label_cookie)
    #     self.cookie_text = QTextEdit()
    #     self.cookie_text.setPlaceholderText("Ingresa la cookie de sesión...")
    #     self.cookie_text.setFixedHeight(60)
    #     self.cookie_text.setStyleSheet(self.groupbox_style())
    #     layout.addWidget(self.cookie_text)

    #     btn_ejecutar = QPushButton("Ejecutar")
    #     btn_ejecutar.setStyleSheet(self.button_style())
    #     btn_ejecutar.clicked.connect(self.generate_report)
    #     layout.addWidget(btn_ejecutar, alignment=Qt.AlignLeft)

    #     # --- Botón Descargar ---
    #     self.btn_descargar = QPushButton("Descargar")
    #     self.btn_descargar.setStyleSheet(self.button_style())
    #     self.btn_descargar.setEnabled(False)  # Deshabilitado al inicio
    #     self.btn_descargar.clicked.connect(self.descargar_resultado)
    #     layout.addWidget(self.btn_descargar, alignment=Qt.AlignLeft)

    #     group.setMinimumHeight(100)
    #     group.setMaximumHeight(400)
    #     group.setFixedWidth(650)
    #     group.setLayout(layout)
    #     return group

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

        label_version = QLabel("Selecciona Versión:")
        label_version.setStyleSheet(self.label_style())
        layout.addWidget(label_version)
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

        # --- Contenedor horizontal para botones ---
        button_layout = QHBoxLayout()

        # Botón Ejecutar (izquierda)
        btn_ejecutar = QPushButton("Ejecutar")
        btn_ejecutar.setStyleSheet(self.button_style())
        btn_ejecutar.clicked.connect(self.generate_report)
        button_layout.addWidget(btn_ejecutar, alignment=Qt.AlignLeft)

        # Espaciador para empujar el segundo botón a la derecha
        button_layout.addStretch()

        # Botón Descargar (derecha)
        self.btn_descargar = QPushButton("Descargar")
        self.btn_descargar.setStyleSheet(self.button_style())
        self.btn_descargar.setEnabled(False)
        self.btn_descargar.clicked.connect(self.descargar_resultado)
        button_layout.addWidget(self.btn_descargar, alignment=Qt.AlignRight)

        # Agregar el layout de botones al layout principal
        layout.addLayout(button_layout)

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
        """
        Crea un grupo con elementos de pipeline; cada paso tiene:
         - etiqueta con nombre
         - barra de progreso (QProgressBar)
        Se almacenan referencias en self.pipeline_bars (index -> QProgressBar)
        """
        group = QGroupBox("Pipeline de Ejecución")
        group.setStyleSheet(self.groupbox_style())
        layout = QVBoxLayout()

        # Definir pasos (mantener sincronía con WorkerThread.steps)
        self.pipeline_steps = [
            "Preparando Entorno",
            "Descargas Artifactory",
            "Request LRBA",
            "Clone",
            "Compilación y generación de Reporte"
        ]

        # Diccionario para almacenar barras y etiquetas por índice
        self.pipeline_bars = {}
        self.pipeline_labels = {}

        for i, step in enumerate(self.pipeline_steps, 1):
            lbl = QLabel(f"{i}. {step}")
            lbl.setStyleSheet("padding: 5px;")

            # Barra de progreso para cada paso
            bar = QProgressBar()
            bar.setMaximum(100)
            bar.setValue(0)
            bar.setTextVisible(False)
            bar.setFixedHeight(10)
            # Estilo base; el color del chunk cambiará al marcar éxito/fallo
            bar.setStyleSheet("""
                QProgressBar {
                    background-color: #2c2c3c;
                    border-radius: 5px;
                    height: 10px;
                }
                QProgressBar::chunk {
                    background-color: #00ccff;
                    border-radius: 5px;
                }
            """)

            step_layout = QVBoxLayout()
            step_layout.setContentsMargins(6, 6, 6, 6)
            step_layout.addWidget(lbl)
            step_layout.addWidget(bar)

            frame = QFrame()
            frame.setLayout(step_layout)
            layout.addWidget(frame)

            self.pipeline_bars[i-1] = bar         # guardamos por índice 0-based
            self.pipeline_labels[i-1] = lbl

        group.setMinimumHeight(300)
        group.setMaximumHeight(400)
        group.setFixedWidth(650)
        group.setLayout(layout)
        return group

    # ---------- estilos reutilizables ----------
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

    # ---------- generación / ejecución ----------
    def generate_report(self):
        param1 = self.cb_pais.currentText()
        param2 = self.cb_version.currentText()
        param3 = self.cookie_text.toPlainText()

        if "Selecciona" in param1 or "Selecciona" in param2 or not param3.strip():
            QMessageBox.warning(self, "Validación", "Debe seleccionar un valor para todos los parámetros.")
            return

        # Reset visual del pipeline (barras y estilos)
        for idx, bar in self.pipeline_bars.items():
            bar.setValue(0)
            bar.setStyleSheet("""
                QProgressBar {
                    background-color: #2c2c3c;
                    border-radius: 5px;
                    height: 10px;
                }
                QProgressBar::chunk {
                    background-color: #00ccff;
                    border-radius: 5px;
                }
            """)
            self.pipeline_labels[idx].setStyleSheet("padding: 5px; color: white;")

        self.log_output.append("Iniciando ejecución del pipeline...")

        # Crear worker y conectar señales
        self.worker = WorkerThread(param1, param2, param3)
        self.worker.progress.connect(self.update_pipeline_progress)
        self.worker.finished_step.connect(self.mark_pipeline_step)
        self.worker.finished.connect(self.finalizar_ejecucion)  # QThread.finished -> invoca finalizar
        self.worker.start()

    def update_pipeline_progress(self, index, value):
        """Actualiza la barra de progreso del paso `index`."""
        if index in self.pipeline_bars:
            self.pipeline_bars[index].setValue(value)

    def mark_pipeline_step(self, index, success=True):
        """Marca el paso `index` como exitoso o fallido, cambiando el color."""
        if index in self.pipeline_bars:
            color = "#00cc66" if success else "#ff4d4d"
            self.pipeline_bars[index].setStyleSheet(f"""
                QProgressBar {{
                    background-color: #2c2c3c;
                    border-radius: 5px;
                    height: 10px;
                }}
                QProgressBar::chunk {{
                    background-color: {color};
                    border-radius: 5px;
                }}
            """)
            self.pipeline_bars[index].setValue(100)
            # Opcional: colorear también la etiqueta
            lab = self.pipeline_labels.get(index)
            if lab:
                lab.setStyleSheet(f"padding:5px; color: {color}; font-weight:bold;")

    # ---------- salida normal y finalización ----------
    def normal_output_written(self, text):
        # Recibe texto desde stdout/stderr y lo muestra en la consola
        self.log_output.append(text)

    def finalizar_ejecucion(self):
        # Este método se conecta al finished() del QThread worker
        # En QThread, finished se emite cuando run() termina
        if hasattr(self, "worker") and self.worker:
            if getattr(self.worker, "error", None):
                QMessageBox.critical(self, "Error", f"Ocurrió un error:\n{self.worker.error}")
                self.log_output.append(f"Error: {self.worker.error}")
            else:
                QMessageBox.information(self, "Éxito", "Script ejecutado correctamente")
                self.log_output.append("Proceso ejecutado.")
                self.btn_descargar.setEnabled(True)

                # Obtener resultados
                datos = getattr(self.worker, "resultado", None)
                if datos:
                    try:
                        self.actualizar_estadisticas(datos)
                    except Exception as e:
                        # si la estructura de datos no coincide, lo logueamos
                        self.log_output.append(f"Warning: no se pudieron actualizar estadísticas: {e}")

    def actualizar_estadisticas(self, datos):
        # Espera que 'datos' sea un dict con keys: total, errores, ok, clone
        self.label_total.setText(str(datos.get("total", 0)))
        self.label_error.setText(str(datos.get("errores", 0)))
        self.label_ok.setText(str(datos.get("ok", 0)))
        self.label_clone.setText(str(datos.get("clone", 0)))


    def descargar_resultado(self):
        # Obtener la ruta base (carpeta del script actual)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
        archivos = [
            constants.PRODUCTIVE_XLSX,
            constants.ERROR_XLSX,
            constants.CLONE_ERROR_XLSX
        ]

        archivos_existentes = []
        for root, _, files in os.walk(PARENT_DIR):
            for nombre in archivos:
                if nombre in files:
                    archivos_existentes.append(os.path.join(root, nombre))

        if not archivos_existentes:
            self.log_output.append("No se encontraron archivos para incluir en el ZIP.")
            return

        nombre_zip_sugerido = f"Reporte__Breackin_Change{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        destino_zip, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Reporte ZIP",
            nombre_zip_sugerido,
            "Archivo ZIP (*.zip);;Todos (*.*)"
        )

        if not destino_zip:
            return

        try:
            with zipfile.ZipFile(destino_zip, 'w') as zipf:
                for archivo in archivos_existentes:
                    zipf.write(archivo, os.path.basename(archivo))
            self.log_output.append(f"Archivos comprimidos en: {destino_zip}")
        except Exception as e:
            self.log_output.append(f"Error al crear ZIP: {str(e)}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReportSystem()
    window.showMaximized()
    window.show()
    sys.exit(app.exec_())
