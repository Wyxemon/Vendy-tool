import firebase_admin
from firebase_admin import credentials, db
from json import dump, load
from datetime import datetime
from os import listdir, startfile, system, name
from prompt_toolkit.shortcuts import radiolist_dialog
from sys import exit
from os import path, makedirs

BASE_DIR = path.dirname(path.abspath(__file__))
BACKUP_DIR = path.join(BASE_DIR, "backup")
KEY_PATH = path.join(BASE_DIR, "serviceAccountKey.json")

cred = credentials.Certificate(KEY_PATH)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://vendy-4687d-default-rtdb.europe-west1.firebasedatabase.app"
})
ref = db.reference("/")

makedirs(BACKUP_DIR, exist_ok=True)

def createBackup():
    data = ref.get()
    datenow = datetime.now().strftime("%d-%m-%Y_%H-%M")
    current = path.join(BACKUP_DIR, f"backup{datenow}.json")
    with open(current, "w", encoding="utf-8") as a:
        dump(data, a, ensure_ascii=False, indent=4)

def applyBackup(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = load(f)
    ref.set(data)

def openNote(file_name):
    startfile(path.join(BACKUP_DIR, file_name))

while True:
    result = radiolist_dialog(
        title="Vendy Tool",
        text="Selecciona una opción:",
        values=[
            ("1", "Crear backup"),
            ("2", "Ver backups"),
            ("3", "Aplicar backup en Vendy"),
            ("0", "Salir"),
        ],
    ).run()

    if result == "1":
        system("cls" if name == "nt" else "clear")
        createBackup()
        datenow = datetime.now().strftime("%d-%m-%Y_%H-%M")
        print(f"Backup creado: backup{datenow}")
        input("Enter...")

    elif result == "2":
        lista = listdir(BACKUP_DIR)
        if not lista:
            print("No hay backups disponibles.")
            input("Enter...")
            continue

        result = radiolist_dialog(
            title="Ver backups",
            text="Selecciona un backup:",
            values=[(file, file) for file in lista],
        ).run()

        if result:
            openNote(result)

    elif result == "3":
        lista = listdir(BACKUP_DIR)
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
            applyBackup(path.join(BACKUP_DIR, result))
            print(f"Backup {result} aplicada en la base de datos.")
            input("Enter...")

    else:
        exit()