from dao.trabajador_dao import TrabajadorDao
from model.mesero import Mesero

class MeseroDao(TrabajadorDao):
    """
    DAO para la entidad Mesero (subtipo de Trabajador) en SQLite.
    Persistencia relacional con clave foránea hacia la tabla trabajadores.
    Operaciones CRUD completas y 100% parametrizadas (Criterio 2.1.3).
    """

    def crear_tabla(self):
        super().crear_tabla()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS meseros (
            rut TEXT PRIMARY KEY,
            FOREIGN KEY (rut) REFERENCES trabajadores (rut) ON DELETE CASCADE
        )""")
        self.conexion.commit()

    def insertar(self, mesero: Mesero) -> str:
        super().insertar(mesero)
        self.cursor.execute("""
        INSERT INTO meseros (rut)
        VALUES (?)
        """, (mesero.rut,))
        self.conexion.commit()
        return mesero.rut

    def obtener_por_rut(self, rut: str):
        self.cursor.execute("""
        SELECT t.rut, t.nombre
        FROM trabajadores t
        INNER JOIN meseros m ON t.rut = m.rut
        WHERE t.rut = ?
        """, (rut,))
        fila = self.cursor.fetchone()
        if not fila:
            return None
        r, n = fila
        return Mesero(r, n)

    def listar_todos(self) -> list:
        self.cursor.execute("""
        SELECT t.rut, t.nombre
        FROM trabajadores t
        INNER JOIN meseros m ON t.rut = m.rut
        ORDER BY t.nombre ASC
        """)
        filas = self.cursor.fetchall()
        return [Mesero(r, n) for r, n in filas]

    def actualizar(self, mesero: Mesero) -> bool:
        return super().actualizar(mesero)

    def eliminar(self, rut: str) -> bool:
        try:
            self.cursor.execute("DELETE FROM meseros WHERE rut = ?", (rut,))
            self.cursor.execute("DELETE FROM trabajadores WHERE rut = ?", (rut,))
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            raise e
