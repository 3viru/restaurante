from dao.dao import Dao
from model.trabajador import Trabajador

class TrabajadorDao(Dao):
    """
    DAO para la entidad Trabajador en SQLite.
    Cumple con Criterio 2.1.3:
    - Operaciones CRUD completas (Crear, Leer, Actualizar, Eliminar).
    - Consultas 100% parametrizadas con placeholders '?' (previene inyección SQL).
    """

    def crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS trabajadores (
            rut TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            rol TEXT NOT NULL
        )""")
        self.conexion.commit()

    def insertar(self, trabajador: Trabajador) -> str:
        self.cursor.execute("""
        INSERT INTO trabajadores (rut, nombre, rol)
        VALUES (?, ?, ?)
        """, (trabajador.rut, trabajador.nombre, trabajador.rol))
        self.conexion.commit()
        return trabajador.rut

    def obtener_por_rut(self, rut: str):
        self.cursor.execute("""
        SELECT rut, nombre, rol
        FROM trabajadores
        WHERE rut = ?
        """, (rut,))
        fila = self.cursor.fetchone()
        if not fila:
            return None
        r, n, rol = fila
        return Trabajador(r, n, rol)

    def listar_todos(self) -> list:
        self.cursor.execute("""
        SELECT rut, nombre, rol
        FROM trabajadores
        ORDER BY nombre ASC
        """)
        filas = self.cursor.fetchall()
        return [Trabajador(r, n, rol) for r, n, rol in filas]

    def actualizar(self, trabajador: Trabajador) -> bool:
        try:
            self.cursor.execute("""
            UPDATE trabajadores
            SET nombre = ?, rol = ?
            WHERE rut = ?
            """, (trabajador.nombre, trabajador.rol, trabajador.rut))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conexion.rollback()
            raise e

    def eliminar(self, rut: str) -> bool:
        try:
            self.cursor.execute("DELETE FROM trabajadores WHERE rut = ?", (rut,))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conexion.rollback()
            raise e
