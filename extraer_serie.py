import requests
import re

def buscar_ids(file_id):
    # Intentamos cargar la página de vista previa del archivo
    url = f"https://drive.google.com/file/d/{file_id}/view"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    print(f"🔍 Analizando origen del archivo...")
    try:
        res = requests.get(url, headers=headers)
        # Buscamos si Google Drive revela el ID de la carpeta contenedora en el código fuente
        parent_id = re.findall(r'\"parent_id\":\"([^\"]+)\"', res.text)
        
        if parent_id:
            print(f"📂 ¡Carpeta encontrada! ID: {parent_id[0]}")
            return parent_id[0]
        else:
            print("❌ No se pudo encontrar la carpeta automáticamente.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    my_id = "1-fxjpfyO1EZL_cKmlyY_IB_-KmlaEih9"
    folder = buscar_ids(my_id)
    if folder:
        print(f"\nUsa este ID en el script drive_to_m3u.py: {folder}")
