import customtkinter as ctk
import json
import os
import csv
import random
from ventana_base import BaseVentana
from componentes import crear_boton_regresar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class DoctorVisualizarECG(BaseVentana):
    def __init__(self, nombre_paciente, documento_paciente):
        super().__init__("Visualizar ECG")
        
        self.nombre_paciente = nombre_paciente
        self.documento_paciente = documento_paciente
        self.señal_ecg = self.cargar_ultimo_ecg()

        # Botón regresar
        crear_boton_regresar(self, self.volver)

        # --- Información del paciente (más compacta) ---
        ctk.CTkLabel(
            self.contenido,
            text=f"Paciente: {nombre_paciente}",
            font=("Arial", 14, "bold"),
            text_color="black"
        ).pack(pady=(15, 2))  # Menos espacio

        ctk.CTkLabel(
            self.contenido,
            text=f"CC. {documento_paciente}",
            font=("Arial", 12),
            text_color="black"
        ).pack(pady=(0, 15))  # Menos espacio

        # --- Gráfico ECG ---
        if self.señal_ecg:
            self.mostrar_grafico_ecg()
        else:
            ctk.CTkLabel(
                self.contenido,
                text="No se encontraron registros ECG",
                text_color="red",
                font=("Arial", 12, "bold")
            ).pack(pady=15)

        # --- Botón para generar registro ---
        if self.señal_ecg:
            ctk.CTkButton(
                self.contenido,
                text="Generar registro",
                width=200,
                height=45,
                corner_radius=25,
                fg_color="#3E7CB1",
                hover_color="#2F5E85",
                font=("Arial", 13, "bold"),
                command=self.generar_registro
            ).pack(pady=15)  # Menos espacio

        self.mainloop()

    def cargar_ultimo_ecg(self):
        """Carga el último ECG registrado del paciente"""
        archivo_ecg = "registros_ecg.csv"
        if not os.path.exists(archivo_ecg):
            return None

        try:
            with open(archivo_ecg, "r", encoding="utf-8") as f:
                lector = csv.DictReader(f)
                registros = []
                for fila in lector:
                    if fila.get("documento") == self.documento_paciente:
                        registros.append(fila)
                
                if registros:
                    # Tomar el último registro
                    ultimo_registro = registros[-1]
                    # Convertir string de lista a lista real
                    señal_str = ultimo_registro.get("señal_ecg", "[]")
                    return eval(señal_str)  # Convierte string a lista
                
            return None
        except Exception as e:
            print(f"Error cargando ECG: {e}")
            return None

    def mostrar_grafico_ecg(self):
        """Muestra el gráfico ECG con diseño más compacto"""
        # Crear figura más compacta
        fig, ax = plt.subplots(figsize=(4.5, 2.5))  # Más pequeño
        
        # Graficar la señal
        ax.plot(self.señal_ecg, color="black", linewidth=1)
        
        # Configurar título y ejes
        ax.set_title("ECG Signal", fontsize=12, weight="bold")  # Título más pequeño
        ax.set_xlabel("Muestras")
        ax.set_ylabel("mV")
        ax.grid(True, alpha=0.3)
        
        # Ajustar diseño para que ocupe menos espacio
        plt.tight_layout()
        
        # Mostrar en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=self.contenido)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)  # Menos espacio alrededor del gráfico

    def generar_registro(self):
        """Abre la ventana para generar registro con observaciones"""
        if not self.señal_ecg:
            self.mostrar_popup("No hay señal ECG para generar registro")
            return
            
        self.destroy()
        from doctor.registro import DoctorRegistroECG
        DoctorRegistroECG(self.nombre_paciente, self.documento_paciente, self.señal_ecg)

    def mostrar_popup(self, mensaje):
        popup = ctk.CTkToplevel(self)
        popup.title("Aviso")
        popup.geometry("320x150")
        popup.resizable(False, False)
        popup.grab_set()

        ctk.CTkLabel(popup, text=mensaje, font=("Arial", 13, "bold"), text_color="black").pack(pady=(40, 10))
        ctk.CTkButton(popup, text="Aceptar", width=100, fg_color="#3E7CB1", hover_color="#2F5E85",
                      command=popup.destroy).pack(pady=10)

    def volver(self):
        self.destroy()
        from doctor.buscar import DoctorBuscarPaciente
        DoctorBuscarPaciente()