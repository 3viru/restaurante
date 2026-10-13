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

    def actualizar(self, item) -> bool:
        try:
            self.cursor.execute("""
            UPDATE itemmenu
            SET nombre = ?, precioBase = ?, disponible = ?
            WHERE id = ?
            """, (item.nombre, item.precioBase, 1 if item.disponible else 0, item.id))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conexion.rollback()
            raise e

    def eliminar(self, id_item: int) -> bool:
        try:
            # Validación defensiva de integridad referencial:
            try:
                self.cursor.execute("SELECT COUNT(*) FROM detalles_pedido WHERE item_id = ?", (id_item,))
                fila_ped = self.cursor.fetchone()
                if fila_ped and fila_ped[0] > 0:
                    raise ValueError(f"No se puede eliminar el ítem #{id_item} porque registra historial en {fila_ped[0]} comanda(s). Para retirarlo, modifique su disponibilidad a 'Agotado'.")
            except ValueError as ve:
                raise ve
            except Exception:
                pass

            try:
                self.cursor.execute("DELETE FROM bebidas_importadas WHERE id = ?", (id_item,))
            except Exception:
                pass
            try:
                self.cursor.execute("DELETE FROM bebidas WHERE id = ?", (id_item,))
            except Exception:
                pass
            try:
                self.cursor.execute("DELETE FROM platos_calientes WHERE id = ?", (id_item,))
            except Exception:
                pass
            try:
                self.cursor.execute("DELETE FROM postres WHERE id = ?", (id_item,))
            except Exception:
                pass

            self.cursor.execute("DELETE FROM itemmenu WHERE id = ?", (id_item,))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conexion.rollback()
            raise e

    def obtener_por_id(self, id_item: int):
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
        WHERE i.id = ?
        """
        self.cursor.execute(query, (id_item,))
        fila = self.cursor.fetchone()
        if not fila:
            return None
        id_i, nombre, precio_base, disponible, temp_serv, es_alc, pais_origen, req_refrig = fila
        disp_bool = bool(disponible)
        if pais_origen is not None:
            return BebidaImportada(id_i, nombre, precio_base, disp_bool, bool(es_alc), pais_origen)
        elif es_alc is not None:
            return Bebida(id_i, nombre, precio_base, disp_bool, bool(es_alc))
        elif temp_serv is not None:
            return PlatoCaliente(id_i, nombre, precio_base, disp_bool, temp_serv)
        elif req_refrig is not None:
            return Postre(id_i, nombre, precio_base, disp_bool, bool(req_refrig))
        else:
            return ItemMenu(id_i, nombre, precio_base, disp_bool)

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
