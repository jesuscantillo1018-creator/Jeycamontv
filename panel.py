import json, os, random, string
from datetime import datetime, timedelta
try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except ImportError:
    os.system('pip install colorama')
    from colorama import Fore, Back, Style, init
    init(autoreset=True)

DB_FILE = "clientes.json"
CLIENT_DIR = "clientesTV"
LINK_BASE = "https://raw.githubusercontent.com/jesuscantillo1018-creator/Jeycamontv/maestro/clientesTV/"
LINK_MAESTRO = "global_jeycamon.m3u"

# --- DISEÑO VISUAL ---
R = Fore.RED + Style.BRIGHT
W = Fore.WHITE + Style.BRIGHT
G = Fore.GREEN + Style.BRIGHT
Y = Fore.YELLOW + Style.BRIGHT

def inicializar():
    if not os.path.exists(CLIENT_DIR): os.makedirs(CLIENT_DIR)

def cargar_db():
    if not os.path.exists(DB_FILE): return {"clientes": []}
    with open(DB_FILE, "r") as f: return json.load(f)

def guardar_db(db):
    with open(DB_FILE, "w") as f: json.dump(db, f, indent=4)

def crear_cliente():
    inicializar()
    print(f"\n{R}--- {W}REGISTRO DE CLIENTE PROFESIONAL {R}---")
    nombre = input(f"{W}Nombre del Cliente: ")
    
    print(f"\n{R}[ {W}REFERENCIA DE INTERÉS / GANCHO {R}]")
    print(f"{W}Ejemplo: Win Sport+, HBO, Novelas, XXX, etc.")
    interes = input(f"{W}¿Qué es lo que más consume?: ").upper()

    try:
        horas = int(input(f"{W}Duración (2=Demo, 720=1 Mes): "))
    except: return

    token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    archivo_cliente = f"access_{token}.m3u"
    vencimiento = datetime.now() + timedelta(hours=horas)
    
    if os.path.exists(LINK_MAESTRO):
        with open(LINK_MAESTRO, 'r') as original: data = original.read()
        with open(f"{CLIENT_DIR}/{archivo_cliente}", 'w') as f: f.write(data)
        
        db = cargar_db()
        nuevo = {
            "nombre": nombre,
            "interes": interes, # Aquí guardamos lo que le gusta
            "token": token,
            "vencimiento": vencimiento.strftime("%Y-%m-%d %H:%M"),
            "link_final": LINK_BASE + archivo_cliente,
            "fecha_registro": datetime.now().strftime("%Y-%m-%d")
        }
        db["clientes"].append(nuevo)
        guardar_db(db)
        
        print(f"\n{G}✅ CLIENTE REGISTRADO")
        print(f"{W}Perfil: {R}{interes}")
        print(f"{W}Link: {G}{nuevo['link_final']}")
        print(f"{R}Acción: {W}Corre ./actualizar.sh para sincronizar.")
    else:
        print(f"{R}❌ Error: No existe la lista maestra.")

def listar_clientes():
    db = cargar_db()
    print(f"\n{Back.RED}{W}   CONTROL DE USUARIOS JEYCAMONTV   ")
    print(f"{R}{'CLIENTE':<12} {'INTERÉS':<12} {'VENCE':<18} {'ESTADO'}")
    print(f"{W}{'-'*60}")
    for c in db["clientes"]:
        venc = datetime.strptime(c["vencimiento"], "%Y-%m-%d %H:%M")
        status = f"{G}ACTIVO" if venc > datetime.now() else f"{R}EXPIRADO"
        print(f"{W}{c['nombre']:<12} {Y}{c['interes']:<12} {W}{c['vencimiento']:<18} {status}")

def menu():
    while True:
        os.system('clear')
        print(f"{R}########################################")
        print(f"{R}#     {W}JEYCAMONTV - BUSINESS PANEL      {R}#")
        print(f"{R}########################################")
        print(f"{W}1. {R}➕ {W}Nuevo Cliente (Demo/Full)")
        print(f"{W}2. {R}📊 {W}Ver Cartera e Intereses")
        print(f"{W}3. {R}🚪 {W}Salir")
        print(f"{R}----------------------------------------")
        op = input(f"{W}Seleccione: ")
        if op == "1": crear_cliente(); input(f"\n{W}Presione Enter...")
        elif op == "2": listar_clientes(); input(f"\n{W}Presione Enter...")
        elif op == "3": break

if __name__ == "__main__":
    menu()
