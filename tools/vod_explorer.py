import requests
import re
import os
from urllib.parse import urljoin

def extraer_recursivo(url_base, categoria, lista_enlaces):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url_base, headers=headers, timeout=10)
        # 1. Buscar archivos de video
        videos = re.findall(r'href="([^"]+\.(mp4|mkv|ts|m3u8|avi))"', r.text)
        for vid in videos:
            full_url = urljoin(url_base, vid[0])
            nombre = vid[0].replace("%20", " ").split('/')[-1]
            lista_enlaces.append({"name": nombre, "url": full_url})
            print(f"[+] Encontrado: {nombre}")

        # 2. Buscar subcarpetas (terminan en / y no son el directorio padre)
        carpetas = re.findall(r'href="([^"\/]+\/)"', r.text)
        for carpeta in carpetas:
            if carpeta not in ['../', './']:
                nueva_url = urljoin(url_base, carpeta)
                extraer_recursivo(nueva_url, categoria, lista_enlaces)
    except:
        pass

def iniciar_escaneo():
    base_url = "http://64.23.147.53:9000/"
    secciones = ["vod/", "iptv-manager/"]
    output_path = os.path.expanduser("~/iptv/listas_raw/shodan_deep_vod.m3u")
    
    resultados = []
    print("="*45)
    print("🔍 INICIANDO ESCANEO DE PROFUNDIDAD (SHODAN)")
    print("="*45)

    for sec in secciones:
        print(f"[*] Entrando a: {sec}")
        extraer_recursivo(base_url + sec, sec, resultados)

    if resultados:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for res in resultados:
                f.write(f'#EXTINF:-1 group-title="SHODAN_VOD",{res["name"]}\n')
                f.write(f'{res["url"]}\n')
        print(f"\n[✔] ¡LISTO! Se rescataron {len(resultados)} archivos de video.")
    else:
        print("\n[!] El servidor parece estar vacío o protegido por indexado.")

if __name__ == "__main__":
    iniciar_escaneo()
