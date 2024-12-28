import sqlite3
import os
from colorama import Fore, Style, init

# Inicializar colorama para colores en la terminal
init(autoreset=True)

# Conectar o crear la base de datos
conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

# Crear tabla de productos 
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    numero_producto TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    categoria TEXT,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL
)              
''')

