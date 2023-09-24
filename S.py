import socket
import nmap

# Función para escanear puertos en una dirección IP
def escanear_puertos(ip, puertos):
    resultados = {}
    for puerto in puertos:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            resultado = sock.connect_ex((ip, puerto))
            sock.close()
            
            if resultado == 0:
                resultados[puerto] = "Abierto"
            else:
                resultados[puerto] = "Cerrado"
        except socket.error as e:
            resultados[puerto] = f"Error: {str(e)}"
    return resultados

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

if __name__ == "__main__":
    puertos_objetivo = [554, 2020, 443]  # Puertos que te interesan
    
    # Encontrar cámaras en la red local con puertos específicos
    camaras_en_red = encontrar_camaras_en_red(puertos_objetivo)
    
    if not camaras_en_red:
        print("No se encontraron cámaras IP en la red local con los puertos especificados.")
    else:
        # Extraer las direcciones IP de las cámaras encontradas
        ips_camaras = list(camaras_en_red.keys())
        
        # Escanear las direcciones IP en busca de puertos abiertos
        resultados_ips = {}
        for ip in ips_camaras:
            resultados_ips[ip] = escanear_puertos(ip, puertos_objetivo)
        
        # Mostrar resultados
        for ip, resultados_puertos in resultados_ips.items():
            print(f"IP: {ip}")
            for puerto, estado in resultados_puertos.items():
                print(f"Puerto {puerto}: {estado}")
