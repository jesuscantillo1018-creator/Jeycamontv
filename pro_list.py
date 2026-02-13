import requests
import os
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def el_canal_sirve(url):
    try:
        with requests.get(url, headers=headers, timeout=2.0, stream=True) as r:
            return r.status_code == 200
    except:
        return False

def agregar_links():
    while True:
        res = input("\n➕ ¿Quieres añadir un link nuevo para TESTEAR? (s/n): ").lower()
        if res == 's':
            u = input("🔗 Pega el Link RAW: ").strip()
            n = input("🏷️ Nombre de Categoría (Enter para mantener original): ").strip().upper()
            print(f"⏳ Verificando canales... esto será rápido.")
            try:
                r = requests.get(u, headers=headers, timeout=10)
                if r.status_code == 200:
                    with open("manuales.m3u", "a", encoding="utf-8") as f:
                        lines = r.text.splitlines()
                        for i in range(len(lines)):
                            if lines[i].startswith("#EXTINF"):
                                info, v_url = lines[i], lines[i+1].strip() if i+1 < len(lines) else ""
                                if el_canal_sirve(v_url):
                                    if n:
                                        info = re.sub(r'group-title="[^"]*"', '', info)
                                        info = info.replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{n}"')
                                    f.write(info + "\n" + v_url + "\n")
                print(f"✅ Proceso de añadido terminado.")
            except: print("❌ Error con el link.")
        else: break

def limpieza_profunda():
    if not os.path.exists("manuales.m3u"): return
    print("\n🧹 Iniciando limpieza profunda de lo que ya tienes guardado...")
    vivos = []
    with open("manuales.m3u", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for i in range(0, len(lines), 2):
        if i+1 < len(lines) and lines[i].startswith("#EXTINF"):
            info, url = lines[i].strip(), lines[i+1].strip()
            print(f"⚖️ Verificando: {info.split(',')[-1][:25]}...", end="\r")
            if el_canal_sirve(url):
                vivos.append(f"{info}\n{url}\n")
    
    with open("manuales.m3u", "w", encoding="utf-8") as f:
        f.writelines(vivos)
    print(f"\n✅ Limpieza terminada. Quedaron {len(vivos)} canales vivos.")

def generar_global():
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        if os.path.exists("manuales.m3u"):
            with open("manuales.m3u", "r", encoding="utf-8") as m:
                f.write(m.read())
    print("🚀 global_jeycamon.m3u actualizado.")

if __name__ == "__main__":
    agregar_links()
    limpiar = input("\n🧹 ¿Quieres hacer una limpieza profunda de TODA tu lista guardada? (s/n): ").lower()
    if limpiar == 's':
        limpieza_profunda()
    generar_global()
