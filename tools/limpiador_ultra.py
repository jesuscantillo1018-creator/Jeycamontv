import requests
import re
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# --- CONFIGURACIÓN ---
URL_RAW = "https://raw.githubusercontent.com/jesuscantillo1018-creator/Jeycamontv/maestro/global_jeycamon.m3u"
BASE_DIR = os.path.expanduser("~/iptv")
OUTPUT_FILE = os.path.join(BASE_DIR, "global_jeycamon.m3u")

# User-Agent y Referer para saltar bloqueos de región/servidor
UA_PRO = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
REF_PRO = "https://vaughn.live/" # Referencia común para canales 24/7

def verificar_canal(bloque):
    info, url = bloque
    # Añadimos parámetros de cabecera que Smarters puede interpretar
    headers = {'User-Agent': UA_PRO, 'Referer': REF_PRO}
    try:
        response = requests.get(url, headers=headers, timeout=5, stream=True, allow_redirects=True)
        if response.status_code == 200:
            info_limpia = re.sub(r'\[.*?\]|\(.*?\)|\*.*?\*', '', info).strip()
            # Inyectamos UA y Referer en el M3U
            info_fix = info_limpia.replace('#EXTINF:', f'#EXTINF: user-agent="{UA_PRO}" referer="{REF_PRO}"')
            nombre_solo = info_limpia.split(',')[-1].strip().upper()
            return {"info": info_fix, "url": url, "nombre": nombre_solo}
    except:
        pass
    return None

def procesar():
    print("\n[🛡️] APLICANDO FIX DE REFERENCIA (REFERER) + UA")
    r = requests.get(URL_RAW, timeout=15)
    bloques = re.findall(r'(#EXTINF:.*?)\n(http.*?)(?=\n#EXTINF|$)', r.text, re.DOTALL)
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        vivos = [r for r in list(executor.map(verificar_canal, bloques)) if r]
    
    # Filtro duplicados
    finales = []
    urls_vistas = set()
    for canal in vivos:
        if canal['url'] not in urls_vistas:
            finales.append(f"{canal['info']}\n{canal['url']}\n")
            urls_vistas.add(canal['url'])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for c in finales: f.write(c)

    # Subida forzada
    os.chdir(BASE_DIR)
    subprocess.run(["git", "add", "."], shell=True)
    subprocess.run(['git', 'commit', '-m', 'Fix Referer 24/7'], shell=True)
    subprocess.run(["git", "push", "origin", "maestro"], shell=True)
    print("\n[✅] TODO LISTO. Prueba en Smarters con VPN en Latam si falla.")

if __name__ == "__main__":
    procesar()
