import os
import subprocess
from datetime import datetime

# --- CONFIGURACIÓN ---
BASE_DIR = os.path.expanduser("~/iptv")
GLOBAL_M3U = os.path.join(BASE_DIR, "global_jeycamon.m3u")
# Aquí definimos los archivos que encontró tu escaneo Shodan
VOD_FILES = [
    {"nombre": "Estreno Rescatado M1", "url": "https://TU_SERVIDOR_IPTV/vod/m1.m3u8"},
    {"nombre": "Estreno Rescatado M2", "url": "https://TU_SERVIDOR_IPTV/vod/m2.m3u8"},
    {"nombre": "Serie Rescatada T1", "url": "https://TU_SERVIDOR_IPTV/vod/t1.m3u8"}
]

def integrar():
    print("\n🚀 INTEGRANDO VOD RESCATADOS A LA SUITE...")
    
    if not os.path.exists(GLOBAL_M3U):
        print("[!] No se encontró global_jeycamon.m3u. Creando uno nuevo...")
        with open(GLOBAL_M3U, "w") as f: f.write("#EXTM3U\n")

    # Escribir los nuevos VOD al final del archivo
    with open(GLOBAL_M3U, "a", encoding="utf-8") as f:
        for vod in VOD_FILES:
            # Reemplaza TU_SERVIDOR_IPTV por la IP o dominio donde encontraste los archivos
            f.write(f'#EXTINF:-1 group-title="JEYCAMON VOD",{vod["nombre"]}\n')
            f.write(f'{vod["url"]}\n')

    print(f"[✅] Se añadieron {len(VOD_FILES)} contenidos VOD.")

    # Subida automática a GitHub
    try:
        os.chdir(BASE_DIR)
        subprocess.run(["git", "add", "global_jeycamon.m3u"], check=True)
        subprocess.run(["git", "commit", "-m", f"Add VOD Rescatados - {datetime.now().strftime('%H:%M')}"], check=True)
        subprocess.run(["git", "push", "origin", "maestro"], check=True)
        print("[🚀] ¡Lista actualizada con películas en GitHub!")
    except Exception as e:
        print(f"[!] Error al subir: {e}")

if __name__ == "__main__":
    integrar()
