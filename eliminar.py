import customtkinter as ctk
import json
from ventana_base import BaseVentana
from componentes import crear_boton_regresar, crear_boton_buscar

class EliminarUsuario(BaseVentana):
    def __init__(self):
        self.usuario_actual = None
        super().__init__("Eliminar Usuario")
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

        # Campos de solo lectura para mostrar información
        self.entry_nombre = ctk.CTkEntry(self.contenido, placeholder_text="Nombre completo", width=250, state="readonly")
        self.entry_nombre.pack(pady=5)
        
        self.entry_tel = ctk.CTkEntry(self.contenido, placeholder_text="Teléfono", width=250, state="readonly")
        self.entry_tel.pack(pady=5)
        
        self.menu_rol = ctk.CTkOptionMenu(self.contenido, values=["doctor", "paciente"], state="disabled")
        self.menu_rol.set("Rol")
        self.menu_rol.pack(pady=5)

        # Edad y peso (solo lectura)
        frame_datos = ctk.CTkFrame(self.contenido, fg_color="transparent")
        frame_datos.pack(pady=5)
        
        self.entry_edad = ctk.CTkEntry(frame_datos, placeholder_text="Edad", width=100, state="readonly")
        self.entry_edad.pack(side="left", padx=5)
        
        self.entry_peso = ctk.CTkEntry(frame_datos, placeholder_text="Peso", width=100, state="readonly")
        self.entry_peso.pack(side="left", padx=5)

        # Botón eliminar
        ctk.CTkButton(self.contenido, text="Eliminar usuario", width=250,
                     fg_color="#FF4B4B", hover_color="#CC3C3C",
                     command=self.eliminar_usuario).pack(pady=15)

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
                    self.entry_nombre.configure(state="normal")
                    self.entry_nombre.delete(0, "end")
                    self.entry_nombre.insert(0, usuario["nombre_completo"])
                    self.entry_nombre.configure(state="readonly")
                    
                    self.entry_tel.configure(state="normal")
                    self.entry_tel.delete(0, "end")
                    self.entry_tel.insert(0, usuario["telefono"])
                    self.entry_tel.configure(state="readonly")
                    
                    self.menu_rol.set(usuario["rol"])
                    
                    self.entry_edad.configure(state="normal")
                    self.entry_edad.delete(0, "end")
                    self.entry_edad.insert(0, str(usuario["edad"]))
                    self.entry_edad.configure(state="readonly")
                    
                    self.entry_peso.configure(state="normal")
                    self.entry_peso.delete(0, "end")
                    self.entry_peso.insert(0, str(usuario["peso"]))
                    self.entry_peso.configure(state="readonly")
                    
                    self.mostrar_mensaje("✅ Usuario encontrado", "green")
                    return

        self.mostrar_mensaje("⚠️ Usuario no encontrado.", "red")

    def eliminar_usuario(self):
        if not self.usuario_actual:
            self.mostrar_mensaje("⚠️ Busca primero un usuario.", "red")
            return

        ventana_confirmar = ctk.CTkToplevel(self)
        ventana_confirmar.title("Confirmar eliminación")
        ventana_confirmar.geometry("300x150")
        ventana_confirmar.resizable(False, False)
        ventana_confirmar.grab_set()

        ctk.CTkLabel(ventana_confirmar, text="¿Estás seguro de eliminar este usuario?", 
                    font=("Arial", 12), text_color="black").pack(pady=(25, 15))

        frame_botones = ctk.CTkFrame(ventana_confirmar, fg_color="transparent")
        frame_botones.pack(pady=10)

        ctk.CTkButton(frame_botones, text="Sí", width=80, fg_color="#FF4B4B",
                     command=lambda: self.confirmar_eliminar(ventana_confirmar)).pack(side="left", padx=10)
        
        ctk.CTkButton(frame_botones, text="No", width=80, fg_color="gray",
                     command=ventana_confirmar.destroy).pack(side="left", padx=10)

    def confirmar_eliminar(self, ventana):
        try:
            with open("usuarios.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.mostrar_mensaje("⚠️ No hay usuarios registrados.", "red")
            ventana.destroy()
            return

        for rol in data:
            for usuario in data[rol]:
                if usuario["documento"] == self.usuario_actual["documento"]:
                    data[rol].remove(usuario)
                    
                    with open("usuarios.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                    
                    self.mostrar_mensaje("✅ Usuario eliminado correctamente.", "green")
                    self.limpiar_campos()
                    ventana.destroy()
                    return

        self.mostrar_mensaje("⚠️ Usuario no encontrado.", "red")
        ventana.destroy()

    def mostrar_mensaje(self, texto, color):
        self.label_mensaje.configure(text=texto, text_color=color)

    def limpiar_campos(self):
        for entry in [self.entry_nombre, self.entry_doc, self.entry_tel, self.entry_edad, self.entry_peso]:
            entry.configure(state="normal")
            entry.delete(0, "end")
            if entry != self.entry_doc:
                entry.configure(state="readonly")
        
        self.menu_rol.set("Rol")
        self.usuario_actual = None

    def volver(self):
        from administrador.admin_main import AdminFunciones
        self.destroy()
        AdminFunciones()