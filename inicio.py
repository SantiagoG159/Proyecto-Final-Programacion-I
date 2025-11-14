import customtkinter as ctk
from PIL import Image
from ventana_base import BaseVentana  # ventana base reutilizable
from entrar import abrir_login        # login de usuarios
from componentes import crear_boton_regresar  # botón reutilizable de regreso


def ventana_inicio():
    inicio = BaseVentana("Clínica ECG")

    # --- Logo central ---
    logo = ctk.CTkImage(light_image=Image.open("imagenes/logoo.png"), size=(200, 100))
    label_logo = ctk.CTkLabel(inicio.contenido, image=logo, text="")
    label_logo.pack(pady=(20, 10))

    texto_bienvenida = ctk.CTkLabel(
        inicio.contenido,
        text="Bienvenido a tu clínica de confianza",
        font=("Arial", 14),
        text_color="black"
    )
    texto_bienvenida.pack(pady=(10, 25))

    boton_ingresar = ctk.CTkButton(
        inicio.contenido,
        text="Ingresar",
        width=200,
        height=45,
        corner_radius=25,
        fg_color="#3E7CB1",
        hover_color="#2F5E85",
        font=("Arial", 13, "bold"),
        command=lambda: abrir_seleccion(inicio)
    )
    boton_ingresar.pack(pady=(0, 20))

    frame_registro = ctk.CTkFrame(inicio.contenido, fg_color="white")
    frame_registro.pack(pady=(10, 0))

    texto_registro = ctk.CTkLabel(
        frame_registro,
        text="¿Aún no tienes una cuenta? ",
        font=("Arial", 11),
        text_color="black"
    )
    texto_registro.pack(side="left")

    enlace_registro = ctk.CTkLabel(
        frame_registro,
        text="Regístrate aquí",
        font=("Arial", 11, "bold"),
        text_color="#007ACC",
        cursor="hand2"
    )
    enlace_registro.pack(side="left", padx=(3, 0))

    label_legal = ctk.CTkLabel(
        inicio.contenido,
        text="Al registrarte aceptas nuestros Términos y Condiciones,\ny nuestra Política de Privacidad.",
        font=("Arial", 8),
        text_color="gray"
    )
    label_legal.pack(side="bottom", pady=10)

    inicio.mainloop()


def abrir_seleccion(ventana_anterior=None):
    # Cerrar la ventana anterior si existe
    if ventana_anterior:
        ventana_anterior.destroy()

    seleccion = BaseVentana("Seleccionar Rol")

    # --- Botón de regresar ---
    crear_boton_regresar(seleccion, lambda: volver_inicio(seleccion))

    # --- Título ---
    ctk.CTkLabel(
        seleccion.contenido,
        text="Selecciona tu rol para continuar:",
        font=("Arial", 13),
        text_color="black"
    ).pack(pady=(30, 15))

    # --- Botones de roles ---
    roles = [
        ("Administrador", "#3E7CB1"),
        ("Doctor", "#3E7CB1"),
        ("Paciente", "#3E7CB1")
    ]

    for rol, color in roles:
        boton = ctk.CTkButton(
            seleccion.contenido,
            text=rol,
            width=200,
            height=45,
            corner_radius=25,
            fg_color=color,
            hover_color="#2F5E85",
            font=("Arial", 13, "bold"),
            command=lambda r=rol: abrir_login(r, seleccion)
        )
        boton.pack(pady=15)

    label_legal = ctk.CTkLabel(
        seleccion.contenido,
        text="Al registrarte aceptas nuestros Términos y Condiciones,\ny nuestra Política de Privacidad.",
        font=("Arial", 8),
        text_color="gray"
    )
    label_legal.pack(side="bottom", pady=10)

    seleccion.mainloop()


def volver_inicio(ventana_actual):
    ventana_actual.destroy()
    ventana_inicio()


if __name__ == "__main__":
    ventana_inicio()
