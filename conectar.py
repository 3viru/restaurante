import sqlite3

def crear_conexion():
    conn = sqlite3.connect("restaurante.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
