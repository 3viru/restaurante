import sys
import datetime
import conectar

# Modelos del negocio (Entidades POO)
from model.itemmenu import ItemMenu
from model.platocaliente import PlatoCaliente
from model.bebida import Bebida
from model.bebidaimportada import BebidaImportada
from model.postre import Postre
from model.mesa import Mesa
from model.pedido import Pedido
from model.detallepedido import DetallePedido
from model.boleta import Boleta

# Excepciones propias del dominio del negocio
from model.item_sin_stock_error import ItemSinStockError
from model.mesa_ocupada_error import MesaOcupadaError
from model.pedido_cerrado_error import PedidoCerradoError
from model.rut_invalido_error import RutInvalidoError

# Capa de persistencia (DAO con SQLite)
from dao.trabajador_dao import TrabajadorDao
from dao.mesero_dao import MeseroDao
from dao.mesa_dao import MesaDao
from dao.itemmenu_dao import ItemMenuDao
from dao.platocaliente_dao import PlatoCalienteDao
from dao.bebida_dao import BebidaDao
from dao.bebidaimportada_dao import BebidaImportadaDao
from dao.postre_dao import PostreDao
from dao.pedido_dao import PedidoDao
from dao.boleta_dao import BoletaDao

# Servicios externos
from servicios.miindicador import MiIndicador


def inicializar_bd():
    """Crea las tablas en SQLite si no existen para garantizar que corra en cualquier equipo (Criterio 2.1.3)."""
    conn = conectar.crear_conexion()
    TrabajadorDao(conn).crear_tabla()
    MeseroDao(conn).crear_tabla()
    MesaDao(conn).crear_tabla()
    ItemMenuDao(conn).crear_tabla()
    PlatoCalienteDao(conn).crear_tabla()
    BebidaDao(conn).crear_tabla()
    BebidaImportadaDao(conn).crear_tabla()
    PostreDao(conn).crear_tabla()
    PedidoDao(conn).crear_tabla()
    BoletaDao(conn).crear_tabla()
    conn.close()


# =====================================================================
# FUNCIONES AUXILIARES DE VALIDACIÓN DEFENSIVA DE ENTRADAS (Criterio 3.1.2)
# =====================================================================

