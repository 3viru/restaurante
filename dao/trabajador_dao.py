from dao.dao import Dao

class TrabajadorDao(Dao):
    def crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS trabajadores (
            rut TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            rol TEXT NOT NULL
        )""")
        self.conexion.commit()
