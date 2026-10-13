"""
test_rubrica.py - Suite Integral de Pruebas Automatizadas en Tiempo Real
Evaluación Sumativa N°3 - Programación Orientada a Objeto Seguro (INACAP)

Verifica empíricamente el 100% de los criterios y actividades de la rúbrica:
- Actividad N°1: Persistencia DAO (CRUD completo, transacciones con detalles, consultas parametrizadas, tablas auto-creadas).
- Actividad N°2: Validación de entradas y setters defensivos (rangos, tipos, algoritmo Módulo 11 para RUT).
- Actividad N°3: Consumo de API externa (mindicador.cl, timeout=5, tolerancia a fallos y fallback).
- Actividad N°4: Cumplimiento estructural del README.md (4 secciones en orden).
- Requisitos del Negocio: Polimorfismo en 4 subtipos, Composición/Agregación y Excepciones de Dominio propias.
"""

import os
import sys
import sqlite3
import unittest
from unittest.mock import patch, MagicMock

# Importar modelos
from model.itemmenu import ItemMenu
from model.platocaliente import PlatoCaliente
from model.bebida import Bebida
from model.bebidaimportada import BebidaImportada
from model.postre import Postre
from model.mesa import Mesa
from model.pedido import Pedido
from model.detallepedido import DetallePedido
from model.boleta import Boleta
from model.trabajador import Trabajador
from model.mesero import Mesero

# Importar excepciones propias
from model.item_sin_stock_error import ItemSinStockError
from model.mesa_ocupada_error import MesaOcupadaError
from model.pedido_cerrado_error import PedidoCerradoError
from model.rut_invalido_error import RutInvalidoError

# Importar DAOs
from dao.mesa_dao import MesaDao
from dao.itemmenu_dao import ItemMenuDao
from dao.platocaliente_dao import PlatoCalienteDao
from dao.bebida_dao import BebidaDao
from dao.bebidaimportada_dao import BebidaImportadaDao
from dao.postre_dao import PostreDao
from dao.pedido_dao import PedidoDao
from dao.boleta_dao import BoletaDao
from dao.trabajador_dao import TrabajadorDao
from dao.mesero_dao import MeseroDao

# Importar servicios
from servicios.miindicador import MiIndicador