def leer_entero(mensaje: str, min_val: int = None, max_val: int = None) -> int:
    """Valida tipo de dato entero y rango antes de utilizarlo."""
    while True:
        entrada = input(mensaje).strip()
        try:
            val = int(entrada)
            if min_val is not None and val < min_val:
                print(f"❌ Valor inválido: debe ser mayor o igual a {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"❌ Valor inválido: debe ser menor o igual a {max_val}.")
                continue
            return val
        except ValueError:
            print("❌ Entrada inválida: debe ingresar un número entero.")


def leer_float(mensaje: str, min_val: float = None) -> float:
    """Valida tipo numérico real y rango antes de utilizarlo, sanitizando formatos monetarios."""
    while True:
        entrada = input(mensaje).strip()
        val_limpio = entrada.replace("$", "").replace(" ", "")
        if "." in val_limpio and "," in val_limpio:
            val_limpio = val_limpio.replace(".", "").replace(",", ".")
        elif val_limpio.count(".") > 1:
            val_limpio = val_limpio.replace(".", "")
        elif "." in val_limpio and not val_limpio.startswith("0.") and len(val_limpio.split(".")[-1]) == 3:
            # Formato chileno con punto de miles (ej: 8.500 -> 8500)
            val_limpio = val_limpio.replace(".", "")
        else:
            val_limpio = val_limpio.replace(",", ".")
        try:
            val = float(val_limpio)
            if min_val is not None and val < min_val:
                print(f"❌ Valor inválido: debe ser mayor o igual a {min_val}.")
                continue
            return val
        except ValueError:
            print("❌ Entrada inválida: debe ingresar un valor numérico.")


def leer_texto(mensaje: str) -> str:
    """Valida que una cadena no esté vacía."""
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            return entrada
        print("❌ El texto no puede estar vacío.")


def leer_confirmacion(mensaje: str) -> bool:
    """Valida opciones afirmativas o negativas."""
    while True:
        entrada = input(mensaje).strip().lower()
        if entrada in ['s', 'si', 'y']:
            return True
        if entrada in ['n', 'no']:
            return False
        print("❌ Por favor responda con 's' (Sí) o 'n' (No).")


# =====================================================================
# DEMOSTRACIÓN DE CRITERIOS CLAVE (Criterios 2.1.2, 2.1.3, 3.1.1, 3.1.2, 3.1.3)
# =====================================================================

def ejecutar_demostracion(api_dolar: MiIndicador):
    """
    Script de Demostración que verifica los cinco requisitos de la ficha del negocio:
    1. Tres subtipos con un método polimórfico que se comporta distinto.
    2. Encapsulamiento con @property y validación en setter (ValueError capturado).
    3. Transacción con sus líneas de detalle (Composición de DetallePedido y Agregación de ItemMenu).
    4. Dos reglas del negocio como excepciones de dominio capturadas con try/except.
    5. Precio con indicador externo obtenido dinámicamente mediante la API con requests.
    """
    print("\n" + "=" * 75)
    print(" EVALUACIÓN SUMATIVA N°3 - PROGRAMACIÓN ORIENTADA A OBJETO SEGURO ")
    print(" DEMOSTRACIÓN DE CRITERIOS: SISTEMA DE ADMINISTRACIÓN DE RESTAURANTE ")
    print("=" * 75)

    # -------------------------------------------------------------
    # 1. HERENCIA Y POLIMORFISMO (3 SUBTIPOS DE ITEMMENU + API)
    # -------------------------------------------------------------
    print("\n" + "-" * 75)
    print(" 1. HERENCIA Y POLIMORFISMO (MÉTODOS POLIMÓRFICOS Y API EXTERNA)")
    print("-" * 75)
    print("Consultando cotización oficial del dólar desde API mindicador.cl...")
    valor_dolar = api_dolar.valor("dolar")
    print(f"Cotización de referencia USD: ${valor_dolar:,.2f} CLP\n")

    plato = PlatoCaliente(id_item=1, nombre="Lomo a lo Pobre", precioBase=8500, disponible=True, temperaturaServicio=65)
    bebida = Bebida(id_item=2, nombre="Jugo Natural Frambuesa", precioBase=2500, disponible=True, esAlcoholica=False)
    postre = Postre(id_item=3, nombre="Tiramisú Casero", precioBase=3500, disponible=True, requiereRefrigeracion=True)
    bebida_imp = BebidaImportada(id_item=4, nombre="Whisky Jack Daniel's", precioBaseUSD=15.0, disponible=True, esAlcoholica=True, paisOrigen="EE.UU.")

    items_menu = [plato, bebida, postre, bebida_imp]

    print("Invocando métodos polimórficos sin bifurcaciones por tipo (Duck Typing / POO):")
    for item in items_menu:
        precio_venta = item.obtenerPrecioVenta(valor_dolar)
        tiempo_prep = item.obtenerTiempoPreparacion()
        print(f"  • [{type(item).__name__:<15}] '{item.nombre}':")
        print(f"      - Estación Cocina  : {item.estacion}")
        print(f"      - Tiempo Estimado  : {tiempo_prep} minutos")
        print(f"      - Precio de Venta  : ${precio_venta:,.0f} CLP")

    # -------------------------------------------------------------
    # 2. ENCAPSULAMIENTO CON PROPERTY Y VALIDACIÓN EN SETTERS
    # -------------------------------------------------------------
    print("\n" + "-" * 75)
    print(" 2. ENCAPSULAMIENTO CON @property Y VALIDACIÓN DEFENSIVA EN SETTER")
    print("-" * 75)
    mesa_prueba = Mesa(numero=1, capacidad=4)
    print(f"Mesa creada: N°{mesa_prueba.numero} con capacidad inicial: {mesa_prueba.capacidad} personas.")

    print("\n[A] Modificación válida mediante setter:")
    mesa_prueba.capacidad = 6
    print(f"  -> Capacidad actualizada a: {mesa_prueba.capacidad} personas (OK).")

    print("\n[B] Provocando dato inválido a propósito en Mesa (capacidad <= 0):")
    try:
        mesa_prueba.capacidad = -2
    except ValueError as e:
        print(f"  [CAPTURA try/except] -> ValueError capturado: '{e}'")
        print("  -> El setter rechazó el estado corrupto y el programa continúa de forma segura.")

    print("\n[C] Provocando dato inválido en ItemMenu (precioBase <= 0):")
    try:
        plato.precioBase = -500
    except ValueError as e:
        print(f"  [CAPTURA try/except] -> ValueError capturado: '{e}'")
        print("  -> El setter de ItemMenu protegió la integridad del precio base.")

    # -------------------------------------------------------------
    # 3. TRANSACCIÓN CON LÍNEAS DE DETALLE (COMPOSICIÓN Y AGREGACIÓN)
    # -------------------------------------------------------------
    print("\n" + "-" * 75)
    print(" 3. TRANSACCIÓN CON LÍNEAS DE DETALLE (COMPOSICIÓN Y AGREGACIÓN)")
    print("-" * 75)
    mesa_transaccion = Mesa(numero=2, capacidad=4)
    mesa_transaccion.abrirMesa()

    pedido = Pedido(numeroPedido=101, fechaHora=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"Transacción creada: Pedido #{pedido.numeroPedido} en Mesa {mesa_transaccion.numero} ({pedido.fechaHora})")

    # COMPOSICIÓN: Pedido.agregarDetalle instancia internamente el DetallePedido
    # AGREGACIÓN: DetallePedido recibe el objeto ItemMenu preexistente
    pedido.agregarDetalle(plato, cant=2, obs="Carne 3/4")
    pedido.agregarDetalle(bebida, cant=2, obs="Sin hielo")
    pedido.agregarDetalle(postre, cant=1, obs="Dos cucharas")

    print(f"Líneas de detalle agregadas a la transacción ({len(pedido.detalles)} detalles):")
    for idx, d in enumerate(pedido.detalles, start=1):
        subtotal = d.item.obtenerPrecioVenta(valor_dolar) * d.cantidad
        print(f"  {idx}. {d.cantidad}x '{d.item.nombre}' | Obs: {d.observacion} | Subtotal: ${subtotal:,.0f} CLP")

    total_neto = pedido.calcularTotal(valor_dolar)
    print(f"Total Neto de la transacción: ${total_neto:,.0f} CLP")

    # Facturación con validación de RUT
    rut_cliente_valido = "11.111.111-1"
    boleta = Boleta(numeroBoleta=1, rutCliente=rut_cliente_valido, montoNeto=total_neto)
    boleta.emitirBoleta()
    print(f"Boleta #{boleta.numeroBoleta} emitida al RUT {boleta.rutCliente}:")
    print(f"  - Monto Neto : ${boleta.montoNeto:,.0f} CLP")
    print(f"  - IVA (19%)  : ${boleta.montoTotal - boleta.montoNeto:,.0f} CLP")
    print(f"  - Total Final: ${boleta.montoTotal:,.0f} CLP")

    # -------------------------------------------------------------
    # 4. REGLAS DEL NEGOCIO IMPLEMENTADAS COMO EXCEPCIONES PROPIAS
    # -------------------------------------------------------------
    print("\n" + "-" * 75)
    print(" 4. REGLAS DEL NEGOCIO (EXCEPCIONES DE DOMINIO CAPTURADAS)")
    print("-" * 75)

    # REGLA 1: Item sin stock
    print("[REGLA 1] No se puede agregar a un pedido un ítem sin stock disponible.")
    item_agotado = PlatoCaliente(id_item=99, nombre="Pastel de Choclo", precioBase=7900, disponible=False, temperaturaServicio=70)
    print(f"  -> Ítem agotado de prueba: '{item_agotado.nombre}' con disponible = False.")
    try:
        pedido.agregarDetalle(item_agotado, cant=1, obs="Caliente")
    except ItemSinStockError as e:
        print(f"  [CAPTURA try/except] -> Excepción propia '{type(e).__name__}' capturada:")
        print(f"    Mensaje: \"{e}\"")
        print("    Lanzador: Pedido.agregarDetalle()")

    # REGLA 2: Mesa ya ocupada
    print("\n[REGLA 2] No se puede abrir una mesa que ya está ocupada con un pedido activo.")
    print(f"  -> Estado actual Mesa {mesa_transaccion.numero}: {mesa_transaccion.estado} (tienePedidoAbierto = {mesa_transaccion.tienePedidoAbierto}).")
    try:
        mesa_transaccion.abrirMesa()
    except MesaOcupadaError as e:
        print(f"  [CAPTURA try/except] -> Excepción propia '{type(e).__name__}' capturada:")
        print(f"    Mensaje: \"{e}\"")
        print("    Lanzador: Mesa.abrirMesa()")

    # REGLA 3: RUT inválido
    print("\n[REGLA 3 - SEGURIDAD] Validación de RUT de cliente con algoritmo Módulo 11.")
    rut_invalido = "11.111.111-9"
    try:
        Boleta(numeroBoleta=2, rutCliente=rut_invalido, montoNeto=5000)
    except RutInvalidoError as e:
        print(f"  [CAPTURA try/except] -> Excepción propia '{type(e).__name__}' capturada:")
        print(f"    Mensaje: \"{e}\"")
        print("    Lanzador: Boleta.rutCliente.setter")

    print("\n" + "=" * 75)
    print(" DEMOSTRACIÓN FINALIZADA CON ÉXITO: 100% CUMPLIMIENTO DE CRITERIOS ")
    print("=" * 75 + "\n")


def mostrar_detalle_pedido(pedido, mesa_num, total, api_dolar):
    """Muestra todas las líneas de detalle de un pedido (Criterio 2.1.2 y Prueba P13)."""
    valor_dolar = api_dolar.valor('dolar')
    print("\n" + "=" * 65)
    print(f" DETALLE COMPLETO DEL PEDIDO #{pedido.numeroPedido} (Mesa #{mesa_num})")
    print("=" * 65)
    print(f"Fecha/Hora : {pedido.fechaHora}")
    print(f"Estado     : {pedido.estado}")
    print("-" * 65)
    if not pedido.detalles:
        print("  (El pedido no contiene líneas de detalle)")
    else:
        print("Líneas de Detalle del Pedido:")
        for idx, d in enumerate(pedido.detalles, start=1):
            p_unit = d.item.obtenerPrecioVenta(valor_dolar)
            subtot = p_unit * d.cantidad
            obs_str = f" | Obs: '{d.observacion}'" if d.observacion else ""
            est_str = getattr(d.item, 'estacion', 'Cocina General')
            t_prep = d.item.obtenerTiempoPreparacion()
            print(f"  {idx}. {d.cantidad}x '{d.item.nombre}' [{type(d.item).__name__}] -> Subtotal: ${subtot:,.0f} CLP")
            print(f"     Estación: {est_str} ({t_prep} min) | Prep. lista: {'Sí' if d.listo else 'No'}{obs_str}")
    print("-" * 65)
    total_calc = pedido.calcularTotal(valor_dolar)
    print(f"TOTAL ESTIMADO : ${total_calc:,.0f} CLP (Guardado: ${total or 0:,.0f} CLP)")
    print("=" * 65 + "\n")


def menu_admin(item_dao, plato_dao, bebida_dao, bebida_imp_dao, postre_dao, boleta_dao, pedido_dao, mesa_dao, api_dolar):
    """Menú administrativo con CRUD completo de catálogo, mesas y reportes."""
    while True:
        print("\n=== Menú de Administración ===")
        print("1. Agregar Ítem al Catálogo (Plato, Bebida, Postre)")
        print("2. Listar Catálogo Completo (SQLite)")
        print("3. Modificar Ítem del Catálogo")
        print("4. Eliminar Ítem del Catálogo")
        print("5. Gestionar Mesas (CRUD)")
        print("6. Ver Historial de Boletas Emitidas (SQLite)")
        print("7. Ver Historial de Pedidos (SQLite)")
        print("8. Volver al Menú Principal")

        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                print("\n--- Agregar Nuevo Ítem ---")
                print("1. Plato Caliente")
                print("2. Bebida Nacional")
                print("3. Bebida Importada")
                print("4. Postre")
                sub_op = input("Seleccione tipo: ").strip()

                if sub_op == "1":
                    nombre = leer_texto("Nombre del plato: ")
                    precio = leer_float("Precio base CLP: ", min_val=1)
                    temp = leer_entero("Temperatura de servicio (°C): ", min_val=0, max_val=100)
                    plato = PlatoCaliente(0, nombre, precio, True, temp)
                    plato_dao.insertar(plato)
                    print(f"✅ Plato '{nombre}' agregado exitosamente con ID #{plato.id}.")

                elif sub_op == "2":
                    nombre = leer_texto("Nombre de la bebida: ")
                    precio = leer_float("Precio base CLP: ", min_val=1)
                    alcohol = leer_confirmacion("¿Es alcohólica? (s/n): ")
                    bebida = Bebida(0, nombre, precio, True, alcohol)
                    bebida_dao.insertar(bebida)
                    print(f"✅ Bebida '{nombre}' agregada exitosamente con ID #{bebida.id}.")

                elif sub_op == "3":
                    nombre = leer_texto("Nombre de la bebida importada: ")
                    precio_usd = leer_float("Precio base USD: $", min_val=0.1)
                    alcohol = leer_confirmacion("¿Es alcohólica? (s/n): ")
                    pais = leer_texto("País de origen: ")
                    valor_dolar = api_dolar.valor('dolar')
                    bebida_imp = BebidaImportada(0, nombre, precio_usd, True, alcohol, pais)
                    bebida_imp_dao.insertar(bebida_imp)
                    print(f"✅ Dólar actual: ${valor_dolar:,.0f} CLP")
                    print(f"💵 Precio venta estimado: ${bebida_imp.obtenerPrecioVenta(valor_dolar):,.0f} CLP")
                    print(f"✅ Bebida Importada '{nombre}' agregada con ID #{bebida_imp.id}.")

                elif sub_op == "4":
                    nombre = leer_texto("Nombre del postre: ")
                    precio = leer_float("Precio base CLP: ", min_val=1)
                    refrig = leer_confirmacion("¿Requiere refrigeración? (s/n): ")
                    postre = Postre(0, nombre, precio, True, refrig)
                    postre_dao.insertar(postre)
                    print(f"✅ Postre '{nombre}' agregado exitosamente con ID #{postre.id}.")

            elif opcion == "2":
                print("\n=== Catálogo de Ítems en Base de Datos ===")
                actuales = item_dao.listar_todos()
                if not actuales:
                    print("- No hay ítems registrados en el catálogo -")
                else:
                    for it in actuales:
                        estado_stock = "Disponible" if it.disponible else "Agotado"
                        det_extra = ""
                        if isinstance(it, PlatoCaliente):
                            det_extra = f"| Servir a {it.temperaturaServicio}°C"
                        elif isinstance(it, BebidaImportada):
                            det_extra = f"| Origen: {it.paisOrigen} (USD ${it.precioBaseUSD:.2f})"
                        elif isinstance(it, Bebida):
                            det_extra = f"| {'Alcohólica' if it.esAlcoholica else 'Sin alcohol'}"
                        elif isinstance(it, Postre):
                            det_extra = f"| {'Refrigerado' if it.requiereRefrigeracion else 'Ambiente'}"
                        print(f"ID #{it.id:02d} | [{type(it).__name__:<15}] {it.nombre:<22} | ${it.precioBase:>7,.0f} CLP | {estado_stock:<10} | Estación: {it.estacion} ({it.obtenerTiempoPreparacion()} min) {det_extra}")

            elif opcion == "3":
                print("\n=== Modificar Ítem del Catálogo ===")
                id_mod = leer_entero("Ingrese el ID del ítem a modificar: ", min_val=1)
                item_existente = item_dao.obtener_por_id(id_mod)
                if not item_existente:
                    print(f"❌ No existe un ítem con ID #{id_mod}.")
                    continue

                es_importada = isinstance(item_existente, BebidaImportada)
                if es_importada:
                    print(f"Modificando: {item_existente.nombre} (Precio actual: ${item_existente.precioBaseUSD:.2f} USD)")
                else:
                    print(f"Modificando: {item_existente.nombre} (Precio actual: ${item_existente.precioBase:,.0f} CLP)")
                nuevo_nom = input(f"Nuevo nombre (enter para mantener '{item_existente.nombre}'): ").strip()
                if nuevo_nom:
                    item_existente.nombre = nuevo_nom

                prompt_pre = f"Nuevo precio base USD (enter para mantener ${item_existente.precioBaseUSD:.2f} USD): " if es_importada else f"Nuevo precio base CLP (enter para mantener ${item_existente.precioBase:,.0f}): "
                nuevo_pre = input(prompt_pre).strip()
                if nuevo_pre:
                    val_limpio = nuevo_pre.replace("$", "").strip()
                    if "." in val_limpio and "," in val_limpio:
                        val_limpio = val_limpio.replace(".", "").replace(",", ".")
                    elif "." in val_limpio and not val_limpio.startswith("0.") and len(val_limpio.split(".")[-1]) == 3:
                        val_limpio = val_limpio.replace(".", "")
                    else:
                        val_limpio = val_limpio.replace(",", ".")
                    if es_importada:
                        item_existente.precioBaseUSD = float(val_limpio)
                    else:
                        item_existente.precioBase = float(val_limpio)

                nuevo_disp = input("¿Disponible? (s/n, enter para mantener): ").strip().lower()
                if nuevo_disp in ['s', 'si']:
                    item_existente.disponible = True
                elif nuevo_disp in ['n', 'no']:
                    item_existente.disponible = False

                if isinstance(item_existente, PlatoCaliente):
                    plato_dao.actualizar(item_existente)
                elif isinstance(item_existente, BebidaImportada):
                    bebida_imp_dao.actualizar(item_existente)
                elif isinstance(item_existente, Bebida):
                    bebida_dao.actualizar(item_existente)
                elif isinstance(item_existente, Postre):
                    postre_dao.actualizar(item_existente)
                else:
                    item_dao.actualizar(item_existente)

                print(f"✅ Ítem #{id_mod} actualizado exitosamente en SQLite.")

            elif opcion == "4":
                print("\n=== Eliminar Ítem del Catálogo ===")
                id_elim = leer_entero("Ingrese el ID del ítem a eliminar: ", min_val=1)
                item_existente = item_dao.obtener_por_id(id_elim)
                if not item_existente:
                    print(f"❌ No existe un ítem con ID #{id_elim}.")
                    continue

                if leer_confirmacion(f"¿Confirma eliminar definitivamente '{item_existente.nombre}' (ID #{id_elim})? (s/n): "):
                    item_dao.eliminar(id_elim)
                    print(f"✅ Ítem #{id_elim} '{item_existente.nombre}' eliminado de SQLite.")

            elif opcion == "5":
                print("\n=== Gestión de Mesas (CRUD SQLite) ===")
                print("1. Listar Mesas")
                print("2. Registrar Nueva Mesa")
                print("3. Modificar Capacidad de Mesa")
                print("4. Eliminar Mesa")
                sub_m = input("Opción: ").strip()

                if sub_m == "1":
                    mesas = mesa_dao.listar_todas()
                    for m in mesas:
                        print(f"Mesa #{m.numero} | Capacidad: {m.capacidad} pers. | Estado: {m.estado} | Pedido Activo: {'Sí' if m.tienePedidoAbierto else 'No'}")
                elif sub_m == "2":
                    num = leer_entero("Número de nueva mesa: ", min_val=1)
                    if mesa_dao.obtener_por_numero(num):
                        print(f"❌ La mesa #{num} ya existe.")
                    else:
                        cap = leer_entero("Capacidad (personas): ", min_val=1, max_val=20)
                        mesa_dao.insertar(Mesa(num, cap))
                        print(f"✅ Mesa #{num} registrada exitosamente.")
                elif sub_m == "3":
                    num = leer_entero("Número de mesa a modificar: ", min_val=1)
                    mesa_mod = mesa_dao.obtener_por_numero(num)
                    if not mesa_mod:
                        print(f"❌ Mesa #{num} no encontrada.")
                    else:
                        nueva_cap = leer_entero(f"Nueva capacidad (actual {mesa_mod.capacidad}): ", min_val=1, max_val=20)
                        mesa_mod.capacidad = nueva_cap
                        mesa_dao.actualizar(mesa_mod)
                        print(f"✅ Mesa #{num} actualizada.")
                elif sub_m == "4":
                    num = leer_entero("Número de mesa a eliminar: ", min_val=1)
                    if mesa_dao.eliminar(num):
                        print(f"✅ Mesa #{num} eliminada de SQLite.")
                    else:
                        print(f"❌ Mesa #{num} no encontrada.")

            elif opcion == "6":
                boletas = boleta_dao.listar_todas()
                print("\n=== Historial de Boletas en Base de Datos ===")
                if not boletas:
                    print("- No hay boletas registradas aún -")
                else:
                    for b in boletas:
                        num_b, num_p, rut_c, neto, tot, f_h = b
                        print(f"Boleta #{num_b} | Pedido #{num_p} | RUT: {rut_c} | Neto: ${neto:,.0f} | Total: ${tot:,.0f} | Fecha: {f_h}")

            elif opcion == "7":
                pedidos = pedido_dao.listar_pedidos()
                print("\n=== Historial de Pedidos en Base de Datos ===")
                if not pedidos:
                    print("- No hay pedidos registrados aún -")
                else:
                    for p in pedidos:
                        num_p, f_h, est, mesa_num, tot = p
                        print(f"Pedido #{num_p} | Mesa: {mesa_num} | Estado: {est:<7} | Total: ${tot or 0:,.0f} | Fecha: {f_h}")

                    if leer_confirmacion("\n¿Desea consultar las líneas de detalle de algún pedido? (s/n): "):
                        num_con = leer_entero("Ingrese número de pedido a consultar: ", min_val=1)
                        res = pedido_dao.obtener_pedido_completo(num_con, item_dao)
                        if not res:
                            print(f"❌ El pedido #{num_con} no existe.")
                        else:
                            ped_obj, m_num, tot_ped = res
                            mostrar_detalle_pedido(ped_obj, m_num, tot_ped, api_dolar)

            elif opcion == "8":
                break
            else:
                print("❌ Opción no válida.")
        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")


def menu_mesero(mesa_dao, pedido_dao, boleta_dao, item_dao, api_dolar, pedidos_activos):
    """Menú del rol Mesero con validaciones de negocio y transacciones."""
    while True:
        print("\n=== Menú Mesero ===")
        print("1. Abrir Mesa y Tomar Pedido")
        print("2. Agregar Ítem a Pedido Existente")
        print("3. Cerrar Mesa y Cobrar (Emitir Boleta)")
        print("4. Consultar Detalle de un Pedido")
        print("5. Volver al Menú Principal")
        opcion = input("Seleccione: ").strip()

        if opcion == "1":
            try:
                mesas = mesa_dao.listar_todas()
                print("\nMesas registradas en el sistema:")
                for m in mesas:
                    print(f"  • Mesa #{m.numero} | Capacidad: {m.capacidad} | Estado: {m.estado}")

                n_mesa = leer_entero("Seleccione número de mesa: ", min_val=1)
                mesa = mesa_dao.obtener_por_numero(n_mesa)
                if not mesa:
                    print(f"❌ La mesa #{n_mesa} no existe en el sistema.")
                    continue

                mesa.abrirMesa()  # Lanza MesaOcupadaError si está ocupada
                mesa_dao.actualizar_estado(mesa.numero, mesa.estado, mesa.tienePedidoAbierto)

                n_pedido = pedido_dao.obtener_siguiente_numero()
                while any(p.numeroPedido == n_pedido for p in pedidos_activos.values()):
                    n_pedido += 1
                nuevo_pedido = Pedido(n_pedido, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                pedidos_activos[n_mesa] = nuevo_pedido
                pedido_dao.guardar_pedido(nuevo_pedido, mesa_numero=n_mesa)
                print(f"✅ Mesa {n_mesa} abierta. Pedido #{nuevo_pedido.numeroPedido} iniciado.")

                while True:
                    items_actuales = item_dao.listar_todos()
                    print("\nÍtems disponibles en catálogo:")
                    for idx, it in enumerate(items_actuales, start=1):
                        stk = "Disponible" if it.verificarStockIngredientes() else "Sin Stock"
                        print(f"  {idx}. {it.nombre} (${it.precioBase:,.0f} CLP) - [{stk}]")

                    sel = leer_entero("Seleccione ítem (0 para finalizar selección): ", min_val=0, max_val=len(items_actuales))
                    if sel == 0:
                        break

                    item_sel = items_actuales[sel - 1]
                    cant = leer_entero("Cantidad: ", min_val=1, max_val=50)
                    obs = input("Observación (opcional): ").strip()

                    try:
                        nuevo_pedido.agregarDetalle(item_sel, cant, obs)
                        pedido_dao.guardar_pedido(nuevo_pedido, mesa_numero=n_mesa)
                        print(f"✅ {cant}x '{item_sel.nombre}' agregado(s) al Pedido #{nuevo_pedido.numeroPedido}.")
                    except (ItemSinStockError, PedidoCerradoError, ValueError) as err:
                        print(f"❌ Regla de Negocio / Validación: {err}")

            except MesaOcupadaError as e:
                print(f"❌ Regla de Negocio: {e}")
            except Exception as e:
                print(f"❌ Error al abrir mesa: {e}")

        elif opcion == "2":
            try:
                if not pedidos_activos:
                    print("❌ No hay mesas con pedidos abiertos en este momento.")
                    continue

                print("\nMesas con pedidos activos:")
                for m_num in pedidos_activos.keys():
                    print(f"  • Mesa #{m_num}")

                n_mesa = leer_entero("Seleccione mesa: ", min_val=1)
                if n_mesa not in pedidos_activos:
                    print(f"❌ No existe un pedido activo en la mesa #{n_mesa}.")
                    continue

                pedido = pedidos_activos[n_mesa]
                while True:
                    items_actuales = item_dao.listar_todos()
                    print("\nÍtems disponibles en catálogo:")
                    for idx, it in enumerate(items_actuales, start=1):
                        stk = "Disponible" if it.verificarStockIngredientes() else "Sin Stock"
                        print(f"  {idx}. {it.nombre} (${it.precioBase:,.0f} CLP) - [{stk}]")

                    sel = leer_entero("Seleccione ítem (0 para finalizar): ", min_val=0, max_val=len(items_actuales))
                    if sel == 0:
                        break

                    item_sel = items_actuales[sel - 1]
                    cant = leer_entero("Cantidad: ", min_val=1, max_val=50)
                    obs = input("Observación (opcional): ").strip()

                    try:
                        pedido.agregarDetalle(item_sel, cant, obs)
                        pedido_dao.guardar_pedido(pedido, mesa_numero=n_mesa)
                        print(f"✅ {cant}x '{item_sel.nombre}' agregado(s) al pedido.")
                    except (ItemSinStockError, PedidoCerradoError, ValueError) as err:
                        print(f"❌ Regla de Negocio / Validación: {err}")

            except Exception as e:
                print(f"❌ Error: {e}")

        elif opcion == "3":
            try:
                if not pedidos_activos:
                    print("❌ No hay pedidos abiertos para cobrar.")
                    continue

                n_mesa = leer_entero("Número de mesa a cerrar y cobrar: ", min_val=1)
                if n_mesa not in pedidos_activos:
                    print(f"❌ No hay pedido abierto en la mesa #{n_mesa}.")
                    continue

                pedido = pedidos_activos[n_mesa]
                mesa = mesa_dao.obtener_por_numero(n_mesa)

                if not pedido.detalles:
                    if leer_confirmacion("⚠️ La mesa no tiene consumos registrados. ¿Desea anular el pedido y liberar la mesa? (s/n): "):
                        pedido_dao.eliminar_pedido(pedido.numeroPedido)
                        if mesa:
                            mesa.cerrarMesa()
                            mesa_dao.actualizar_estado(mesa.numero, mesa.estado, mesa.tienePedidoAbierto)
                        del pedidos_activos[n_mesa]
                        print(f"✅ Pedido #{pedido.numeroPedido} anulado y Mesa #{n_mesa} liberada exitosamente.")
                        continue

                rut = leer_texto("Ingrese RUT del cliente para la boleta (ej: 11.111.111-1 o 12345678-9): ")
                valor_dolar = api_dolar.valor('dolar')
                total_neto = pedido.calcularTotal(valor_dolar)

                try:
                    boleta = Boleta(1, rut, total_neto)
                    boleta.emitirBoleta()

                    print("\n" + "=" * 45)
                    print("            BOLETA ELECTRÓNICA")
                    print("=" * 45)
                    print(f"Fecha/Hora : {pedido.fechaHora}")
                    print(f"Mesa       : #{n_mesa}")
                    print(f"RUT Cliente: {boleta.rutCliente}")
                    print("-" * 45)
                    print("Detalle de Consumo:")
                    for d in pedido.detalles:
                        p_unit = d.item.obtenerPrecioVenta(valor_dolar)
                        print(f"  • {d.cantidad}x {d.item.nombre:<20} ${p_unit * d.cantidad:>8,.0f} CLP")
                    print("-" * 45)
                    print(f"Monto Neto     : ${boleta.montoNeto:>12,.0f} CLP")
                    print(f"IVA (19%)      : ${boleta.montoTotal - boleta.montoNeto:>12,.0f} CLP")
                    print(f"TOTAL A PAGAR  : ${boleta.montoTotal:>12,.0f} CLP")
                    print("=" * 45)

                    id_boleta = boleta_dao.insertar(boleta, numero_pedido=pedido.numeroPedido)
                    boleta.numeroBoleta = id_boleta
                    pedido.cerrarPedido()
                    pedido_dao.actualizar_estado(pedido.numeroPedido, "Cerrado", total=boleta.montoTotal)

                    if mesa:
                        mesa.cerrarMesa()
                        mesa_dao.actualizar_estado(mesa.numero, mesa.estado, mesa.tienePedidoAbierto)

                    del pedidos_activos[n_mesa]
                    print(f"✅ Boleta #{id_boleta} emitida y registrada exitosamente en SQLite.")
                    print(f"✅ Mesa #{n_mesa} liberada para nuevos clientes.")

                except RutInvalidoError as err:
                    print(f"❌ Regla de Negocio / Seguridad: {err}")
                    print("   -> La boleta no fue emitida. El pedido sigue abierto.")

            except Exception as e:
                print(f"❌ Error al liquidar la mesa: {e}")

        elif opcion == "4":
            try:
                num_ped = leer_entero("Ingrese número de pedido a consultar: ", min_val=1)
                res = pedido_dao.obtener_pedido_completo(num_ped, item_dao)
                if not res:
                    # Si aún no se guardó en BD, buscar en pedidos_activos
                    encontrado = False
                    for m_num, p_act in pedidos_activos.items():
                        if p_act.numeroPedido == num_ped:
                            valor_dolar = api_dolar.valor('dolar')
                            mostrar_detalle_pedido(p_act, m_num, p_act.calcularTotal(valor_dolar), api_dolar)
                            encontrado = True
                            break
                    if not encontrado:
                        print(f"❌ No se encontró ningún pedido con el número #{num_ped}.")
                else:
                    ped_obj, m_num, tot_ped = res
                    mostrar_detalle_pedido(ped_obj, m_num, tot_ped, api_dolar)
            except Exception as e:
                print(f"❌ Error al consultar pedido: {e}")

        elif opcion == "5":
            break
        else:
            print("❌ Opción no válida. Intente nuevamente.")


def menu_cocina(pedidos_activos, pedido_dao=None):
    """Menú del rol Cocinero operando exclusivamente sobre objetos del modelo (Criterio 2.1.2)."""
    while True:
        print("\n=== Menú Cocinero / Estaciones ===")
        pendientes = []
        # Consultar directamente los objetos Pedido y sus DetallePedido
        for n_mesa, pedido in pedidos_activos.items():
            for det in pedido.detalles:
                if not det.listo:
                    pendientes.append((n_mesa, det))

        if not pendientes:
            print("- No hay ítems pendientes de preparación en cocina -")
        else:
            print("Ítems en espera de preparación:")
            for idx, (n_mesa, det) in enumerate(pendientes, start=1):
                tiempo = det.item.obtenerTiempoPreparacion()
                est = getattr(det.item, 'estacion', 'Cocina General')
                obs_txt = f" | Obs: '{det.observacion}'" if det.observacion else ""
                print(f"  {idx}. [Mesa #{n_mesa}] {det.cantidad}x '{det.item.nombre}' | Estación: {est} ({tiempo} min){obs_txt}")

        print("\nOpciones:")
        print("1. Marcar ítem como preparado / listo")
        print("2. Volver al Menú Principal")
        op = input("Seleccione: ").strip()

        if op == "1":
            if not pendientes:
                print("❌ No hay ítems en preparación para marcar.")
                continue
            sel = leer_entero(f"Seleccione número de ítem listo (1-{len(pendientes)}): ", min_val=1, max_val=len(pendientes))
            n_mesa_sel, det_sel = pendientes[sel - 1]
            det_sel.marcarPreparado()
            if pedido_dao and n_mesa_sel in pedidos_activos:
                pedido_dao.guardar_pedido(pedidos_activos[n_mesa_sel], mesa_numero=n_mesa_sel)
            print(f"✅ Ítem '{det_sel.item.nombre}' marcado como preparado.")
        elif op == "2":
            break
        else:
            print("❌ Opción no válida. Intente nuevamente.")


# =====================================================================
# INICIALIZACIÓN DE DATOS PREDEFINIDOS
# =====================================================================

def cargar_datos_iniciales(conn):
    """Garantiza la existencia de mesas y catálogo inicial al ejecutar en un computador nuevo."""
    mesa_dao = MesaDao(conn)
    mesas = mesa_dao.listar_todas()
    if not mesas:
        mesa_dao.insertar(Mesa(1, 4))
        mesa_dao.insertar(Mesa(2, 2))
        mesa_dao.insertar(Mesa(3, 6))
        mesa_dao.insertar(Mesa(4, 4))
        mesa_dao.insertar(Mesa(5, 4))
    else:
        # Asegurar que las mesas 1 a 5 existan (incluyendo Mesa 4 para la prueba P14)
        for num_m, cap_m in [(1, 4), (2, 2), (3, 6), (4, 4), (5, 4)]:
            if not mesa_dao.obtener_por_numero(num_m):
                mesa_dao.insertar(Mesa(num_m, cap_m))

    item_dao = ItemMenuDao(conn)
    items = item_dao.listar_todos()
    if not items:
        PlatoCalienteDao(conn).insertar(PlatoCaliente(0, "Lomo a lo Pobre", 8500, True, 65))
        BebidaDao(conn).insertar(Bebida(0, "Jugo Natural Frambuesa", 2500, True, False))
        BebidaImportadaDao(conn).insertar(BebidaImportada(0, "Whisky Jack Daniel's", 15.0, True, True, "EE.UU."))
        PostreDao(conn).insertar(Postre(0, "Tiramisú Casero", 3500, True, True))


# =====================================================================
# PUNTO DE ENTRADA PRINCIPAL
# =====================================================================

def main():
    inicializar_bd()
    conn = conectar.crear_conexion()
    cargar_datos_iniciales(conn)

    plato_dao = PlatoCalienteDao(conn)
    bebida_dao = BebidaDao(conn)
    bebida_imp_dao = BebidaImportadaDao(conn)
    postre_dao = PostreDao(conn)
    pedido_dao = PedidoDao(conn)
    boleta_dao = BoletaDao(conn)
    item_dao = ItemMenuDao(conn)
    mesa_dao = MesaDao(conn)
    api_dolar = MiIndicador(timeout=5)

    # Si se pasa el argumento --demo, ejecutar la demostración formal y salir
    if "--demo" in sys.argv:
        ejecutar_demostracion(api_dolar)
        conn.close()
        return

    # Diccionario de pedidos activos por mesa: clave = n_mesa, valor = objeto Pedido
    pedidos_activos = {}

    # Restaurar pedidos activos que hayan quedado abiertos en SQLite para continuidad operativa
    pedidos_abiertos = pedido_dao.listar_pedidos_abiertos()
    for num_p, m_num in pedidos_abiertos:
        if m_num:
            res = pedido_dao.obtener_pedido_completo(num_p, item_dao)
            if res:
                ped_obj, _, _ = res
                pedidos_activos[m_num] = ped_obj

    while True:
        print("\n=== SISTEMA DE ADMINISTRACIÓN DE RESTAURANTE 'SABORES DEL SUR' ===")
        print("1. Administrador (Catálogo, Mesas y Reportes SQLite)")
        print("2. Mesero (Atención de Mesas, Pedidos y Boletas)")
        print("3. Cocinero (Visualización y Preparación en Cocina)")
        print("4. Ejecutar Demostración de Criterios (Sumativa N°3)")
        print("5. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            menu_admin(item_dao, plato_dao, bebida_dao, bebida_imp_dao, postre_dao, boleta_dao, pedido_dao, mesa_dao, api_dolar)
        elif opcion == "2":
            menu_mesero(mesa_dao, pedido_dao, boleta_dao, item_dao, api_dolar, pedidos_activos)
        elif opcion == "3":
            menu_cocina(pedidos_activos, pedido_dao)
        elif opcion == "4":
            ejecutar_demostracion(api_dolar)
        elif opcion == "5":
            print("Saliendo del sistema de administración. ¡Buen servicio!")
            break
        else:
            print("❌ Opción no válida. Intente nuevamente.")

    conn.close()


if __name__ == "__main__":
    main()
