from dao.dao import Dao

class PedidoDao(Dao):
    def crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            numero_pedido INTEGER PRIMARY KEY,
            fecha_hora TEXT NOT NULL,
            estado TEXT NOT NULL,
            mesa_numero INTEGER,
            total REAL
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalles_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_pedido INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            observacion TEXT,
            listo INTEGER NOT NULL,
            FOREIGN KEY (numero_pedido) REFERENCES pedidos (numero_pedido),
            FOREIGN KEY (item_id) REFERENCES itemmenu (id)
        )""")
        self.conexion.commit()

    def obtener_siguiente_numero(self) -> int:
        self.cursor.execute("SELECT COALESCE(MAX(numero_pedido), 0) + 1 FROM pedidos")
        row = self.cursor.fetchone()
        return row[0] if row else 1

    def guardar_pedido(self, pedido, mesa_numero: int = None, total: float = 0.0):
        self.cursor.execute("""
        INSERT OR REPLACE INTO pedidos (numero_pedido, fecha_hora, estado, mesa_numero, total)
        VALUES (?, ?, ?, ?, ?)
        """, (pedido.numeroPedido, pedido.fechaHora, pedido.estado, mesa_numero, total))
        
        # Sincronizar detalles (reemplazando para evitar duplicados en actualizaciones)
        self.cursor.execute("DELETE FROM detalles_pedido WHERE numero_pedido = ?", (pedido.numeroPedido,))
        for d in pedido.detalles:
            self.cursor.execute("""
            INSERT INTO detalles_pedido (numero_pedido, item_id, cantidad, observacion, listo)
            VALUES (?, ?, ?, ?, ?)
            """, (pedido.numeroPedido, d.item.id, d.cantidad, d.observacion, 1 if d.listo else 0))
        self.conexion.commit()

    def actualizar_estado(self, numero_pedido: int, estado: str, total: float = None):
        if total is not None:
            self.cursor.execute("""
            UPDATE pedidos SET estado = ?, total = ? WHERE numero_pedido = ?
            """, (estado, total, numero_pedido))
        else:
            self.cursor.execute("""
            UPDATE pedidos SET estado = ? WHERE numero_pedido = ?
            """, (estado, numero_pedido))
        self.conexion.commit()

    def listar_pedidos(self):
        self.cursor.execute("""
        SELECT numero_pedido, fecha_hora, estado, mesa_numero, total
        FROM pedidos
        ORDER BY numero_pedido DESC
        """)
        return self.cursor.fetchall()
