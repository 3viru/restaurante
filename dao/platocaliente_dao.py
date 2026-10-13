from dao.itemmenu_dao import ItemMenuDao
class PlatoCalienteDao(ItemMenuDao):
    def crear_tabla(self):
        super().crear_tabla()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS platos_calientes (
            id INTEGER PRIMARY KEY,
            temperaturaServicio INTEGER NOT NULL,
            FOREIGN KEY (id) REFERENCES itemmenu (id)
        )""")
        self.conexion.commit()

    def insertar(self, plato):
        id_generado = super().insertar(plato)
        self.cursor.execute("""
        INSERT INTO platos_calientes (id, temperaturaServicio)
        VALUES (?, ?)
        """, (id_generado, plato.temperaturaServicio))
        self.conexion.commit()
        return id_generado

    def actualizar(self, plato) -> bool:
        try:
            super().actualizar(plato)
            self.cursor.execute("""
            UPDATE platos_calientes
            SET temperaturaServicio = ?
            WHERE id = ?
            """, (plato.temperaturaServicio, plato.id))
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            raise e
