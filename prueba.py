import json
import os
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

# === Función para cargar una señal ECG aleatoria ===
def obtener_senal_aleatoria(carpeta="ecg_jsons_grouped_keys"):
    archivos = [f for f in os.listdir(carpeta) if f.endswith(".json")]
    if not archivos:
        raise FileNotFoundError("No se encontraron archivos JSON en la carpeta.")

    archivo = random.choice(archivos)
    ruta = os.path.join(carpeta, archivo)

    with open(ruta, "r") as f:
        data = json.load(f)

    clave = random.choice(list(data.keys()))
    senal = data[clave]

    print(f"[DEBUG] Archivo: {archivo} | Clave: {clave} | Muestras: {len(senal)}")
    return senal, archivo, clave


# === Ventana principal ===
def ventana_ecg():
    ventana = ctk.CTk()
    ventana.title("Visualización de ECG")
    ventana.geometry("700x500")

    # Frame principal
    frame = ctk.CTkFrame(ventana)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Función para mostrar señal
    def mostrar_senal():
        senal, archivo, clave = obtener_senal_aleatoria()

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(senal, color='blue')
        ax.set_title(f"Señal ECG ({archivo} - {clave})")
        ax.set_xlabel("Tiempo (muestras)")
        ax.set_ylabel("Amplitud")

        # Limpiar cualquier gráfica anterior
        for widget in frame.winfo_children():
            widget.destroy()

        # Insertar el gráfico en la ventana
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # Botón para cargar nueva señal
    boton = ctk.CTkButton(
        ventana,
        text="Cargar señal ECG",
        command=mostrar_senal,
        fg_color="#3E7CB1",
        hover_color="#2F5E85",
        corner_radius=25,
        width=200,
        height=40
    )
    boton.pack(pady=10)

    ventana.mainloop()


if __name__ == "__main__":
    ventana_ecg()
