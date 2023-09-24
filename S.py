import socket
import random
import string
import curses
import nmap
import progressbar

# Función para escanear puertos en una dirección IP
def encontrar_camaras_en_red(ip, puertos, stdscr):
    resultados = {}
    total_puertos = len(puertos)
    
    stdscr.addstr(4, 0, f"Escaneando puertos en IP: {ip}")
    stdscr.addstr(5, 0, "Porcentaje de finalización:")
    stdscr.addstr(6, 0, "IPs escaneadas:")
    
    # Configura la barra de progreso para puertos
    bar_puertos = progressbar.ProgressBar(max_value=total_puertos, widgets=[
        progressbar.Percentage(),
        ' ', progressbar.Bar(marker='█', left='[', right=']'), ' ',
    ])
    
    stdscr.refresh()
    
    for i, puerto in enumerate(puertos):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            resultado = sock.connect_ex((ip, puerto))
            sock.close()

            if resultado == 0:
                resultados[puerto] = "Abierto"
                # Muestra la dirección IP y el puerto abierto
                stdscr.addstr(8 + i, 0, f"IP: {ip}, Puerto {puerto} abierto")
            else:
                resultados[puerto] = "Cerrado"
        except socket.error as e:
            resultados[puerto] = f"Error: {str(e)}"
        
        # Actualizar el progreso de la barra de puertos
        bar_puertos.update(i + 1)
        
        # Actualizar el porcentaje de finalización
        porcentaje_completado = int((i + 1) / total_puertos * 100)
        stdscr.addstr(5, 25, f"{porcentaje_completado}%")
        stdscr.addstr(7, 17, f"{i + 1} de {total_puertos}")
        stdscr.refresh()
    
    return resultados

# Función para escanear direcciones IP
def escanear_ips(ips, puertos, stdscr):
    resultados = {}
    total_ips = len(ips)
    
    stdscr.addstr(2, 0, "Escaneando la red local en busca de cámaras IP con puertos específicos...")
    stdscr.addstr(4, 0, "Porcentaje de finalización:")
    stdscr.addstr(6, 0, "IPs escaneadas:")
    
    # Configura la barra de progreso para IPs
    bar_ips = progressbar.ProgressBar(max_value=total_ips, widgets=[
        progressbar.Percentage(),
        ' ', progressbar.Bar(marker='█', left='[', right=']'), ' ',
    ])
    
    stdscr.refresh()
    
    for i, ip in enumerate(ips):
        stdscr.addstr(3, 0, f"Explorando IP: {ip}")
        
        # Escanear puertos en esta IP
        resultados[ip] = escanear_puertos(ip, puertos, stdscr)
        
        # Actualizar el progreso de la barra de IPs
        bar_ips.update(i + 1)
        
        # Actualizar el porcentaje de finalización
        porcentaje_completado = int((i + 1) / total_ips * 100)
        stdscr.addstr(4, 25, f"{porcentaje_completado}%")
        stdscr.addstr(6, 17, f"{i + 1} de {total_ips}")
        stdscr.refresh()
    
    return resultados

# Función principal para analizar una cámara
def analizar_camara(stdscr, ip, puertos, usuario, longitud_contraseña, archivo_credenciales):
    # ... (el código para generar credenciales y acceder al RTSP de la cámara sigue aquí)

# Función para encontrar cámaras en la red local con puertos específicos
def encontrar_camaras_en_red(puertos):
    camaras_activas = {}  # Diccionario para almacenar IP y puertos abiertos
    
    for puerto in puertos:
        scanner = nmap.PortScanner()
        
        # Escanea la red local en busca de dispositivos con el puerto especificado abierto
        scanner.scan('192.168.0.0/24', str(puerto))
        
        # Obtiene las direcciones IP de los dispositivos con el puerto abierto
        hosts = scanner.all_hosts()
        
        for host in hosts:
            if host in camaras_activas:
                camaras_activas[host].append(puerto)
            else:
                camaras_activas[host] = [puerto]
    
    return camaras_activas

# Función principal
def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    
    stdscr.addstr(0, 0, "Bienvenido al Escáner y Generador de Credenciales RTSP")
    stdscr.refresh()
    
    puertos_objetivo = [554, 2020, 443]  # Puertos que te interesan
    
    # Encontrar cámaras en la red local con puertos específicos
    camaras_en_red = encontrar_camaras_en_red(puertos_objetivo)
    
    if not camaras_en_red:
        stdscr.addstr(1, 0, "No se encontraron cámaras IP en la red local con los puertos especificados.")
        stdscr.refresh()
        stdscr.getch()
        return
    
    # Extraer las direcciones IP de las cámaras encontradas
    ips_camaras = list(camaras_en_red.keys())
    
    # Escanear las direcciones IP en busca de puertos abiertos
    resultados_ips = escanear_ips(ips_camaras, puertos_objetivo, stdscr)
    
    # Mostrar resultados
    for ip, resultados_puertos in resultados_ips.items():
        stdscr.clear()
        stdscr.addstr(0, 0, "Bienvenido al Escáner y Generador de Credenciales RTSP")
        stdscr.refresh()
        
        # Desactivar curses temporalmente
        curses.endwin()
        
        usuario = input("Ingresa el nombre de usuario (o deja en blanco para generar uno automáticamente): ").strip()
        longitud_contraseña = int(input("Ingresa la longitud de la contraseña (por defecto 12): ") or 12)
        archivo_credenciales = input("Ingresa el nombre del archivo para guardar las credenciales (o deja en blanco para no guardar): ").strip()
        
        # Reactivar curses
        curses.refresh()
        
        # Analizar cámara
        analizar_camara(stdscr, ip, puertos_objetivo, usuario, longitud_contraseña, archivo_credenciales)
        stdscr.clear()

if __name__ == "__main__":
    curses.wrapper(main)
