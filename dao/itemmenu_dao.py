from dao.dao import Dao
from model.itemmenu import ItemMenu
from model.platocaliente import PlatoCaliente
from model.bebida import Bebida
from model.bebidaimportada import BebidaImportada
from model.postre import Postre

class ItemMenuDao(Dao):
    def crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS itemmenu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precioBase REAL NOT NULL,
            disponible INTEGER NOT NULL
        )""")
        self.conexion.commit()

    def insertar(self, item):
        self.cursor.execute("""
        INSERT INTO itemmenu (nombre, precioBase, disponible)
        VALUES (?, ?, ?)
        """, (item.nombre, item.precioBase, 1 if item.disponible else 0))
        self.conexion.commit()
        item.id = self.cursor.lastrowid
        return item.id

    def actualizar_stock(self, id_item, disponible):
        self.cursor.execute("""
        UPDATE itemmenu SET disponible = ? WHERE id = ?
        """, (1 if disponible else 0, id_item))
        self.conexion.commit()

    def listar_todos(self):
        query = """
        SELECT i.id, i.nombre, i.precioBase, i.disponible,
               pc.temperaturaServicio,
               b.esAlcoholica,
               bi.paisOrigen,
               po.requiereRefrigeracion
        FROM itemmenu i
        LEFT JOIN platos_calientes pc ON i.id = pc.id
        LEFT JOIN bebidas b ON i.id = b.id
        LEFT JOIN bebidas_importadas bi ON b.id = bi.id
        LEFT JOIN postres po ON i.id = po.id
        ORDER BY i.id ASC
        """
        self.cursor.execute(query)
        filas = self.cursor.fetchall()
        items = []
        for fila in filas:
            id_item, nombre, precio_base, disponible, temp_serv, es_alc, pais_origen, req_refrig = fila
            disp_bool = bool(disponible)
            if pais_origen is not None:
                items.append(BebidaImportada(id_item, nombre, precio_base, disp_bool, bool(es_alc), pais_origen))
            elif es_alc is not None:
                items.append(Bebida(id_item, nombre, precio_base, disp_bool, bool(es_alc)))
            elif temp_serv is not None:
                items.append(PlatoCaliente(id_item, nombre, precio_base, disp_bool, temp_serv))
            elif req_refrig is not None:
                items.append(Postre(id_item, nombre, precio_base, disp_bool, bool(req_refrig)))
            else:
                items.append(ItemMenu(id_item, nombre, precio_base, disp_bool))
        return items
