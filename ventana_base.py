import customtkinter as ctk
from PIL import Image

class BaseVentana(ctk.CTk):
    def __init__(self, titulo):
        super().__init__()
        self.title(titulo)
        self.geometry("360x700")
        self.resizable(False, False)
        self.configure(fg_color="white")

        # Imagen superior azul (común para todas las ventanas)
        self.imagen_superior = ctk.CTkImage(
            light_image=Image.open("imagenes/fondo.png"),  # ya no se pasa como parámetro
            size=(360, 250)
        )
        self.label_imagen = ctk.CTkLabel(self, image=self.imagen_superior, text="")
        self.label_imagen.pack(pady=0)

        # Frame donde se colocará el contenido personalizado
        self.contenido = ctk.CTkFrame(self, fg_color="white")
        self.contenido.pack(fill="both", expand=True, pady=(0, 10))
