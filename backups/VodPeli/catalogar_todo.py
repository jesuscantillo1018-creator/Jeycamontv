import requests
import re

IP = "45.226.168.29"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Mapa de lo que vamos a buscar
MAPA_CONTENIDO = {
    "Anime": ["DragonBallSuper", "OnePiece", "Naruto"],
    "Novelas": ["BettyLaFea", "PasionDeGavilanes"],
    "Hentai": ["Hentai_Sample", "Classic_H"],
    "4K": ["Avatar2", "TopGunMaverick"],
    "Deporte": ["UFC_300", "F1_Highlights"],
    # CANALES EN VIVO (Se buscan diferente)
    "live": [
        "WinSports", "WinSportsMas", "ESPN", "ESPN2", "FoxSports", 
        "StarPlus", "DirecTV_Sports", "Caracol_TV", "RCN_TV"
    ]
}

def buscar_en_carpeta(carpeta, nombre, f):
    # Definir etiquetas y grupos
    if carpeta == "live":
        icono, grupo = "📡", "⚡ JEYCAMON TV EN VIVO"
    else:
        iconos = {"Anime": "🧧", "Novelas": "💃", "Hentai": "🔞", "Deporte": "⚽", "4K": "💎"}
        icono = iconos.get(carpeta, "📂")
        grupo = f"{icono} JEYCAMON {carpeta.upper()}"

    print(f"{icono} Buscando en {carpeta} -> {nombre}...")
    encontrados = 0

    # --- LÓGICA PARA CANALES EN VIVO ---
    if carpeta == "live":
        # Formatos comunes de Wowza para streaming en vivo
        formatos_live = [
            f"http://{IP}:1935/live/{nombre}/playlist.m3u8",
            f"http://{IP}/live/{nombre}/playlist.m3u8",
            f"http://{IP}/live/{nombre}"
        ]
        for url in formatos_live:
            try:
                # Usamos un timeout corto para no trabar el script
                r = requests.head(url, headers=HEADERS, timeout=1.5)
                if r.status_code == 200:
                    f.write(f'#EXTINF:-1 tvg-id="{nombre}" group-title="{grupo}",{nombre.replace("_", " ")} EN VIVO\n{url}\n')
                    print(f"  🔥 ¡SEÑAL EN VIVO DETECTADA!: {nombre}")
                    encontrados += 1
                    break
            except: continue

    # --- LÓGICA PARA CONTENIDO GRABADO (VOD) ---
    else:
        # (Aquí va tu lógica anterior de S01E01 que ya funciona)
        for s in range(0, 3):
            for e in range(1, 11):
                url = f"http://{IP}/movies/{carpeta}/{nombre}.mp4" if s==0 else f"http://{IP}/movies/{carpeta}/{nombre}_S{s:02d}E{e:02d}.mp4"
                try:
                    r = requests.head(url, headers=HEADERS, timeout=0.5)
                    if r.status_code == 200:
                        nombre_txt = nombre if s==0 else f"{nombre} S{s:02d}E{e:02d}"
                        f.write(f'#EXTINF:-1 group-title="{grupo}",{nombre_txt}\n{url}\n')
                        print(f"  ✅ {nombre_txt}")
                        encontrados += 1
                        if s == 0: break
                    elif s > 0 and e > 2: break
                except: break
            if s == 0: break
    return encontrados

def main():
    print("🚀 SISTEMA JEYCAMON: RASTREO VOD + TV EN VIVO 🚀")
    total = 0
    with open("extra_premium.m3u", "w") as f:
        f.write("#EXTM3U\n")
        for carpeta, titulos in MAPA_CONTENIDO.items():
            for t in titulos:
                total += buscar_en_carpeta(carpeta, t, f)
    print(f"\n✨ ¡ESCANEADO FINALIZADO! {total} señales/archivos listos.")

if __name__ == "__main__":
    main()

