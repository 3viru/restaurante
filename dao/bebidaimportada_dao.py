from dao.bebida_dao import BebidaDao

class BebidaImportadaDao(BebidaDao):
    def crear_tabla(self):
        super().crear_tabla()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS bebidas_importadas (
            id INTEGER PRIMARY KEY,
            paisOrigen TEXT NOT NULL,
            FOREIGN KEY (id) REFERENCES bebidas (id)
        )""")
        self.conexion.commit()

    def insertar(self, bebida_imp):
        # Llama al insertar de BebidaDao, el cual llama a ItemMenuDao
        id_generado = super().insertar(bebida_imp)
        self.cursor.execute("""
        INSERT INTO bebidas_importadas (id, paisOrigen)
        VALUES (?, ?)
        """, (id_generado, bebida_imp.paisOrigen))
        self.conexion.commit()
        return id_generado
