import json, os, random, string, requests
from datetime import datetime, timedelta
try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except ImportError:
    os.system('pip install colorama')
    from colorama import Fore, Back, Style, init
    init(autoreset=True)

# --- CONFIGURACIÓN ---
DB_FILE = "clientes.json"
RESELLERS_FILE = "revendedores.json" # Nueva DB para créditos
CLIENT_DIR = "clientesTV"
LINK_BASE = "https://raw.githubusercontent.com/jesuscantillo1018-creator/Jeycamontv/maestro/clientesTV/"
LINK_MAESTRO = "global_jeycamon.m3u"
WEBAPP_URL = "TU_URL_DE_APPSCRIPT_AQUI" 

R, W, G, Y, C = Fore.RED + Style.BRIGHT, Fore.WHITE + Style.BRIGHT, Fore.GREEN + Style.BRIGHT, Fore.YELLOW + Style.BRIGHT, Fore.CYAN + Style.BRIGHT

# --- LÓGICA DE CRÉDITOS ---
def cargar_db(archivo):
    if not os.path.exists(archivo): 
        return {"clientes": []} if "clientes" in archivo else {}
    with open(archivo, "r") as f: return json.load(f)

def guardar_db(archivo, datos):
    with open(archivo, "w") as f: json.dump(datos, f, indent=4)

def gestionar_creditos():
    r_db = cargar_db(RESELLERS_FILE)
    print(f"\n{R}--- {W}GESTIÓN DE CRÉDITOS {R}---")
    nombre = input(f"{W}Nombre del Revendedor: ").upper()
    try:
        cantidad = int(input(f"{W}Créditos a añadir: "))
    except: return
    
    r_db[nombre] = r_db.get(nombre, 0) + cantidad
    guardar_db(RESELLERS_FILE, r_db)
    print(f"{G}✅ {nombre} ahora tiene {r_db[nombre]} créditos.")

def crear_cliente():
    r_db = cargar_db(RESELLERS_FILE)
    print(f"\n{R}--- {W}NUEVA VENTA / DEMO {R}---")
    rev = input(f"{W}Revendedor: ").upper()
    
    # Validar créditos (Demos no consumen crédito, 1 mes sí)
    horas = int(input(f"{W}Duración (Horas - 2 para Demo, 720 para Mes): "))
    es_demo = horas <= 24
    
    if not es_demo:
        saldo = r_db.get(rev, 0)
        if saldo < 1:
            print(f"{R}❌ ERROR: {rev} no tiene créditos suficientes (Saldo: {saldo})")
            return
        r_db[rev] -= 1 # Descontar crédito
    
    nombre_cli = input(f"{W}Nombre Cliente: ")
    interes = input(f"{W}Interés (HBO, Win+, etc): ").upper()
    token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    archivo_cliente = f"access_{token}.m3u"
    venc_dt = datetime.now() + timedelta(hours=horas)
    
    if os.path.exists(LINK_MAESTRO):
        with open(LINK_MAESTRO, 'r') as original: data = original.read()
        if not os.path.exists(CLIENT_DIR): os.makedirs(CLIENT_DIR)
        with open(f"{CLIENT_DIR}/{archivo_cliente}", 'w') as f: f.write(data)
        
        datos = {
            "nombre": nombre_cli, "interes": interes, "revendedor": rev,
            "vence": venc_dt.strftime("%Y-%m-%d %H:%M"), "link": LINK_BASE + archivo_cliente,
            "registro": datetime.now().strftime("%Y-%m-%d")
        }
        
        c_db = cargar_db(DB_FILE)
        c_db["clientes"].append(datos)
        guardar_db(DB_FILE, c_db)
        guardar_db(RESELLERS_FILE, r_db) # Guardar nuevo saldo

        print(f"{Y}🚀 Sincronizando...")
        os.system("bash actualizar.sh")
        print(f"\n{G}✅ CLIENTE ACTIVO. SALDO DE {rev}: {r_db.get(rev, 0)}")
    else:
        print(f"{R}❌ No existe {LINK_MAESTRO}")

def listar_alertas():
    c_db = cargar_db(DB_FILE)
    hoy = datetime.now()
    print(f"\n{Back.RED}{W}   ⚠️ CLIENTES POR VENCER (PRÓX. 48H)   ")
    for c in c_db["clientes"]:
        venc = datetime.strptime(c["vencimiento" if "vencimiento" in c else "vence"], "%Y-%m-%d %H:%M")
        if hoy < venc < hoy + timedelta(hours=48):
            print(f"{Y}🔔 {c['nombre']} ({c['revendedor']}) vence el {c['vence']}")

def menu():
    while True:
        os.system('clear')
        print(f"{R}########################################")
        print(f"{R}#     {W}JEYCAMONTV - MASTER ADMIN PRO    {R}#")
        print(f"{R}########################################")
        print(f"{W}1. {G}➕ {W}Nueva Venta / Demo")
        print(f"{W}2. {C}💰 {W}Cargar Créditos a Revendedor")
        print(f"{W}3. {Y}📋 {W}Ver Alertas de Vencimiento")
        print(f"{W}4. {W}🔍 Ver Saldo de Revendedores")
        print(f"{W}5. {R}🚪 {W}Salir")
        op = input(f"\n{W}Seleccione: ")
        if op == "1": crear_cliente(); input(f"\n{W}Enter...")
        elif op == "2": gestionar_creditos(); input(f"\n{W}Enter...")
        elif op == "3": listar_alertas(); input(f"\n{W}Enter...")
        elif op == "4": 
            r_db = cargar_db(RESELLERS_FILE)
            for k, v in r_db.items(): print(f"{W}{k}: {G}{v} créditos")
            input(f"\n{W}Enter...")
        elif op == "5": break

if __name__ == "__main__": menu()
