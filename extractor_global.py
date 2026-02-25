import subprocess, os, re

# Forzamos tu configuración guardada para evitar errores de conexión
os.environ['OPENSSL_CONF'] = os.path.expanduser("~/UnibanProject/openssl_legacy.cnf")

fuentes = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/co.m3u",
    "https://raw.githubusercontent.com/jeycamon/iptv/maestro/global_jeycamon.m3u",
    "https://iptv-org.github.io/iptv/languages/spa.m3u"
]

def extraer():
    print("[🌪️] Iniciando ASPIRADORA PROFESIONAL (Modo Legacy SSL)...")
    total_links = []
    for url in fuentes:
        try:
            # Usamos curl con el SSL legacy para saltar bloqueos
            result = subprocess.run(["curl", "-sL", url], capture_output=True, text=True)
            links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', result.stdout)
            if links:
                total_links.extend(links)
                print(f"[✅] Éxito: {len(links)} links capturados de: {url.split('/')[-1]}")
            else:
                print(f"[⚠️] Fuente vacía o bloqueada: {url.split('/')[-1]}")
        except:
            print(f"[❌] Error crítico en fuente: {url}")
    
    with open("raw_captura.txt", "w") as f:
        for link in set(total_links):
            f.write(link + "\n")
    print(f"\n[💎] TOTAL: {len(set(total_links))} links listos para el Script Jeycamon.")

if __name__ == "__main__":
    extraer()
