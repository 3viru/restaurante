from dao.itemmenu_dao import ItemMenuDao

class PostreDao(ItemMenuDao):
    def crear_tabla(self):
        super().crear_tabla()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS postres (
            id INTEGER PRIMARY KEY,
            requiereRefrigeracion INTEGER NOT NULL,
            FOREIGN KEY (id) REFERENCES itemmenu (id)
        )""")
        self.conexion.commit()

    def insertar(self, postre):
        id_generado = super().insertar(postre)
        self.cursor.execute("""
        INSERT INTO postres (id, requiereRefrigeracion)
        VALUES (?, ?)
        """, (id_generado, 1 if postre.requiereRefrigeracion else 0))
        self.conexion.commit()
        return id_generado
