import customtkinter as ctk
import json
from ventana_base import BaseVentana
from componentes import crear_boton_regresar, crear_boton_buscar

class ActualizarUsuario(BaseVentana):
    def __init__(self):
        self.usuario_actual = None
        super().__init__("Actualizar Usuario")
        crear_boton_regresar(self, self.volver)
        self.crear_interfaz()
        self.mainloop()

    def crear_interfaz(self):
        # Campo de documento con botón buscar
        frame_doc = ctk.CTkFrame(self.contenido, fg_color="transparent")
        frame_doc.pack(pady=5)
        
        self.entry_doc = ctk.CTkEntry(frame_doc, placeholder_text="Número de documento", width=200)
        self.entry_doc.pack(side="left", padx=5)
        
        crear_boton_buscar(frame_doc, self.buscar_usuario)

        # Campos principales
        self.entry_nombre = ctk.CTkEntry(self.contenido, placeholder_text="Nombre completo", width=250)
        self.entry_nombre.pack(pady=5)
        
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

        # Botón actualizar
        ctk.CTkButton(self.contenido, text="Actualizar usuario", width=250,
                     fg_color="#3E7CB1", hover_color="#2F5E85",
                     command=self.actualizar_usuario).pack(pady=15)

        self.label_mensaje = ctk.CTkLabel(self.contenido, text="")
        self.label_mensaje.pack()

    def buscar_usuario(self):
        doc = self.entry_doc.get().strip()
        if not doc:
            self.mostrar_mensaje("⚠️ Ingresa un número de documento.", "red")
            return

        try:
            with open("usuarios.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.mostrar_mensaje("⚠️ No hay usuarios registrados.", "red")
            return

        for rol in data:
            for usuario in data[rol]:
                if usuario["documento"] == doc:
                    self.usuario_actual = usuario
                    self.entry_nombre.delete(0, "end")
                    self.entry_nombre.insert(0, usuario["nombre_completo"])
                    self.entry_tel.delete(0, "end")
                    self.entry_tel.insert(0, usuario["telefono"])
                    self.menu_rol.set(usuario["rol"])
                    self.entry_edad.delete(0, "end")
                    self.entry_edad.insert(0, str(usuario["edad"]))
                    self.entry_peso.delete(0, "end")
                    self.entry_peso.insert(0, str(usuario["peso"]))
                    self.mostrar_mensaje("✅ Usuario encontrado", "green")
                    return

        self.mostrar_mensaje("⚠️ Usuario no encontrado.", "red")

    def actualizar_usuario(self):
        if not self.usuario_actual:
            self.mostrar_mensaje("⚠️ Busca primero un usuario.", "red")
            return

        datos = self.obtener_datos()
        if not datos:
            return

        try:
            with open("usuarios.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.mostrar_mensaje("⚠️ No hay usuarios registrados.", "red")
            return

        for rol in data:
            for usuario in data[rol]:
                if usuario["documento"] == self.usuario_actual["documento"]:
                    usuario.update({
                        "nombre_completo": datos[0],
                        "documento": datos[1],
                        "telefono": datos[2],
                        "rol": datos[3],
                        "edad": datos[4],
                        "peso": datos[5],
                        "usuario": datos[0],
                        "contraseña": datos[1]
                    })
                    
                    with open("usuarios.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                    
                    self.mostrar_mensaje("✅ Usuario actualizado correctamente.", "green")
                    return

        self.mostrar_mensaje("⚠️ No se encontró el usuario.", "red")

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
        self.usuario_actual = None

    def volver(self):
        from administrador.admin_main import AdminFunciones
        self.destroy()
        AdminFunciones()