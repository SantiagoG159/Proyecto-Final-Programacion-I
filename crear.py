import customtkinter as ctk
import json
from ventana_base import BaseVentana
from componentes import crear_boton_regresar

class CrearUsuario(BaseVentana):
    def __init__(self):
        super().__init__("Registrar Usuario")
        crear_boton_regresar(self, self.volver)
        self.crear_interfaz()
        self.mainloop()

    def crear_interfaz(self):
        # Campos del formulario
        self.entry_nombre = ctk.CTkEntry(self.contenido, placeholder_text="Nombre completo", width=250)
        self.entry_nombre.pack(pady=5)
        
        self.entry_doc = ctk.CTkEntry(self.contenido, placeholder_text="Número de documento", width=250)
        self.entry_doc.pack(pady=5)
        
        self.entry_tel = ctk.CTkEntry(self.contenido, placeholder_text="Teléfono", width=250)
        self.entry_tel.pack(pady=5)
        
        self.menu_rol = ctk.CTkOptionMenu(self.contenido, values=["doctor", "paciente"])
        self.menu_rol.set("Rol")
        self.menu_rol.pack(pady=5)

        # Edad y peso
        frame_datos = ctk.CTkFrame(self.contenido, fg_color="transparent")
        frame_datos.pack(pady=5)
        
        self.entry_edad = ctk.CTkEntry(frame_datos, placeholder_text="Edad", width=100)
        self.entry_edad.pack(side="left", padx=5)
        
        self.entry_peso = ctk.CTkEntry(frame_datos, placeholder_text="Peso", width=100)
        self.entry_peso.pack(side="left", padx=5)

        # Botón registrar
        ctk.CTkButton(self.contenido, text="Registrar usuario", width=250,
                     fg_color="#3E7CB1", hover_color="#2F5E85",
                     command=self.crear_usuario).pack(pady=15)

        self.label_mensaje = ctk.CTkLabel(self.contenido, text="")
        self.label_mensaje.pack()

    def crear_usuario(self):
        datos = self.obtener_datos()
        if not datos:
            return

        nombre, doc, tel, rol, edad, peso = datos

        try:
            with open("usuarios.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"administrador": [], "doctor": [], "paciente": []}

        # Verificar duplicado
        for usuario in data[rol]:
            if usuario["documento"] == doc:
                self.mostrar_mensaje("⚠️ Ya existe un usuario con ese documento.", "red")
                return

        data[rol].append({
            "nombre_completo": nombre,
            "documento": doc,
            "telefono": tel,
            "rol": rol,
            "edad": edad,
            "peso": peso,
            "usuario": nombre,
            "contraseña": doc
        })

        with open("usuarios.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        self.mostrar_mensaje("✅ Usuario registrado correctamente.", "green")
        self.limpiar_campos()

    def obtener_datos(self):
        campos = [
            self.entry_nombre.get().strip(),
            self.entry_doc.get().strip(),
            self.entry_tel.get().strip(),
            self.menu_rol.get().strip().lower(),
            self.entry_edad.get().strip(),
            self.entry_peso.get().strip()
        ]

        if not all(campos[:3]) or campos[3] == "rol" or not campos[4] or not campos[5]:
            self.mostrar_mensaje("⚠️ Todos los campos son obligatorios.", "red")
            return None

        try:
            return [campos[0], campos[1], campos[2], campos[3], int(campos[4]), float(campos[5])]
        except ValueError:
            self.mostrar_mensaje("⚠️ Edad y peso deben ser numéricos.", "red")
            return None

    def mostrar_mensaje(self, texto, color):
        self.label_mensaje.configure(text=texto, text_color=color)

    def limpiar_campos(self):
        for entry in [self.entry_nombre, self.entry_doc, self.entry_tel, self.entry_edad, self.entry_peso]:
            entry.delete(0, "end")
        self.menu_rol.set("Rol")

    def volver(self):
        from administrador.admin_main import AdminFunciones
        self.destroy()
        AdminFunciones()