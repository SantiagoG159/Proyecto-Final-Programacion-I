import customtkinter as ctk
import json
from ventana_base import BaseVentana
from componentes import crear_boton_regresar


# --- FUNCIÓN PARA ABRIR LOGIN ---
def abrir_login(rol, ventana_anterior):
    ventana_anterior.destroy()
    LoginVentana(rol)


# --- CLASE LOGIN ---
class LoginVentana(BaseVentana):
    def __init__(self, rol):
        super().__init__(f"Iniciar sesión - {rol.capitalize()}")
        self.rol = rol.lower()
        self.mostrar_contrasena = False

        self.crear_interfaz()
        self.mainloop()

    def crear_interfaz(self):
        """Crea toda la interfaz del login"""
        # Botón regresar reutilizable
        crear_boton_regresar(self, self.volver, x=10, y=10)

        # Campos del formulario
        self.crear_campos_login()

        # Botón de inicio de sesión
        boton_login = ctk.CTkButton(
            self.contenido,
            text="Inicia sesión",
            width=200,
            height=45,
            corner_radius=25,
            fg_color="#3E7CB1",
            hover_color="#2F5E85",
            font=("Arial", 13, "bold"),
            command=self.validar_login
        )
        boton_login.pack(pady=(20, 20))

        # Texto inferior
        self.crear_texto_inferior()

    def crear_campos_login(self):
        """Crea los campos de usuario y contraseña"""
        # Usuario
        ctk.CTkLabel(
            self.contenido, text="Escribe tu usuario",
            font=("Arial", 12), text_color="black"
        ).pack(pady=(20, 5))

        self.entry_usuario = ctk.CTkEntry(
            self.contenido, placeholder_text="Usuario", width=230, height=35
        )
        self.entry_usuario.pack(pady=(0, 10))

        # Mensaje dinámico
        self.label_mensaje = ctk.CTkLabel(
            self.contenido, text="", font=("Arial", 11), text_color="red"
        )
        self.label_mensaje.pack()

        # Contraseña
        ctk.CTkLabel(
            self.contenido, text="Contraseña",
            font=("Arial", 12), text_color="black"
        ).pack(pady=(15, 5))

        self.entry_contrasena = ctk.CTkEntry(
            self.contenido, placeholder_text="Contraseña",
            show="*", width=230, height=35
        )
        self.entry_contrasena.pack(pady=(0, 10))

        # Botón mostrar/ocultar contraseña
        self.boton_ver = ctk.CTkButton(
            self.contenido, text="👁", width=35, height=30,
            fg_color="transparent", text_color="gray",
            command=self.toggle_contrasena
        )
        self.boton_ver.place(x=295, y=275)

    def crear_texto_inferior(self):
        """Texto inferior del login"""
        ctk.CTkLabel(
            self.contenido,
            text="¿Aún no tienes una cuenta?",
            font=("Arial", 11), text_color="black"
        ).pack()

        ctk.CTkLabel(
            self.contenido,
            text="Regístrate aquí",
            font=("Arial", 11, "bold"),
            text_color="#007ACC",
            cursor="hand2"
        ).pack()

        ctk.CTkLabel(
            self.contenido,
            text="Al registrarte aceptas nuestros Términos y Condiciones,\n"
                 "y nuestra Política de Privacidad.",
            font=("Arial", 8), text_color="gray"
        ).pack(side="bottom", pady=10)

    def toggle_contrasena(self):
        """Alterna entre mostrar y ocultar contraseña"""
        self.mostrar_contrasena = not self.mostrar_contrasena
        self.entry_contrasena.configure(show="" if self.mostrar_contrasena else "*")

    # --- VALIDAR LOGIN ---
    def validar_login(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not usuario or not contrasena:
            self.mostrar_mensaje("Por favor llena todos los campos.", "red")
            return

        if self.rol in ["administrador", "doctor"]:
            self.login_usuario(usuario, contrasena)
        elif self.rol == "paciente":
            self.login_paciente(usuario, contrasena)

    def login_usuario(self, usuario, contrasena):
        """Login para doctor o administrador"""
        try:
            with open("usuarios.json", "r", encoding="utf-8") as archivo:
                data = json.load(archivo)
        except FileNotFoundError:
            self.mostrar_mensaje("No se encontró el archivo de usuarios.", "red")
            return

        usuarios_rol = data.get(self.rol, [])
        for u in usuarios_rol:
            if u["usuario"].lower() == usuario.lower() and u["contraseña"] == contrasena:
                self.mostrar_mensaje("Inicio de sesión exitoso ✅", "green")
                self.redirigir_panel()
                return

        self.mostrar_mensaje("Usuario o contraseña incorrectos.", "red")

    def login_paciente(self, usuario, contrasena):
        """Login para paciente: usuario = nombre, contraseña = documento"""
        try:
            with open("doc_regis.json", "r", encoding="utf-8") as archivo:
                pacientes = json.load(archivo)
        except FileNotFoundError:
            self.mostrar_mensaje("No se encontró el registro de pacientes.", "red")
            return

        for p in pacientes:
            if p["nombre_paciente"].lower() == usuario.lower() and p["documento_paciente"] == contrasena:
                self.mostrar_mensaje("Inicio de sesión exitoso ✅", "green")
                self.redirigir_panel(p["documento_paciente"])
                return

        self.mostrar_mensaje("Usuario o contraseña incorrectos.", "red")

    def mostrar_mensaje(self, texto, color):
        """Actualiza el mensaje de error o éxito"""
        self.label_mensaje.configure(text=texto, text_color=color)

    def redirigir_panel(self, documento=None):
        """Redirige al panel correcto según el rol"""
        if self.rol == "administrador":
            from administrador.admin_main import abrir_admin_funciones
            abrir_admin_funciones(self)

        elif self.rol == "doctor":
            from doctor.doctor_main import abrir_doctor_funcion
            abrir_doctor_funcion(self)

        elif self.rol == "paciente" and documento:
            from pacientes.paciente_main import abrir_paciente_funcion
            abrir_paciente_funcion(self, documento)

    def volver(self):
        """Vuelve al menú de selección de rol"""
        from inicio import abrir_seleccion
        self.destroy()
        abrir_seleccion()

