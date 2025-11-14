import customtkinter as ctk
import json
from ventana_base import BaseVentana
from componentes import crear_boton_regresar

class DoctorRegistroECG(BaseVentana):
    def __init__(self, nombre_paciente, documento_paciente, señal_ecg):
        super().__init__("Generar Registro")
        
        self.nombre_paciente = nombre_paciente
        self.documento_paciente = documento_paciente
        self.nombre_doctor = "Doctor"  # Cambiar por nombre real

        crear_boton_regresar(self, self.volver)

        # Información del paciente
        ctk.CTkLabel(self.contenido, text=f"Paciente: {nombre_paciente}", font=("Arial", 14, "bold"), text_color="black").pack(pady=10)
        ctk.CTkLabel(self.contenido, text=f"CC. {documento_paciente}", font=("Arial", 12), text_color="black").pack(pady=5)

        # Área de texto
        self.texto_obs = ctk.CTkTextbox(self.contenido, width=320, height=150, font=("Arial", 11))
        self.texto_obs.pack(pady=10)

        # Botón Guardar
        ctk.CTkButton(self.contenido, text="Guardar", width=200, height=40, fg_color="#3E7CB1", command=self.guardar).pack(pady=10)

        self.mainloop()

    def guardar(self):
        observaciones = self.texto_obs.get("1.0", "end-1c").strip()
        
        if not observaciones:
            return

        registro = {
            "documento_paciente": self.documento_paciente,
            "nombre_paciente": self.nombre_paciente,
            "observaciones": observaciones,
            "doctor": self.nombre_doctor
        }

        try:
            # Leer datos existentes
            try:
                with open("doc_regis.json", "r", encoding="utf-8") as f:
                    datos = json.load(f)
            except:
                datos = []
            
            # Agregar y guardar
            datos.append(registro)
            with open("doc_regis.json", "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            
            # Cerrar ventana después de guardar
            self.volver()
            
        except Exception as e:
            print(f"Error: {e}")

    def volver(self):
        self.destroy()
        from doctor.visualizar import DoctorVisualizarECG
        DoctorVisualizarECG(self.nombre_paciente, self.documento_paciente)