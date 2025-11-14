import customtkinter as ctk
from ventana_base import BaseVentana
from componentes import crear_boton_regresar
from administrador.crear import CrearUsuario
from administrador.actualizar import ActualizarUsuario
from administrador.eliminar import EliminarUsuario

def abrir_admin_funciones(ventana_anterior):
    ventana_anterior.destroy()
    AdminFunciones()

class AdminFunciones(BaseVentana):
    def __init__(self):
        super().__init__("Panel del Administrador")
        crear_boton_regresar(self, self.volver)
        
        ctk.CTkLabel(self.contenido, text="Opciones del Administrador", 
                    font=("Arial", 14, "bold"), text_color="black").pack(pady=(30, 15))

        for texto, comando in [
            ("Crear Usuario", self.abrir_crear),
            ("Actualizar Usuario", self.abrir_actualizar),
            ("Eliminar Usuario", self.abrir_eliminar)
        ]:
            ctk.CTkButton(self.contenido, text=texto, width=200, height=45,
                         fg_color="#3E7CB1", hover_color="#2F5E85",
                         font=("Arial", 13, "bold"), command=comando).pack(pady=15)

        self.mainloop()

    def volver(self):
        from entrar import abrir_login
        self.destroy()
        abrir_login("Administrador", None)

    def abrir_crear(self):
        self.destroy()
        CrearUsuario()

    def abrir_actualizar(self):
        self.destroy()
        ActualizarUsuario()

    def abrir_eliminar(self):
        self.destroy()
        EliminarUsuario()