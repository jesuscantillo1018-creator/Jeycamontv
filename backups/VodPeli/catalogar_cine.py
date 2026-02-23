import requests
import re

IP = "45.226.168.29"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# 🎬 ORGANIZACIÓN POR GÉNEROS
# Puedes añadir más títulos aquí y el script los buscará sin duplicar
PELICULAS_POR_GENERO = {
    "ESTRENOS 2024": ["Moana_2", "Gladiador_2", "Deadpool_Wolverine", "Intensamente_2", "Guason_2", "Venom_3", "Sonic_3", "Mufasa", "Wicked"],
    "ACCION": ["John_Wick_4", "Transformers", "Spider_Man", "Batman", "Flash", "Aquaman_2", "Blue_Beetle", "Top_Gun_Maverick"],
    "TERROR": ["Terrifier_3", "El_Conjuro", "Saw_X", "El_Hoyo_2", "Alien_Romulus"],
    "INFANTIL": ["Mario_Bros", "Barbie", "Wonka", "Minions", "Toy_Story_4", "Frozen_2", "Coco", "Encanto", "Shrek", "Kung_Fu_Panda_4"],
    "CIENCIA FICCION": ["Avatar_2", "Oppenheimer", "Duna_2", "Godzilla_Minus_One"]
}

def limpiar_nombre(n):
    return n.replace("_", " ").title()

def catalogar():
    print("🎨 Clasificando películas por géneros...")
    total = 0
    # Usamos set() para evitar duplicados en la misma sesión
    encontradas_hoy = set()

    with open("cine_premium.m3u", "w") as f:
        f.write("#EXTM3U\n")
        
        for genero, titulos in PELICULAS_POR_GENERO.items():
            grupo = f"🍿 JEYCAMON {genero}"
            print(f"\n📂 Categoría: {genero}")
            
            for t in titulos:
                if t in encontradas_hoy: continue # Evita duplicar si pusiste la misma peli en dos géneros
                
                url = f"http://{IP}/movies/{t}.mp4"
                try:
                    r = requests.head(url, headers=HEADERS, timeout=1)
                    if r.status_code == 200:
                        nombre = limpiar_nombre(t)
                        f.write(f'#EXTINF:-1 group-title="{grupo}",{nombre}\n{url}\n')
                        print(f"  ⭐ {nombre}")
                        encontradas_hoy.add(t)
                        total += 1
                except: continue
                
    print(f"\n🚀 ¡Listo! {total} películas organizadas por género.")

if __name__ == "__main__":
    catalogar()

