import requests

IP = "45.226.168.29"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# 🤖 MEGA-DICCIONARIO DE 100 TÍTULOS
DICCIONARIO_BUSQUEDA = [
    # Estrenos y Recientes
    "Moana_2", "Gladiador_2", "Deadpool_Wolverine", "Intensamente_2", "Guason_2", 
    "Venom_3", "Sonic_3", "Mufasa", "Wicked", "Terrifier_3", "Smile_2", "Beetlejuice_2",
    "Alien_Romulus", "Duna_2", "Godzilla_Minus_One", "Despicable_Me_4", "Kung_Fu_Panda_4",
    # Acción y Sagas
    "John_Wick_1", "John_Wick_2", "John_Wick_3", "John_Wick_4",
    "Fast_X", "Fast_And_Furious_9", "Top_Gun_Maverick", "Mission_Impossible_Dead_Reckoning",
    "The_Equalizer_3", "Expendables_4", "Gran_Turismo", "Meg_2_The_Trench",
    # Superhéroes
    "Spider_Man_No_Way_Home", "Spider_Man_Across_the_Spider_Verse", "Guardians_of_the_Galaxy_Vol_3",
    "Ant_Man_And_The_Wasp_Quantumania", "The_Flash", "Aquaman_And_The_Lost_Kingdom", "Blue_Beetle",
    "The_Marvels", "The_Batman", "Black_Adam", "Thor_Love_And_Thunder", "Doctor_Strange_Multiverse",
    # Ciencia Ficción y Aventura
    "Avatar_The_Way_of_Water", "Oppenheimer", "Transformers_Rise_of_the_Beasts", "Indiana_Jones_5",
    "Jurassic_World_Dominion", "Prey", "The_Creator", "Rebel_Moon", "Dune_Part_One",
    # Terror y Suspenso
    "Saw_X", "The_Nun_2", "Evil_Dead_Rise", "Scream_VI", "M3GAN", "Talk_To_Me",
    "Five_Nights_At_Freddys", "Insidious_The_Red_Door", "A_Quiet_Place_Day_One", "Longlegs",
    # Animación y Familia
    "Mario_Bros", "Barbie", "Wonka", "Puss_In_Boots_The_Last_Wish", "Elemental", "Wish",
    "The_Little_Mermaid_2023", "Spider_Man_Into_the_Spider_Verse", "Minions_The_Rise_of_Gru",
    "Toy_Story_4", "Frozen_2", "Encanto", "Coco", "Turning_Red", "Luca",
    # Clásicos que suelen estar
    "Titanic", "Gladiator", "Inception", "Interstellar", "The_Dark_Knight", "Pulp_Fiction",
    "The_Matrix", "Fight_Club", "Forrest_Gump", "The_Lion_King", "Harry_Potter_1",
    # Drama y Otros
    "The_Whale", "Everything_Everywhere_All_At_Once", "Killers_of_the_Flower_Moon", 
    "Napoleon", "Society_of_the_Snow", "Leave_the_World_Behind", "Saltburn"
]

def adivinar_peliculas():
    print(f"🤖 Robot Jeycamon iniciando escaneo de {len(DICCIONARIO_BUSQUEDA)} títulos...")
    encontradas = []
    
    for titulo in DICCIONARIO_BUSQUEDA:
        url = f"http://{IP}/movies/{titulo}.mp4"
        try:
            r = requests.head(url, headers=HEADERS, timeout=0.6)
            if r.status_code == 200:
                print(f"  ✨ ¡HALLAZGO!: {titulo.replace('_', ' ')}")
                encontradas.append(titulo)
        except:
            continue
    
    with open("hallazgos_robot.txt", "w") as f:
        for peli in encontradas:
            f.write(f"{peli}\n")
    
    print(f"\n🤖 Escaneo finalizado. Se detectaron {len(encontradas)} películas activas en el servidor.")

if __name__ == "__main__":
    adivinar_peliculas()

