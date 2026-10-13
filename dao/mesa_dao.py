from dao.dao import Dao
from model.mesa import Mesa

class MesaDao(Dao):
    """
    DAO para la entidad Mesa en SQLite.
    Cumple con Criterio 2.1.3:
    - CRUD completo (Crear, Leer, Actualizar, Eliminar).
    - Consultas 100% parametrizadas con placeholders '?' (previene inyección SQL).
    - Creación automática de la tabla en base de datos.
    """

    def crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS mesas (
            numero INTEGER PRIMARY KEY,
            capacidad INTEGER NOT NULL,
            estado TEXT NOT NULL,
            tiene_pedido INTEGER NOT NULL
        )""")
        self.conexion.commit()

    def insertar(self, mesa: Mesa) -> int:
        self.cursor.execute("""
        INSERT INTO mesas (numero, capacidad, estado, tiene_pedido)
        VALUES (?, ?, ?, ?)
        """, (mesa.numero, mesa.capacidad, mesa.estado, 1 if mesa.tienePedidoAbierto else 0))
        self.conexion.commit()
        return mesa.numero

    def obtener_por_numero(self, numero: int):
        self.cursor.execute("""
        SELECT numero, capacidad, estado, tiene_pedido
        FROM mesas
        WHERE numero = ?
        """, (numero,))
        fila = self.cursor.fetchone()
        if not fila:
            return None
        num, cap, est, tp = fila
        return Mesa(num, cap, estado=est, tienePedidoAbierto=bool(tp))

    def listar_todas(self) -> list:
        self.cursor.execute("""
        SELECT numero, capacidad, estado, tiene_pedido
        FROM mesas
        ORDER BY numero ASC
        """)
        filas = self.cursor.fetchall()
        mesas = []
        for num, cap, est, tp in filas:
            mesas.append(Mesa(num, cap, estado=est, tienePedidoAbierto=bool(tp)))
        return mesas

    def actualizar(self, mesa: Mesa) -> bool:
        try:
            self.cursor.execute("""
            UPDATE mesas
            SET capacidad = ?, estado = ?, tiene_pedido = ?
            WHERE numero = ?
            """, (mesa.capacidad, mesa.estado, 1 if mesa.tienePedidoAbierto else 0, mesa.numero))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conexion.rollback()
            raise e

    def actualizar_estado(self, numero: int, estado: str, tiene_pedido: bool) -> bool:
        try:
            self.cursor.execute("""
            UPDATE mesas
            SET estado = ?, tiene_pedido = ?
            WHERE numero = ?
            """, (estado, 1 if tiene_pedido else 0, numero))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conexion.rollback()
            raise e

    def eliminar(self, numero: int) -> bool:
        try:
            self.cursor.execute("DELETE FROM mesas WHERE numero = ?", (numero,))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conexion.rollback()
            raise e
