import customtkinter as ctk
import json
import os
import csv
import random
from ventana_base import BaseVentana
from componentes import crear_boton_regresar

class DoctorBuscarPaciente(BaseVentana):
    def __init__(self):
        super().__init__("Panel del Doctor")
        self.paciente_actual = None
        self.documento_actual = None

        # --- Flecha de regresar (usando componentes.py) ---
        crear_boton_regresar(self, self.volver)

        # --- Título superior ---
        titulo = ctk.CTkLabel(
            self.contenido,
            text="Buscar Paciente",
            font=("Arial", 14, "bold"),
            text_color="black"
        )
        titulo.pack(pady=(25, 10))

        # --- Campo de identificación ---
        self.entry_id = self._crear_entry("Identificación del Paciente")

        # --- Botón de búsqueda ---
        self.boton_buscar = ctk.CTkButton(
            self.contenido,
            text="🔍",
            width=35,
            height=25,
            fg_color="transparent",
            text_color="black",
            command=self.buscar_paciente
        )
        self.boton_buscar.place(x=285, y=125)

        self.label_error = ctk.CTkLabel(
            self.contenido,
            text="",
            text_color="red",
            font=("Arial", 11, "bold")
        )
        self.label_error.pack(pady=(0, 10))

        # --- Campos adicionales ---
        self.entry_nombre = self._crear_entry("Nombres y Apellidos")
        self.entry_peso = self._crear_entry("Peso (kg)")
        self.entry_altura = self._crear_entry("Altura (m)", comando=self.calcular_imc)
        self.entry_imc = self._crear_entry("IMC", editable=False)

        # --- Frame para botones ---
        frame_botones = ctk.CTkFrame(self.contenido, fg_color="transparent")
        frame_botones.pack(pady=20)

        # --- Botón Generar ECG ---
        self.boton_generar_ecg = ctk.CTkButton(
            frame_botones,
            text="Generar ECG",
            width=150,
            height=45,
            corner_radius=25,
            fg_color="#4CAF50",
            hover_color="#45A049",
            font=("Arial", 13, "bold"),
            command=self.generar_ecg
        )
        self.boton_generar_ecg.pack(side="left", padx=10)

        # --- Botón Ver Historial ECG ---
        self.boton_historial = ctk.CTkButton(
            frame_botones,
            text="Ver Historial ECG",
            width=150,
            height=45,
            corner_radius=25,
            fg_color="#3E7CB1",
            hover_color="#2F5E85",
            font=("Arial", 13, "bold"),
            command=self.ver_historial
        )
        self.boton_historial.pack(side="left", padx=10)

        self.mainloop()

    def _crear_entry(self, placeholder, editable=True, comando=None):
        entry = ctk.CTkEntry(
            self.contenido,
            placeholder_text=placeholder,
            width=250,
            height=40
        )
        entry.pack(pady=8)
        if not editable:
            entry.configure(state="disabled")
        if comando:
            entry.bind("<KeyRelease>", lambda e: comando())
        return entry

    def buscar_paciente(self):
        doc = self.entry_id.get().strip()
        if not doc:
            self.label_error.configure(text="Ingrese un número de documento.")
            return

        try:
            with open("usuarios.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.label_error.configure(text="Archivo usuarios.json no encontrado.")
            return

        paciente_encontrado = None
        for paciente in data.get("paciente", []):
            if paciente["documento"] == doc:
                paciente_encontrado = paciente
                break

        if paciente_encontrado:
            self.label_error.configure(text="")
            self.paciente_actual = paciente_encontrado
            self.documento_actual = doc
            self.entry_nombre.delete(0, "end")
            self.entry_nombre.insert(0, paciente_encontrado["nombre_completo"])
            self.entry_peso.delete(0, "end")
            self.entry_peso.insert(0, str(paciente_encontrado["peso"]))
        else:
            self.label_error.configure(text="Paciente no encontrado")
            self.paciente_actual = None
            self.documento_actual = None
            self.entry_nombre.delete(0, "end")
            self.entry_peso.delete(0, "end")
            self.entry_imc.configure(state="normal")
            self.entry_imc.delete(0, "end")
            self.entry_imc.configure(state="disabled")

    def calcular_imc(self):
        try:
            peso = float(self.entry_peso.get())
            altura = float(self.entry_altura.get())
            imc = peso / (altura ** 2)

            if imc < 18.5:
                categoria = "bajo peso"
            elif imc < 25:
                categoria = "normal"
            elif imc < 30:
                categoria = "sobrepeso"
            else:
                categoria = "obesidad"

            self.entry_imc.configure(state="normal")
            self.entry_imc.delete(0, "end")
            self.entry_imc.insert(0, f"{imc:.1f} - {categoria}")
            self.entry_imc.configure(state="disabled")

        except ValueError:
            self.entry_imc.configure(state="normal")
            self.entry_imc.delete(0, "end")
            self.entry_imc.insert(0, "")
            self.entry_imc.configure(state="disabled")

    def obtener_senal_aleatoria(self):
        """Selecciona una señal ECG aleatoria de los archivos JSON"""
        try:
            # Paso 1: Elegir archivo aleatorio
            num_archivo = random.randint(1, 10)
            archivo = f"ecg_set_{num_archivo:02d}.json"
            ruta = os.path.join("ecg_jsons_grouped_keys", archivo)
            
            # Paso 2: Cargar y elegir señal aleatoria
            with open(ruta, "r") as f:
                datos = json.load(f)
            
            # Elegir una clave aleatoria (ecg_1, ecg_2, ..., ecg_10)
            clave_aleatoria = random.choice(list(datos.keys()))
            return datos[clave_aleatoria]
        except Exception as e:
            print(f"Error cargando señal ECG: {e}")
            # Señal por defecto si hay error
            return [random.uniform(-2, 2) for _ in range(500)]

    
    def generar_ecg(self):
        """Genera un nuevo registro ECG para el paciente"""
        if not self.documento_actual:
            self.mostrar_popup("Primero busque un paciente.")
            return

        # Obtener señal aleatoria
        señal_ecg = self.obtener_senal_aleatoria()

        # Guardar en registros_ecg.csv
        archivo_ecg = "registros_ecg.csv"
        nuevo_registro = {
            "documento": self.documento_actual,
            "nombre": self.paciente_actual["nombre_completo"],
            "señal_ecg": str(señal_ecg)  # Convertir lista a string para CSV
        }

        # Escribir en CSV sin fecha
        try:
            file_exists = os.path.exists(archivo_ecg)
            with open(archivo_ecg, "a", newline="", encoding="utf-8") as f:
                fieldnames = ["documento", "nombre", "señal_ecg"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                writer.writerow(nuevo_registro)
            
            self.mostrar_popup("✅ ECG generado exitosamente")
            
        except Exception as e:
            self.mostrar_popup(f"Error al generar ECG: {str(e)}")
        
    
    def ver_historial(self):
        """Ver historial ECG del paciente"""
        if not self.documento_actual:
            self.mostrar_popup("Primero busque un paciente.")
            return

        archivo_ecg = "registros_ecg.csv"
        tiene_registros = False

        if os.path.exists(archivo_ecg):
            with open(archivo_ecg, "r", encoding="utf-8") as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    if fila.get("documento") == self.documento_actual:
                        tiene_registros = True
                        break

        if not tiene_registros:
            self.mostrar_popup("¡El paciente no tiene registros de ECG!\nUse 'Generar ECG' primero.")
        else:
            self.destroy()
            from doctor.visualizar import DoctorVisualizarECG
            DoctorVisualizarECG(self.paciente_actual["nombre_completo"], self.documento_actual)

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
        from entrar import abrir_login
        self.destroy()
        abrir_login("Doctor", None)
