import customtkinter as ctk
from ventana_base import BaseVentana
from componentes import crear_boton_regresar

class PacientePrincipal(BaseVentana):
    def __init__(self, documento_paciente):
        super().__init__("Panel del Paciente")
        self.documento_paciente = documento_paciente  #uardamos el documento del paciente

        # --- Flecha de regresar ---
        crear_boton_regresar(self, self.volver)

        # --- Botón Ver examen ECG ---
        boton_examen = ctk.CTkButton(
            self.contenido,
            text="Ver examen ECG",
            width=220,
            height=45,
            corner_radius=25,
            fg_color="#3E7CB1",
            hover_color="#2F5E85",
            font=("Arial", 13, "bold"),
            command=self.ver_examen_ecg
        )
        boton_examen.pack(pady=15)

        # --- Botón Ver descripción ECG ---
        boton_descripcion = ctk.CTkButton(
            self.contenido,
            text="Ver descripción ECG",
            width=220,
            height=45,
            corner_radius=25,
            fg_color="#3E7CB1",
            hover_color="#2F5E85",
            font=("Arial", 13, "bold"),
            command=self.ver_descripcion_ecg
        )
        boton_descripcion.pack(pady=10)

        self.mainloop()

    # --- Acciones de botones ---
    def ver_examen_ecg(self):
        self.destroy()
        from pacientes.ecg_ver import PacienteVisualizarECG
        PacienteVisualizarECG(self.documento_paciente)  # 👈 Se pasa correctamente

    def ver_descripcion_ecg(self):
        self.destroy()
        from pacientes.registro_ver import PacienteRegistroECG
        PacienteRegistroECG(self.documento_paciente)

    def volver(self):
        from entrar import abrir_login
        self.destroy()
        abrir_login("Paciente", None)
