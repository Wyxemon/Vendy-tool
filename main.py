import firebase_admin
from firebase_admin import credentials, db
from json import dump, load
from datetime import datetime
from os import listdir, startfile, system, name
from prompt_toolkit.shortcuts import radiolist_dialog
from sys import exit
from os import path, makedirs

dir = path.dirname(path.abspath(__file__)) # ruta del proyecto
backup_dir = path.join(dir, "backup") # ruta de la carpeta backup
key = path.join(dir, "serviceAccountKey.json") # ruta del archivo serviceAccountKey.json

# firebas conexión
cred = credentials.Certificate(key) 

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://vendy-4687d-default-rtdb.europe-west1.firebasedatabase.app"
})
ref = db.reference("/") # ruta raiz

#----------------------- 


makedirs(backup_dir, exist_ok=True) # crear carpeta si no existe

def createBackup():
    data = ref.get() # firebase kontua
    datenow = datetime.now().strftime("%d-%m-%Y_%H-%M") # fecha actual
    current = path.join(backup_dir, f"backup{datenow}.json") # crear archivo
    with open(current, "w", encoding="utf-8") as a:
        dump(data, a, ensure_ascii=False, indent=4) # crear json con 4 espacios

def applyBackup(filename):
    with open(filename, "r", encoding="utf-8") as f: # fitxategia irakurri
        data = load(f) # fitxategiaren informazioa edukia hartu eta gorde aldagi batean
    ref.set(data) # poner en la ruta el archivo

def openNote(file_name):
    startfile(path.join(backup_dir, file_name)) # iniciar archivo en otro navegador

while True:
    result = radiolist_dialog( # sortu menu
        title="Vendy Tool", # izena
        text="Selecciona una opción:", # izenburua
        values=[ # aukerak
            ("1", "Crear backup"),
            ("2", "Ver backups"),
            ("3", "Aplicar backup en Vendy"),
            ("0", "Salir"),
        ],
    ).run()

    if result == "1": # lehenengo aukeraren baldintza
        system("cls" if name == "nt" else "clear") # terminala garbitu
        createBackup() # sortu backup
        datenow = datetime.now().strftime("%d-%m-%Y_%H-%M") # momentu egoerako data jakiteko
        print(f"Backup creado: backup{datenow}") # sortutako pantailan erakutsi
        input("Enter...")

    elif result == "2": # bigarren aukeraren baldintza
        lista = listdir(backup_dir) # backup karpetaren barruan zerrendatzea
        if not lista: # lista ez bada
            print("No hay backups disponibles.")
            input("Enter...")
            continue

        result = radiolist_dialog( # sortu menua
            title="Ver backups",
            text="Selecciona un backup:",
            values=[(file, file) for file in lista], # for bukle baten bidez backup direktorioaren fitxategiak erakutsi.
        ).run()

        if result: # erantzuten ba dugu
            openNote(result) # funtzioa deitu

    elif result == "3": # hirugarren aukeraren baldintza
        lista = listdir(backup_dir) # goikoaren berdina
        if not lista:
            print("No hay backups disponibles.")
            input("Enter...")
            continue

        result = radiolist_dialog(
            title="Aplicar backup",
            text="Selecciona un backup que quieras aplicar:",
            values=[(file, file) for file in lista],
        ).run()

        if result: 
            applyBackup(path.join(backup_dir, result))
            print(f"Backup {result} aplicada en la base de datos.")
            input("Enter...")

    else:
        exit()