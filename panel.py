import json
import os
from datetime import datetime, timedelta

DB_FILE = "clientes.json"

def cargar_db():
    if not os.path.exists(DB_FILE):
        return {"clientes": []}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def guardar_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

def crear_cliente():
    nombre = input("👤 Nombre del cliente: ")
    user = input("🔑 Usuario (ej: jeyca01): ")
    horas = int(input("⏳ Duración en horas (2 para Demo, 720 para 1 mes): "))
    
    vencimiento = datetime.now() + timedelta(hours=horas)
    
    db = cargar_db()
    nuevo_cliente = {
        "nombre": nombre,
        "user": user,
        "pass": "Jeyca" + str(len(db["clientes"]) + 1),
        "vencimiento": vencimiento.strftime("%Y-%m-%d %H:%M"),
        "status": "Activo",
        "link": f"https://raw.githubusercontent.com/jesuscantillo1018-creator/Jeycamontv/maestro/global_jeycamon.m3u"
    }
    
    db["clientes"].append(nuevo_cliente)
    guardar_db(db)
    print(f"\n✅ Cliente creado con éxito!")
    print(f"🔗 Link M3U: {nuevo_cliente['link']}")
    print(f"📅 Vence: {nuevo_cliente['vencimiento']}")

def listar_clientes():
    db = cargar_db()
    print("\n--- 📝 LISTA DE CLIENTES JEYCAMONTV ---")
    for c in db["clientes"]:
        venc = datetime.strptime(c["vencimiento"], "%Y-%m-%d %H:%M")
        status = "✅" if venc > datetime.now() else "❌ EXPIRADO"
        print(f"{status} {c['nombre']} | Usuario: {c['user']} | Vence: {c['vencimiento']}")

def menu():
    while True:
        print("\n--- 🚀 JEYCAMONTV RESELLER PANEL ---")
        print("1. Crear Nuevo Cliente / Demo")
        print("2. Ver Lista de Clientes")
        print("3. Salir")
        opcion = input("Seleccione: ")
        
        if opcion == "1": crear_cliente()
        elif opcion == "2": listar_clientes()
        elif opcion == "3": break
        else: print("Opción no válida")

if __name__ == "__main__":
    menu()
