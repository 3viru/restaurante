import datetime
from dao.dao import Dao

class BoletaDao(Dao):
    def crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS boletas (
            numero_boleta INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_pedido INTEGER,
            rut_cliente TEXT NOT NULL,
            monto_neto REAL NOT NULL,
            monto_total REAL NOT NULL,
            fecha_hora TEXT NOT NULL,
            FOREIGN KEY (numero_pedido) REFERENCES pedidos (numero_pedido)
        )""")
        self.conexion.commit()

    def insertar(self, boleta, numero_pedido: int = None, fecha_hora: str = None) -> int:
        if fecha_hora is None:
            fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
        INSERT INTO boletas (numero_pedido, rut_cliente, monto_neto, monto_total, fecha_hora)
        VALUES (?, ?, ?, ?, ?)
        """, (numero_pedido, boleta.rutCliente, boleta.montoNeto, boleta.montoTotal, fecha_hora))
        self.conexion.commit()
        return self.cursor.lastrowid

    def listar_todas(self):
        self.cursor.execute("""
        SELECT numero_boleta, numero_pedido, rut_cliente, monto_neto, monto_total, fecha_hora
        FROM boletas
        ORDER BY numero_boleta DESC
        """)
        return self.cursor.fetchall()
