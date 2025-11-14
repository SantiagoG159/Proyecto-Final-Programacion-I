from pacientes.funciones import PacientePrincipal

def abrir_paciente_funcion(ventana_anterior, documento):
    """
    Cierra la ventana anterior e inicia la ventana principal del paciente.
    """
    ventana_anterior.destroy()
    PacientePrincipal(documento)