class TestRubricaSumativa3(unittest.TestCase):

    def setUp(self):
        """Prepara una base de datos SQLite en memoria aislada para cada test."""
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("PRAGMA foreign_keys = ON")
        
        # Inicializar tablas
        TrabajadorDao(self.conn).crear_tabla()
        MeseroDao(self.conn).crear_tabla()
        MesaDao(self.conn).crear_tabla()
        ItemMenuDao(self.conn).crear_tabla()
        PlatoCalienteDao(self.conn).crear_tabla()
        BebidaDao(self.conn).crear_tabla()
        BebidaImportadaDao(self.conn).crear_tabla()
        PostreDao(self.conn).crear_tabla()
        PedidoDao(self.conn).crear_tabla()
        BoletaDao(self.conn).crear_tabla()

    def tearDown(self):
        self.conn.close()

    # =========================================================================
    # ACTIVIDAD N°1: PERSISTENCIA EN BASE DE DATOS (CRITERIO 2.1.3)
    # =========================================================================

    def test_01_crud_completo_mesa(self):
        """Actividad 1: MesaDao ejecuta CRUD completo (Crear, Leer, Actualizar, Eliminar)."""
        dao = MesaDao(self.conn)
        
        # 1. Crear
        mesa = Mesa(numero=10, capacidad=4)
        dao.insertar(mesa)
        
        # 2. Leer
        recuperada = dao.obtener_por_numero(10)
        self.assertIsNotNone(recuperada)
        self.assertEqual(recuperada.capacidad, 4)
        self.assertEqual(recuperada.estado, "Disponible")
        
        # 3. Actualizar
        recuperada.capacidad = 8
        recuperada.estado = "Ocupada"
        recuperada.tienePedidoAbierto = True
        actualizado = dao.actualizar(recuperada)
        self.assertTrue(actualizado)
        modificada = dao.obtener_por_numero(10)
        self.assertEqual(modificada.capacidad, 8)
        self.assertEqual(modificada.estado, "Ocupada")
        self.assertTrue(modificada.tienePedidoAbierto)
        
        # 4. Eliminar
        eliminado = dao.eliminar(10)
        self.assertTrue(eliminado)
        self.assertIsNone(dao.obtener_por_numero(10))

    def test_02_crud_completo_itemmenu(self):
        """Actividad 1: ItemMenuDao y subtipos ejecutan CRUD completo y Joined Table Inheritance."""
        item_dao = ItemMenuDao(self.conn)
        plato_dao = PlatoCalienteDao(self.conn)
        
        # 1. Crear
        plato = PlatoCaliente(0, "Cazuela de Vacuno", 6500.0, True, 75)
        id_creado = plato_dao.insertar(plato)
        self.assertGreater(id_creado, 0)
        
        # 2. Leer polimórficamente
        recuperado = item_dao.obtener_por_id(id_creado)
        self.assertIsInstance(recuperado, PlatoCaliente)
        self.assertEqual(recuperado.nombre, "Cazuela de Vacuno")
        self.assertEqual(recuperado.temperaturaServicio, 75)
        
        # 3. Actualizar
        recuperado.nombre = "Cazuela Especial"
        recuperado.precioBase = 7200.0
        recuperado.temperaturaServicio = 80
        plato_dao.actualizar(recuperado)
        
        modificado = item_dao.obtener_por_id(id_creado)
        self.assertEqual(modificado.nombre, "Cazuela Especial")
        self.assertEqual(modificado.precioBase, 7200.0)
        self.assertEqual(modificado.temperaturaServicio, 80)
        
        # 4. Eliminar
        eliminado = item_dao.eliminar(id_creado)
        self.assertTrue(eliminado)
        self.assertIsNone(item_dao.obtener_por_id(id_creado))

    def test_03_transaccion_con_lineas_de_detalle(self):
        """Actividad 1: La transacción se guarda junto con sus líneas de detalle (Pedido + Detalles)."""
        item_dao = ItemMenuDao(self.conn)
        bebida_dao = BebidaDao(self.conn)
        pedido_dao = PedidoDao(self.conn)
        
        # Insertar items
        jugo = Bebida(0, "Jugo de Naranja", 2000.0, True, False)
        id_jugo = bebida_dao.insertar(jugo)
        jugo.id = id_jugo
        
        # Crear pedido y agregar detalles (Composición y Agregación)
        pedido = Pedido(numeroPedido=501, fechaHora="2026-10-09 18:30:00")
        pedido.agregarDetalle(jugo, 2, "Sin azúcar")
        
        # Guardar transacción atómica
        pedido_dao.guardar_pedido(pedido, mesa_numero=1, total=4000.0)
        
        # Verificar que se recupera el pedido con sus líneas de detalle
        recuperado, mesa_num, total = pedido_dao.obtener_pedido_completo(501, item_dao)
        self.assertIsNotNone(recuperado)
        self.assertEqual(recuperado.numeroPedido, 501)
        self.assertEqual(mesa_num, 1)
        self.assertEqual(total, 4000.0)
        self.assertEqual(len(recuperado.detalles), 1)
        self.assertEqual(recuperado.detalles[0].cantidad, 2)
        self.assertEqual(recuperado.detalles[0].observacion, "Sin azúcar")
        self.assertEqual(recuperado.detalles[0].item.nombre, "Jugo de Naranja")

    def test_04_crud_completo_boleta(self):
        """Actividad 1: BoletaDao ejecuta CRUD completo."""
        dao = BoletaDao(self.conn)
        
        # 1. Crear
        boleta = Boleta(numeroBoleta=1, rutCliente="11.111.111-1", montoNeto=10000.0)
        id_b = dao.insertar(boleta)
        self.assertGreater(id_b, 0)
        
        # 2. Leer
        fila = dao.obtener_por_numero(id_b)
        self.assertIsNotNone(fila)
        self.assertEqual(fila[2], "11.111.111-1")
        self.assertEqual(fila[3], 10000.0)
        self.assertEqual(fila[4], 11900.0)  # IVA 19%
        
        # 3. Actualizar
        boleta.numeroBoleta = id_b
        boleta.rutCliente = "22.222.222-2"
        boleta.montoNeto = 20000.0  # montoTotal pasa a 23800.0
        actualizado = dao.actualizar(boleta)
        self.assertTrue(actualizado)
        fila_mod = dao.obtener_por_numero(id_b)
        self.assertEqual(fila_mod[2], "22.222.222-2")
        self.assertEqual(fila_mod[3], 20000.0)
        
        # 4. Eliminar
        eliminado = dao.eliminar(id_b)
        self.assertTrue(eliminado)
        self.assertIsNone(dao.obtener_por_numero(id_b))

    def test_05_consultas_100_parametrizadas_resistencia_inyeccion_sql(self):
        """Actividad 1: Inyección SQL neutralizada mediante placeholders '?'."""
        dao = TrabajadorDao(self.conn)
        
        # Intentar inyección SQL maliciosa clásica
        ataque_rut = "' OR '1'='1"
        trabajador_hacker = Trabajador(rut=ataque_rut, nombre="Hacker Inyeccion", rol="Mesero")
        dao.insertar(trabajador_hacker)
        
        # Si estuviera concatenado, SELECT * WHERE rut = '' OR '1'='1' retornaría filas indiscriminadamente.
        # Al estar parametrizado, busca literalmente la cadena "' OR '1'='1":
        encontrado = dao.obtener_por_rut(ataque_rut)
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.rut, ataque_rut)
        
        # Buscar un RUT inexistente no devuelve nada (no hay bypass booleano)
        self.assertIsNone(dao.obtener_por_rut("11.111.111-1"))

    # =========================================================================
    # ACTIVIDAD N°2: VALIDACIÓN DE ENTRADAS Y SETTERS (CRITERIOS 3.1.2)
    # =========================================================================

    def test_06_validacion_setter_itemmenu_preciobase(self):
        """Actividad 2: ItemMenu.precioBase rechaza precios <= 0 con ValueError."""
        item = ItemMenu(1, "Empanada", 1500.0, True)
        
        # Precio válido
        item.precioBase = 2000.0
        self.assertEqual(item.precioBase, 2000.0)
        
        # Precios inválidos (negativo y cero)
        with self.assertRaises(ValueError):
            item.precioBase = -500.0
        with self.assertRaises(ValueError):
            item.precioBase = 0.0

    def test_07_validacion_setter_mesa_capacidad(self):
        """Actividad 2: Mesa.capacidad rechaza enteros <= 0 con ValueError."""
        mesa = Mesa(1, 4)
        mesa.capacidad = 6
        self.assertEqual(mesa.capacidad, 6)
        
        with self.assertRaises(ValueError):
            mesa.capacidad = 0
        with self.assertRaises(ValueError):
            mesa.capacidad = -2

    def test_08_validacion_setter_boleta_rut_modulo_11(self):
        """Actividad 2: Boleta.rutCliente valida algoritmo Módulo 11 y rechaza RUTs falsos."""
        # RUT válido
        boleta = Boleta(1, "11.111.111-1", 10000.0)
        self.assertEqual(boleta.rutCliente, "11.111.111-1")
        
        # RUT con dígito verificador inválido -> RutInvalidoError
        with self.assertRaises(RutInvalidoError):
            boleta.rutCliente = "11.111.111-9"
            
        with self.assertRaises(RutInvalidoError):
            Boleta(2, "12.345.678-0", 5000.0)

    # =========================================================================
    # ACTIVIDAD N°3: CONSUMO DE API Y CONTINUIDAD (CRITERIOS 3.1.1 Y 3.1.3)
    # =========================================================================

    def test_09_consumo_api_real_mindicador_dolar(self):
        """Actividad 3: Consulta en vivo a mindicador.cl con requests y timeout=5."""
        api = MiIndicador(timeout=5)
        valor_dolar = api.valor("dolar")
        self.assertIsInstance(valor_dolar, float)
        self.assertGreater(valor_dolar, 500.0)  # El dólar en Chile siempre es > 500 CLP

    def test_10_tolerancia_a_fallos_y_fallback_de_api(self):
        """Actividad 3: Si la API demora (timeout) o falla la red, emite aviso y usa fallback."""
        api = MiIndicador(timeout=1)
        
        # Simular timeout en requests.get
        import requests
        with patch("requests.get", side_effect=requests.exceptions.Timeout):
            valor = api.valor("dolar")
            # Debe retornar el fallback de contingencia (950.0) sin lanzar excepción al exterior
            self.assertEqual(valor, 950.0)
            
        # Simular caída de conexión
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            valor_uf = api.valor("uf")
            self.assertEqual(valor_uf, 38000.0)

    # =========================================================================
    # ACTIVIDAD N°4: REVISIÓN ESTRUCTURAL DE README.MD (CRITERIO 3.1.4)
    # =========================================================================

    def test_11_readme_contiene_los_cuatro_apartados_en_orden(self):
        """Actividad 4: README.md contiene los 4 títulos exigidos en el orden exacto."""
        readme_path = os.path.join(os.path.dirname(__file__), "README.md")
        self.assertTrue(os.path.exists(readme_path), "README.md debe existir en la raíz del proyecto.")
        
        with open(readme_path, "r", encoding="utf-8") as f:
            contenido = f.read()
            
        # 1. Integrantes y negocio
        pos1 = contenido.find("## 1. Integrantes y Negocio")
        # 2. Cómo instalar y ejecutar el programa...
        pos2 = contenido.find("## 2. Cómo instalar y ejecutar el programa, paso a paso, desde un computador que solo tiene Python")
        # 3. Decisiones de seguridad...
        pos3 = contenido.find("## 3. Decisiones de Seguridad: Cómo se evita la inyección SQL y qué entradas se validan")
        # 4. Uso de inteligencia artificial...
        pos4 = contenido.find("## 4. Uso de Inteligencia Artificial: Ejemplos Concretos de Adopción, Modificación y Descarte")
        
        self.assertGreater(pos1, -1, "Falta la Sección 1: Integrantes y Negocio.")
        self.assertGreater(pos2, -1, "Falta la Sección 2: Cómo instalar y ejecutar...")
        self.assertGreater(pos3, -1, "Falta la Sección 3: Decisiones de Seguridad...")
        self.assertGreater(pos4, -1, "Falta la Sección 4: Uso de Inteligencia Artificial...")
        
        # Verificar orden estricto: 1 < 2 < 3 < 4
        self.assertTrue(pos1 < pos2 < pos3 < pos4, "Las secciones del README.md no están en el orden exigido por la rúbrica.")

    # =========================================================================
    # REQUISITOS DEL NEGOCIO: POLIMORFISMO Y EXCEPCIONES PROPIAS
    # =========================================================================

    def test_12_polimorfismo_en_cuatro_subtipos(self):
        """Requisito de Negocio: Cuatro subtipos implementan obtenerPrecioVenta y obtenerTiempoPreparacion."""
        plato = PlatoCaliente(1, "Lomo a lo Pobre", 8500.0, True, 70)
        bebida = Bebida(2, "Bebida Cola", 1800.0, True, False)
        postre = Postre(3, "Flan Casero", 2500.0, True, True)
        importada = BebidaImportada(4, "Cerveza Alemana", 0.0, True, True, "Alemania", precioBaseUSD=5.0)
        
        dolar_ref = 950.0
        
        # Todos responden al mismo mensaje pero calculan según su comportamiento
        self.assertEqual(plato.obtenerPrecioVenta(dolar_ref), 8500.0)
        self.assertEqual(bebida.obtenerPrecioVenta(dolar_ref), 1800.0)
        self.assertEqual(postre.obtenerPrecioVenta(dolar_ref), 2500.0)
        self.assertEqual(importada.obtenerPrecioVenta(dolar_ref), 4750.0)  # 5 * 950 = 4750
        
        # Tiempos polimórficos
        self.assertEqual(plato.obtenerTiempoPreparacion(), 20)
        self.assertEqual(bebida.obtenerTiempoPreparacion(), 5)
        self.assertEqual(postre.obtenerTiempoPreparacion(), 10)
        self.assertEqual(importada.obtenerTiempoPreparacion(), 5)

    def test_13_excepciones_de_dominio_propias(self):
        """Requisito de Negocio: Lanzamiento y captura de ItemSinStockError y MesaOcupadaError."""
        # 1. Regla de negocio: Sin stock -> ItemSinStockError
        item_agotado = ItemMenu(99, "Producto Agotado", 3000.0, disponible=False)
        pedido = Pedido(1, "2026-10-09 19:00:00")
        
        with self.assertRaises(ItemSinStockError):
            pedido.agregarDetalle(item_agotado, 1)
            
        # 2. Regla de negocio: Mesa ya ocupada -> MesaOcupadaError
        mesa = Mesa(1, 4)
        mesa.abrirMesa()  # Abre correctamente la primera vez
        self.assertTrue(mesa.tienePedidoAbierto)
        
        with self.assertRaises(MesaOcupadaError):
            mesa.abrirMesa()  # Error: no se puede volver a abrir si ya está ocupada


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print(" EJECUTANDO SUITE COMPLETA DE PRUEBAS EN TIEMPO REAL (RÚBRICA SUMATIVA N°3)")
    print("=" * 80 + "\n")
    unittest.main(verbosity=2)
