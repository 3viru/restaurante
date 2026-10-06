from dao.trabajador_dao import TrabajadorDao

class MeseroDao(TrabajadorDao):
    def crear_tabla(self):
        super().crear_tabla()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS meseros (
            rut TEXT PRIMARY KEY,
            FOREIGN KEY (rut) REFERENCES trabajadores (rut)
        )""")
        self.conexion.commit()
