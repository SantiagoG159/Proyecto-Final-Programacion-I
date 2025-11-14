import customtkinter as ctk
from doctor.buscar import DoctorBuscarPaciente

def abrir_doctor_funcion(ventana_anterior):
    """
    Cierra la ventana anterior e inicia la ventana principal del doctor.
    """
    ventana_anterior.destroy()
    DoctorBuscarPaciente()