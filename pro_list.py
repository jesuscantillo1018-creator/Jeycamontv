import requests
import os
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def el_canal_sirve(url):
    """Prueba si el link abre en menos de 2 segundos"""
    try:
        with requests.get(url, headers=headers, timeout=2.0, stream=True) as r:
            return r.status_code == 200
    except:
        return False

def limpiar_manteniendo_orden():
    if not os.path.exists("manuales.m3u"):
        print("❌ No hay canales manuales para limpiar.")
        return

    print("🧹 Limpiando canales muertos pero MANTENIENDO categorías...")
    canales_vivos = []
    
    with open("manuales.m3u", "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        if lines[i].startswith("#EXTINF"):
            info = lines[i].strip()
            url = lines[i+1].strip() if i+1 < len(lines) else ""
            
            # Extraer el nombre para mostrar en pantalla
            nombre = info.split(",")[-1]
            print(f"⚖️ Verificando: {nombre[:30]}...", end="\r")
            
            if el_canal_sirve(url):
                # Guardamos la línea completa (que ya tiene el group-title que te gusta)
                canales_vivos.append(f"{info}\n{url}\n")

    # Guardar solo los que sirven en el archivo manual
    with open("manuales.m3u", "w", encoding="utf-8") as f:
        for canal in canales_vivos:
            f.write(canal)
            
    print(f"\n✅ ¡Limpieza terminada! Se quedaron {len(canales_vivos)} canales vivos con sus categorías intactas.")

def generar_global():
    # Esta parte junta el manual limpio con los países actualizados
    print("📡 Regenerando lista global...")
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        if os.path.exists("manuales.m3u"):
            with open("manuales.m3u", "r", encoding="utf-8") as m:
                f.write(m.read())
        # Aquí puedes añadir de nuevo la descarga de países si quieres
        # que también se testeen los de Colombia, México, etc.

if __name__ == "__main__":
    limpiar_manteniendo_orden()
    generar_global()
