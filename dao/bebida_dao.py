from dao.itemmenu_dao import ItemMenuDao
class BebidaDao(ItemMenuDao):
    def crear_tabla(self):
        super().crear_tabla()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS bebidas (
            id INTEGER PRIMARY KEY,
            esAlcoholica INTEGER NOT NULL,
            FOREIGN KEY (id) REFERENCES itemmenu (id)
        )""")
        self.conexion.commit()

    def insertar(self, bebida):
        id_generado = super().insertar(bebida)
        self.cursor.execute("""
        INSERT INTO bebidas (id, esAlcoholica)
        VALUES (?, ?)
        """, (id_generado, 1 if bebida.esAlcoholica else 0))
        self.conexion.commit()
        return id_generado

    def actualizar(self, bebida) -> bool:
        try:
            super().actualizar(bebida)
            self.cursor.execute("""
            UPDATE bebidas
            SET esAlcoholica = ?
            WHERE id = ?
            """, (1 if bebida.esAlcoholica else 0, bebida.id))
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            raise e
