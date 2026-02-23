import requests
import concurrent.futures
import os
import time

def check_link(item):
    name, url, info = item
    # User-Agent para parecer un televisor Smart TV
    headers = {'User-Agent': 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 sb.2.2.0.31000 Safari/533.3'}
    try:
        # Usamos GET pero pedimos solo el primer byte para no saturar
        r = requests.get(url, headers=headers, timeout=5, stream=True)
        if r.status_code == 200:
            return f"{info}\n{url}\n"
    except:
        pass
    return None

def iniciar_auditoria():
    m3u_path = os.path.expanduser("~/iptv/global_jeycamon.m3u")
    if not os.path.exists(m3u_path): return

    print("[🔍] Iniciando Auditoría VIP (Modo Sigilo)...")
    canales = []
    with open(m3u_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].startswith("#EXTINF"):
                canales.append((lines[i].split(",")[-1], lines[i+1].strip(), lines[i].strip()))

    lista_viva = ["#EXTM3U\n"]
    # Bajamos los hilos a 10 para no ser baneados
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        resultados = list(executor.map(check_link, canales))
        for res in resultados:
            if res: lista_viva.append(res)

    with open(m3u_path, "w", encoding="utf-8") as f:
        f.writelines(lista_viva)
    
    print(f"[✔] Auditoría terminada. Canales estables: {len(lista_viva)-1}")

if __name__ == "__main__":
    iniciar_auditoria()
