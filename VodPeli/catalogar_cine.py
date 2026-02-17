import requests

# Configuración
IP = "45.226.168.29"
RUTA = "/movies/"
NOMBRE_ARCHIVO = "cine_premium.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Lista de títulos (puedes seguir ampliándola)
PELIS = [
    "Moana2", "Gladiador2", "DeadpoolWolverine", "Intensamente2", "Guason2", 
    "Venom3", "Sonic3", "Avatar2", "Mufasa", "Wicked", "Terrifier3", "ElHoyo2",
    "MarioBros", "Barbie", "Oppenheimer", "JohnWick4", "Pinocho", "Transformers",
    "SpiderMan", "Batman", "Flash", "Aquaman2", "BlueBeetle", "Wonka",
    "Minions", "ToyStory4", "Frozen2", "Coco", "Encanto", "Shrek", "KungFuPanda4",
    "ElConjuro", "SawX", "TopGunMaverick", "Duna2", "GodzillaMinusOne", "AlienRomulus"
]

EXTS = [".mp4", ".mov", ".mkv"]

def limpiar_nombre(texto):
    # Separa mayúsculas (ej: Moana2 -> Moana 2)
    import re
    res = re.sub(r'([a-z])([A-Z0-8])', r'\1 \2', texto)
    return res.title()

def generar_catalogo():
    print(f"🎨 Embelleciendo JEYCAMON CINEMA...")
    total = 0

    with open(NOMBRE_ARCHIVO, "w") as f:
        f.write("#EXTM3U\n")
        
        for p in PELIS:
            hallada = False
            for ext in EXTS:
                if hallada: break
                for variante in [p, p.lower(), p.replace(" ", "_")]:
                    if hallada: break
                    url = f"http://{IP}{RUTA}{variante}{ext}"
                    try:
                        r = requests.head(url, headers=HEADERS, timeout=1)
                        if r.status_code == 200:
                            nombre_bonito = limpiar_nombre(p)
                            
                            # URL de logo genérica basada en el nombre para que la APP busque el poster
                            logo_url = f"https://www.themoviedb.org/search?query={p}" 
                            
                            # Escribimos la línea con metadatos extendidos
                            f.write(f'#EXTINF:-1 tvg-name="{nombre_bonito}" tvg-logo="https://raw.githubusercontent.com/jesuscantillo1018-creator/Jeycamontv/maestro/logo_cine.png" group-title="🍿 JEYCAMON CINEMA",{nombre_bonito}\n')
                            f.write(f'{url}\n')
                            
                            print(f"⭐ Agregada con estilo: {nombre_bonito}")
                            total += 1
                            hallada = True
                    except:
                        continue

    print(f"\n🚀 ¡Listo! {total} películas formateadas para Jeycamontv.")

if __name__ == "__main__":
    generar_catalogo()

