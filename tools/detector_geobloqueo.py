import requests
import re
import os
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURACIÓN ---
URL_RAW = "https://raw.githubusercontent.com/jesuscantillo1018-creator/Jeycamontv/maestro/global_jeycamon.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': '*/*'
}

def testear_canal(bloque):
    info, url = bloque
    nombre = info.split(',')[-1].strip()
    try:
        # Hacemos una petición HEAD o GET corta para ver el estado
        response = requests.get(url, headers=HEADERS, timeout=6, stream=True, allow_redirects=True)
        status = response.status_code
        
        if status == 200:
            return f"✅ [OK] - {nombre}"
        elif status in [403, 451]:
            return f"🚫 [GEO-BLOQUEADO] - {nombre} (Código: {status})"
        elif status == 404:
            return f"💀 [MUERTO] - {nombre} (No existe)"
        else:
            return f"⚠️ [ERROR {status}] - {nombre}"
    except Exception:
        return f"❌ [TIMEOUT/CAÍDO] - {nombre}"

def procesar():
    print("\n" + "="*50)
    print("🌍 ESCÁNER DE REGIÓN JEYCAMON TV")
    print("="*50)
    print(f"[📥] Obteniendo lista desde tu GitHub...")
    
    try:
        r = requests.get(URL_RAW)
        bloques = re.findall(r'(#EXTINF:.*?)\n(http.*?)(?=\n#EXTINF|$)', r.text, re.DOTALL)
    except:
        print("Error al conectar con GitHub.")
        return

    print(f"[🔍] Analizando {len(bloques)} canales desde tu IP actual...")
    print("Nota: Si estás en USA, verás cuáles te bloquean por región.\n")

    # Auditoría rápida con 40 hilos
    with ThreadPoolExecutor(max_workers=40) as executor:
        resultados = list(executor.map(testear_canal, bloques))

    # Clasificación de resultados
    geobloqueados = [res for res in resultados if "GEO-BLOQUEADO" in res]
    funcionales = [res for res in resultados if "OK" in res]
    otros = [res for res in resultados if "OK" not in res and "GEO-BLOQUEADO" not in res]

    # Mostrar solo los bloqueados para que los identifiques rápido
    print("--- CANALES DETECTADOS CON BLOQUEO DE REGIÓN ---")
    if not geobloqueados:
        print("Ninguno detectado (o todos están caídos/abiertos).")
    else:
        for canal in geobloqueados:
            print(canal)

    print("\n" + "="*50)
    print(f"📊 RESUMEN DESDE TU UBICACIÓN:")
    print(f"✅ Canales Abiertos: {len(funcionales)}")
    print(f"🚫 Canales Geobloqueados: {len(geobloqueados)}")
    print(f"💀 Otros errores/Caídos: {len(otros)}")
    print("="*50)

if __name__ == "__main__":
    procesar()
