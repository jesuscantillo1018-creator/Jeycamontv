import requests
import os
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Connection': 'keep-alive'
}

def el_canal_sirve(url):
    try:
        with requests.get(url, headers=headers, timeout=2.5, stream=True) as r:
            return r.status_code == 200
    except:
        return False

def agregar_links():
    while True:
        res = input("\n➕ ¿Añadir link nuevo para testear? (s/n): ").lower()
        if res == 's':
            u = input("🔗 Link RAW: ").strip()
            n = input("🏷️ Categoría Forzada (Enter para mantener original): ").strip().upper()
            print(f"⏳ Conectando y analizando fuente...")
            try:
                r = requests.get(u, headers=headers, timeout=15)
                if r.status_code == 200:
                    vivos = 0
                    muertos = 0
                    # Usamos splitlines para manejar cualquier tipo de salto de línea (\n o \r\n)
                    lines = r.text.splitlines()
                    total_lines = len(lines)
                    print(f"📄 Archivo recibido ({total_lines} líneas). Iniciando testeo...\n")
                    
                    with open("manuales.m3u", "a", encoding="utf-8") as f:
                        for i in range(total_lines):
                            line = lines[i].strip()
                            if line.startswith("#EXTINF"):
                                info = line
                                # Buscamos la URL en la siguiente línea que no esté vacía
                                v_url = ""
                                for j in range(i + 1, min(i + 5, total_lines)):
                                    next_line = lines[j].strip()
                                    if next_line and not next_line.startswith("#"):
                                        v_url = next_line
                                        break
                                
                                if v_url:
                                    nombre_canal = info.split(',')[-1] if ',' in info else "Canal sin nombre"
                                    if el_canal_sirve(v_url):
                                        print(f"  ✅ {nombre_canal[:35]}")
                                        if n:
                                            info = re.sub(r'group-title="[^"]*"', '', info)
                                            info = info.replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{n}"')
                                        f.write(info + "\n" + v_url + "\n")
                                        vivos += 1
                                    else:
                                        print(f"  ❌ {nombre_canal[:35]}")
                                        muertos += 1
                    print(f"\n📊 RESUMEN: {vivos} vivos / {muertos} muertos.")
                else:
                    print(f"❌ Error HTTP: {r.status_code}")
            except Exception as e:
                print(f"❌ Error: {e}")
        else: break

def limpieza_profunda():
    if not os.path.exists("manuales.m3u"): return
    print("\n🧹 Iniciando limpieza de base de datos local...")
    vivos_lista = []
    with open("manuales.m3u", "r", encoding="utf-8") as f:
        lines = f.readlines()
    for i in range(0, len(lines), 2):
        if i+1 < len(lines) and lines[i].startswith("#EXTINF"):
            info, url = lines[i].strip(), lines[i+1].strip()
            if el_canal_sirve(url):
                print(f"  ✅ MANTENIDO: {info.split(',')[-1][:30]}")
                vivos_lista.append(f"{info}\n{url}\n")
            else:
                print(f"  🗑️ ELIMINADO: {info.split(',')[-1][:30]}")
    with open("manuales.m3u", "w", encoding="utf-8") as f:
        f.writelines(vivos_lista)

def generar_global():
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        if os.path.exists("manuales.m3u"):
            with open("manuales.m3u", "r", encoding="utf-8") as m:
                f.write(m.read())
    print("🚀 Archivo global_jeycamon.m3u actualizado.")

if __name__ == "__main__":
    agregar_links()
    limpiar = input("\n🧹 ¿Limpieza profunda? (s/n): ").lower()
    if limpiar == 's': limpieza_profunda()
    generar_global()
