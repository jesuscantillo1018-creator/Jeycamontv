import requests

IP = "45.226.168.29"
# Diccionario para organizar por países en GitHub
SENSADO = {
    "COLOMBIA": ["Caracol_TV", "RCN_TV", "Win_Sports_Mas", "Canal_1"],
    "MEXICO": ["Las_Estrellas", "Azteca_7", "Canal_5_MX", "Imagen_TV"],
    "ARGENTINA": ["Telefe", "El_Trece", "TyC_Sports", "C5N"],
    "DEPORTES": ["ESPN_Latino", "Fox_Sports", "Directv_Sports", "Star_Plus_Live"]
}

def scan():
    with open("canales_vivos.m3u", "w") as f:
        f.write("#EXTM3U\n")
        for pais, canales in SENSADO.items():
            iconos = {"COLOMBIA": "🇨🇴", "MEXICO": "🇲🇽", "ARGENTINA": "🇦🇷", "DEPORTES": "⚽"}
            icono = iconos.get(pais, "📡")
            for c in canales:
                url = f"http://{IP}/live/{c}/playlist.m3u8"
                try:
                    r = requests.head(url, timeout=1)
                    if r.status_code == 200:
                        f.write(f'#EXTINF:-1 group-title="{icono} JEYCAMON {pais}",{c.replace("_", " ")}\n{url}\n')
                        print(f"  ✅ {icono} {c} detectado")
                except: continue

if __name__ == "__main__":
    scan()
