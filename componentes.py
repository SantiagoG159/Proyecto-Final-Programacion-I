import customtkinter as ctk
from PIL import Image

def crear_boton_regresar(ventana, comando, x=310, y=10):
    """
    Crea un botón de regresar estandarizado
    """
    try:
        flecha_img = ctk.CTkImage(light_image=Image.open("imagenes/flecha.png"), size=(25, 25))
        boton_regresar = ctk.CTkButton(
            ventana.label_imagen,
            image=flecha_img,
            text="",
            width=25,
            height=25,
            fg_color="transparent",
            hover_color="#D9EAF5",
            command=comando
        )
        boton_regresar.place(x=x, y=y)
        return boton_regresar
    except Exception as e:
        print(f"Error creando botón regresar: {e}")
        return None

def crear_boton_buscar(contenedor, comando):
    """
    Crea un botón de búsqueda estandarizado
    """
    try:
        lupa_img = ctk.CTkImage(light_image=Image.open("imagenes/lupa.png"), size=(20, 20))
        boton_buscar = ctk.CTkButton(
            contenedor,
            image=lupa_img,
            text="",
            width=35,
            height=30,
            fg_color="transparent",
            hover_color="#D9EAF5",
            command=comando
        )
        boton_buscar.pack(side="left", padx=5)
        return boton_buscar
    except Exception as e:
        print(f"Error creando botón buscar: {e}")
        return None