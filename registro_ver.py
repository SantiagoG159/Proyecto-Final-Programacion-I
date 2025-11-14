import customtkinter as ctk
import json
import os
from ventana_base import BaseVentana
from componentes import crear_boton_regresar

class PacienteRegistroECG(BaseVentana):
    def __init__(self, documento):
        super().__init__("Ver Descripción ECG")
        self.documento_actual = documento

        # --- Flecha para regresar ---
        crear_boton_regresar(self, self.volver)

        # --- Label del doctor (sin CC) ---
        self.label_doctor = ctk.CTkLabel(
            self.contenido,
            text="Doctor: ---",
            font=("Arial", 13)
        )
        self.label_doctor.pack(pady=(15, 10))

        # --- Cuadro de texto para observaciones ---
        self.cuadro_texto = ctk.CTkTextbox(
            self.contenido,
            width=300,
            height=180,
            corner_radius=10,
            fg_color="white",
            text_color="black",
            font=("Arial", 13),
            wrap="word"
        )
        self.cuadro_texto.pack(pady=(10, 15))
        self.cuadro_texto.configure(state="disabled")

        # --- Botón Salir ---
        boton_salir = ctk.CTkButton(
            self.contenido,
            text="Salir",
            width=150,
            height=40,
            corner_radius=25,
            fg_color="#3E7CB1",
            hover_color="#2F5E85",
            font=("Arial", 13, "bold"),
            command=self.volver
        )
        boton_salir.pack(pady=(10, 15))

        # --- Cargar descripción del archivo JSON ---
        self.cargar_descripcion()

        self.mainloop()

    def cargar_descripcion(self):
        """Lee la descripción del ECG desde doc_regis.json y la muestra."""
        # Ruta absoluta al archivo global
        archivo_json = os.path.abspath("doc_regis.json")

        if not os.path.exists(archivo_json):
            self.mostrar_texto("No se encontró el archivo de descripciones.")
            return

        try:
            with open(archivo_json, "r", encoding="utf-8") as f:
                registros = json.load(f)

            encontrado = False
            for r in registros:
                if r.get("documento_paciente") == self.documento_actual:
                    doctor = r.get("doctor", "Desconocido")
                    observaciones = r.get("observaciones", "Sin observaciones registradas.")
                    self.label_doctor.configure(text=f"Doctor: {doctor}")
                    self.mostrar_texto(observaciones)
                    encontrado = True
                    break

            if not encontrado:
                self.mostrar_texto("No hay registros disponibles para este paciente.")

        except Exception as e:
            self.mostrar_texto(f"Error al leer el archivo: {e}")

    def mostrar_texto(self, texto):
        """Muestra texto en el cuadro de texto deshabilitado."""
        self.cuadro_texto.configure(state="normal")
        self.cuadro_texto.delete("1.0", "end")
        self.cuadro_texto.insert("1.0", texto)
        self.cuadro_texto.configure(state="disabled")

    def volver(self):
        """Regresa al panel principal del paciente."""
        self.destroy()
        from pacientes.funciones import PacientePrincipal
        PacientePrincipal(self.documento_actual)

