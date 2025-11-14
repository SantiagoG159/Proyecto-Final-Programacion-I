import customtkinter as ctk
from ventana_base import BaseVentana
from componentes import crear_boton_regresar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import ast
import os

class PacienteVisualizarECG(BaseVentana):
    def __init__(self, documento):
        super().__init__("Ver Examen ECG")
        self.documento_actual = documento

        # --- Flecha de regresar ---
        crear_boton_regresar(self, self.volver)

        # --- Título superior ---
        titulo = ctk.CTkLabel(
            self.contenido,
            text="Examen ECG",
            font=("Arial", 16, "bold"),
            text_color="black"
        )
        titulo.pack(pady=(20, 10))

        # --- Frame para gráfico ---
        frame_grafico = ctk.CTkFrame(self.contenido, fg_color="white", corner_radius=10)
        frame_grafico.pack(pady=15, padx=15, fill="both", expand=True)

        # --- Mostrar gráfico ECG ---
        self.mostrar_grafico(frame_grafico)

        # --- Labels de información ---
        self.label_doctor = ctk.CTkLabel(
            self.contenido,
            text="Doctor: Juan Yepes",  # por ahora es estático
            font=("Arial", 13)
        )
        self.label_doctor.pack(pady=(10, 0))

        self.label_cc = ctk.CTkLabel(
            self.contenido,
            text="CC. 1589782345",  # también estático por ahora
            font=("Arial", 13)
        )
        self.label_cc.pack(pady=(0, 15))

        self.mainloop()

    def mostrar_grafico(self, frame):
        """Busca el ECG más reciente del paciente y lo grafica."""
        archivo_ecg = "registros_ecg.csv"
        ultima_senal = None

        if os.path.exists(archivo_ecg):
            with open(archivo_ecg, "r", encoding="utf-8") as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    if fila.get("documento") == self.documento_actual:
                        try:
                            ultima_senal = ast.literal_eval(fila["señal_ecg"])
                        except Exception as e:
                            print(f"Error al leer señal: {e}")
                        # Sigue leyendo hasta el último registro

        if ultima_senal:
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(ultima_senal, color='red', linewidth=1)
            ax.set_title("Señal ECG", fontsize=12)
            ax.set_xlabel("Muestras")
            ax.set_ylabel("Amplitud (mV)")
            ax.grid(True)

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        else:
            ctk.CTkLabel(
                frame,
                text="No se encontró ningún registro ECG.",
                font=("Arial", 13),
                text_color="gray"
            ).pack(pady=30)

    def volver(self):
        """Regresa al panel del paciente."""
        self.destroy()
        from pacientes.funciones import PacientePrincipal
        PacientePrincipal(self.documento_actual)
