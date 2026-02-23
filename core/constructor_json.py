import json
import os

def m3u_to_jey_json():
    m3u_path = os.path.expanduser("~/iptv/global_jeycamon.m3u")
    json_path = os.path.expanduser("~/iptv/jeycamon.json")
    
    if not os.path.exists(m3u_path): return

    lista_final = {"n_canales": 0, "categorias": [], "streams": []}
    categorias_set = set()
    
    with open(m3u_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    for i in range(len(lines)):
        if lines[i].startswith("#EXTINF"):
            info = lines[i]
            url = lines[i+1].strip() if (i+1) < len(lines) else ""
            nombre = info.split(",")[-1].strip()
            
            # Extraer grupo del tag group-title
            grupo = "VARIADOS"
            if 'group-title="' in info:
                grupo = info.split('group-title="')[1].split('"')[0].upper()
            
            categorias_set.add(grupo)
            lista_final["streams"].append({
                "name": nombre,
                "url": url,
                "group": grupo
            })
            lista_final["n_canales"] += 1

    lista_final["categorias"] = sorted(list(categorias_set))
    
    with open(json_path, "w", encoding="utf-8") as j:
        json.dump(lista_final, j, indent=4, ensure_ascii=False)
    
    print(f"[✔] JSON Estructurado: {lista_final['n_canales']} canales en {len(lista_final['categorias'])} categorías.")

if __name__ == "__main__":
    m3u_to_jey_json()
