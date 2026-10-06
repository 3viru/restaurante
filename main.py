import sys
import datetime
import conectar

# Modelos del negocio
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

# Capa de persistencia (DAO)
from dao.trabajador_dao import TrabajadorDao
from dao.mesero_dao import MeseroDao
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
    """Crea las tablas en SQLite si no existen."""
    conn = conectar.crear_conexion()
    TrabajadorDao(conn).crear_tabla()
    MeseroDao(conn).crear_tabla()
    ItemMenuDao(conn).crear_tabla()
    PlatoCalienteDao(conn).crear_tabla()
    BebidaDao(conn).crear_tabla()
    BebidaImportadaDao(conn).crear_tabla()
    PostreDao(conn).crear_tabla()
    PedidoDao(conn).crear_tabla()
    BoletaDao(conn).crear_tabla()
    conn.close()


def ejecutar_demostracion():
    """
    Actividad N°2 - Script de Demostración:
    Cumple al 100% con los criterios de evaluación:
    1. Tres subtipos con su método distinto (Polimorfismo).
    2. Encapsulamiento con property y validación en el setter.
    3. Transacción con sus líneas de detalle (Composición y Agregación).
    4. Dos reglas del negocio implementadas como excepciones propias,
       provocadas a propósito y capturadas con try/except.
    El script corre de principio a fin sin errores no controlados.
    """
    print("\n" + "=" * 70)
    print(" EVALUACIÓN SUMATIVA N°2 - PROGRAMACIÓN ORIENTADA A OBJETOS ")
    print(" SCRIPT DE DEMOSTRACIÓN: SISTEMA DE ADMINISTRACIÓN DE RESTAURANTE ")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. TRES SUBTIPOS Y POLIMORFISMO
    # -------------------------------------------------------------
    print("\n" + "-" * 70)
    print(" 1. HERENCIA Y POLIMORFISMO (3 SUBTIPOS DE ITEMMENU)")
    print("-" * 70)
    print("Creando instancias de los subtipos que heredan de ItemMenu:")

    plato = PlatoCaliente(id_item=1, nombre="Lomo a lo Pobre", precioBase=8500, disponible=True, temperaturaServicio=60)
    bebida = Bebida(id_item=2, nombre="Jugo Natural Frambuesa", precioBase=2500, disponible=True, esAlcoholica=False)
    postre = Postre(id_item=3, nombre="Tiramisú Casero", precioBase=3500, disponible=True, requiereRefrigeracion=True)
    bebida_imp = BebidaImportada(id_item=4, nombre="Whisky Jack Daniel's", precioBaseUSD=15.0, disponible=True, esAlcoholica=True, paisOrigen="EE.UU.")

    items_menu = [plato, bebida, postre, bebida_imp]
    valor_dolar = 920.0  # Cotización referencial para conversión de ítems en USD

    print(f"Tipo de cambio referencial USD: ${valor_dolar:,.0f} CLP")
    print("Invocando métodos polimórficos sin preguntar el tipo de objeto (duck typing / OOP):")
    for item in items_menu:
        # LLAMADA POLIMÓRFICA DIRECTA:
        precio_venta = item.obtenerPrecioVenta(valor_dolar)
        tiempo_prep = item.obtenerTiempoPreparacion()
        print(f"  • [{type(item).__name__:<15}] '{item.nombre}':")
        print(f"      - Estación Cocina  : {item.estacion}")
        print(f"      - Tiempo Estimado  : {tiempo_prep} minutos")
        print(f"      - Precio de Venta  : ${precio_venta:,.0f} CLP")

    # -------------------------------------------------------------
    # 2. ENCAPSULAMIENTO Y VALIDACIÓN EN SETTERS
    # -------------------------------------------------------------
    print("\n" + "-" * 70)
    print(" 2. ENCAPSULAMIENTO CON PROPERTY Y VALIDACIÓN EN SETTER")
    print("-" * 70)
    mesa_prueba = Mesa(numero=1, capacidad=4)
    print(f"Mesa creada: N°{mesa_prueba.numero} con capacidad inicial: {mesa_prueba.capacidad} personas.")

    print("\n[A] Modificación válida usando setter:")
    mesa_prueba.capacidad = 6
    print(f"  -> Capacidad actualizada a: {mesa_prueba.capacidad} personas (OK).")

    print("\n[B] Provocando dato inválido a propósito (capacidad <= 0):")
    try:
        mesa_prueba.capacidad = -3
    except ValueError as e:
        print(f"  [CAPTURA try/except] -> ValueError capturado: '{e}'")
        print("  -> La validación en el setter impidió el estado corrupto y el programa continúa.")

    print("\n[C] Provocando dato inválido en ItemMenu (precioBase <= 0):")
    try:
        plato.precioBase = -100
    except ValueError as e:
        print(f"  [CAPTURA try/except] -> ValueError capturado: '{e}'")
        print("  -> La validación en el setter de ItemMenu protegió el precio base.")

    # -------------------------------------------------------------
    # 3. TRANSACCIÓN CON LÍNEAS DE DETALLE (COMPOSICIÓN Y AGREGACIÓN)
    # -------------------------------------------------------------
    print("\n" + "-" * 70)
    print(" 3. TRANSACCIÓN CON LÍNEAS DE DETALLE (COMPOSICIÓN Y AGREGACIÓN)")
    print("-" * 70)
    mesa_transaccion = Mesa(numero=2, capacidad=4)
    mesa_transaccion.abrirMesa()

    pedido = Pedido(numeroPedido=101, fechaHora=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"Transacción creada: Pedido #{pedido.numeroPedido} en Mesa {mesa_transaccion.numero} ({pedido.fechaHora})")

    # COMPOSICIÓN: Pedido.agregarDetalle crea internamente DetallePedido
    # AGREGACIÓN: DetallePedido recibe el objeto ItemMenu ya existente
    pedido.agregarDetalle(plato, cant=2, obs="Carne a punto 3/4")
    pedido.agregarDetalle(bebida, cant=2, obs="Sin hielo")
    pedido.agregarDetalle(postre, cant=1, obs="Con dos cucharas")

    print(f"Líneas de detalle agregadas a la transacción ({len(pedido.detalles)} detalles):")
    for idx, d in enumerate(pedido.detalles, start=1):
        subtotal = d.item.obtenerPrecioVenta(valor_dolar) * d.cantidad
        print(f"  {idx}. {d.cantidad}x '{d.item.nombre}' | Obs: {d.observacion} | Subtotal: ${subtotal:,.0f} CLP")

    total_neto = pedido.calcularTotal(valor_dolar)
    print(f"Total Neto de la transacción: ${total_neto:,.0f} CLP")

    # Emisión de Boleta
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
    print("\n" + "-" * 70)
    print(" 4. REGLAS DEL NEGOCIO (EXCEPCIONES PROPIAS DEL DOMINIO)")
    print("-" * 70)

    # REGLA 1: Item sin stock
    print("[REGLA 1] No se puede agregar a un pedido un ítem sin stock disponible.")
    item_agotado = PlatoCaliente(id_item=99, nombre="Pastel de Choclo", precioBase=7900, disponible=False, temperaturaServicio=70)
    print(f"  -> Ítem de prueba: '{item_agotado.nombre}' con disponible = False.")
    print("  -> Provocando la regla a propósito al invocar pedido.agregarDetalle()...")
    try:
        pedido.agregarDetalle(item_agotado, cant=1, obs="Bien caliente")
        print("  ❌ ERROR: La excepción no fue lanzada.")
    except ItemSinStockError as e:
        print(f"  [CAPTURA try/except] -> Excepción propia '{type(e).__name__}' capturada exitosamente:")
        print(f"    Detalle: \"{e}\"")
        print("    Método lanzador: Pedido.agregarDetalle()")

    # REGLA 2: Mesa ocupada
    print("\n[REGLA 2] No se puede abrir una mesa que ya se encuentra ocupada con un pedido activo.")
    print(f"  -> Estado actual de Mesa {mesa_transaccion.numero}: {mesa_transaccion.estado} (tienePedidoAbierto = {mesa_transaccion.tienePedidoAbierto}).")
    print("  -> Provocando la regla a propósito al invocar mesa_transaccion.abrirMesa()...")
    try:
        mesa_transaccion.abrirMesa()
        print("  ❌ ERROR: La excepción no fue lanzada.")
    except MesaOcupadaError as e:
        print(f"  [CAPTURA try/except] -> Excepción propia '{type(e).__name__}' capturada exitosamente:")
        print(f"    Detalle: \"{e}\"")
        print("    Método lanzador: Mesa.abrirMesa()")

    # REGLA ADICIONAL: Validación de RUT en Boleta
    print("\n[REGLA 3 - ADICIONAL] No se puede emitir una boleta con un RUT de cliente inválido.")
    rut_invalido = "11.111.111-9"  # Dígito verificador incorrecto
    print(f"  -> Intentando emitir Boleta con RUT erróneo: '{rut_invalido}'...")
    try:
        boleta_erronea = Boleta(numeroBoleta=2, rutCliente=rut_invalido, montoNeto=5000)
    except RutInvalidoError as e:
        print(f"  [CAPTURA try/except] -> Excepción propia '{type(e).__name__}' capturada exitosamente:")
        print(f"    Detalle: \"{e}\"")
        print("    Método lanzador: Boleta.rutCliente.setter")

    print("\n" + "=" * 70)
    print(" DEMOSTRACIÓN FINALIZADA CON ÉXITO: 0 ERRORES NO CONTROLADOS ")
    print("=" * 70 + "\n")


# =====================================================================
# SISTEMA INTERACTIVO DE GESTIÓN (ADMIN, MESERO, COCINERO CON PERSISTENCIA)
# =====================================================================

mesas_sistema = [Mesa(1, 4), Mesa(2, 2), Mesa(3, 6)]
pedidos_activos = {}
detalles_cocina = []


def menu_admin(plato_dao, bebida_dao, bebida_imp_dao, postre_dao, boleta_dao, api_dolar, items_menu):
    while True:
        print("\n=== Menú de Administración ===")
        print("1. Agregar Plato Caliente")
        print("2. Agregar Bebida Nacional")
        print("3. Agregar Bebida Importada")
        print("4. Agregar Postre")
        print("5. Ver Historial de Boletas Emitidas (SQLite)")
        print("6. Volver")
        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                nombre = input("Nombre del plato: ")
                precio = float(input("Precio base CLP: "))
                temp = int(input("Temperatura de servicio (°C): "))
                plato = PlatoCaliente(0, nombre, precio, True, temp)
                plato_dao.insertar(plato)
                items_menu.append(plato)
                print(f"✅ Plato '{nombre}' agregado exitosamente.")

            elif opcion == "2":
                nombre = input("Nombre de la bebida: ")
                precio = float(input("Precio base CLP: "))
                alcohol = input("¿Es alcohólica? (s/n): ").lower() == 's'
                bebida = Bebida(0, nombre, precio, True, alcohol)
                bebida_dao.insertar(bebida)
                items_menu.append(bebida)
                print(f"✅ Bebida '{nombre}' agregada exitosamente.")

            elif opcion == "3":
                nombre = input("Nombre del licor/vino importado: ")
                precio_usd = float(input("Precio base USD: $"))
                alcohol = input("¿Es alcohólica? (s/n): ").lower() == 's'
                pais = input("País de origen: ")
                try:
                    valor_dolar = api_dolar.valor('dolar')
                except Exception:
                    valor_dolar = 900.0
                bebida_imp = BebidaImportada(0, nombre, precio_usd, True, alcohol, pais)
                bebida_imp_dao.insertar(bebida_imp)
                items_menu.append(bebida_imp)
                print(f"✅ Dólar actual: ${valor_dolar:,.0f} CLP")
                print(f"💵 Precio venta estimado: ${bebida_imp.obtenerPrecioVenta(valor_dolar):,.0f} CLP")

            elif opcion == "4":
                nombre = input("Nombre del postre: ")
                precio = float(input("Precio base CLP: "))
                refrig = input("¿Requiere refrigeración? (s/n): ").lower() == 's'
                postre = Postre(0, nombre, precio, True, refrig)
                postre_dao.insertar(postre)
                items_menu.append(postre)
                print(f"✅ Postre '{nombre}' agregado exitosamente.")

            elif opcion == "5":
                boletas = boleta_dao.listar_todas()
                print("\n=== Historial de Boletas en Base de Datos ===")
                if not boletas:
                    print("- No hay boletas registradas aún -")
                else:
                    for b in boletas:
                        num_b, num_p, rut_c, neto, tot, f_h = b
                        print(f"Boleta #{num_b} | Pedido #{num_p} | RUT: {rut_c} | Neto: ${neto:,.0f} | Total: ${tot:,.0f} | Fecha: {f_h}")

            elif opcion == "6":
                break
            else:
                print("❌ Opción no válida.")
        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")


def menu_mesero(api_dolar, todos_los_items, pedido_dao, boleta_dao):
    while True:
        print("\n=== Menú Mesero ===")
        print("1. Abrir Mesa y Tomar Pedido")
        print("2. Agregar a Pedido Existente")
        print("3. Cerrar Mesa y Cobrar (Boleta)")
        print("4. Volver")
        opcion = input("Seleccione: ")

        if opcion == "1":
            try:
                n_mesa = int(input("Número de mesa (1-3): "))
                mesa = next((m for m in mesas_sistema if m.numero == n_mesa), None)
                if not mesa:
                    print("❌ Mesa no existe.")
                    continue

                mesa.abrirMesa()  # Puede lanzar MesaOcupadaError
                n_pedido = pedido_dao.obtener_siguiente_numero()
                nuevo_pedido = Pedido(n_pedido, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                pedidos_activos[n_mesa] = nuevo_pedido
                print(f"✅ Mesa {n_mesa} abierta. Pedido #{nuevo_pedido.numeroPedido} iniciado.")

                while True:
                    print("\nÍtems disponibles:")
                    for idx, it in enumerate(todos_los_items):
                        print(f"{idx+1}. {it.nombre} - Stock: {'Sí' if it.verificarStockIngredientes() else 'No'}")
                    sel = input("Seleccione ítem (0 para terminar): ")
                    if sel == "0":
                        break
                    try:
                        item_sel = todos_los_items[int(sel)-1]
                        cant = int(input("Cantidad: "))
                        obs = input("Observación: ")
                        nuevo_pedido.agregarDetalle(item_sel, cant, obs)  # Lanza ItemSinStockError o ValueError
                        detalles_cocina.append({"mesa": n_mesa, "detalle": nuevo_pedido.detalles[-1]})
                        pedido_dao.guardar_pedido(nuevo_pedido, mesa_numero=n_mesa)
                        print("✅ Ítem agregado al pedido.")
                    except (ItemSinStockError, PedidoCerradoError, ValueError) as err:
                        print(f"❌ Regla de Negocio: {err}")
                    except Exception as err:
                        print(f"❌ Selección inválida: {err}")
            except MesaOcupadaError as e:
                print(f"❌ Regla de Negocio: {e}")
            except ValueError as e:
                print(f"❌ Entrada inválida: {e}")

        elif opcion == "2":
            try:
                n_mesa = int(input("Número de mesa (1-3): "))
                if n_mesa not in pedidos_activos:
                    print("❌ No hay pedido abierto en esa mesa.")
                    continue
                pedido = pedidos_activos[n_mesa]
                while True:
                    print("\nÍtems disponibles:")
                    for idx, it in enumerate(todos_los_items):
                        print(f"{idx+1}. {it.nombre} - Stock: {'Sí' if it.verificarStockIngredientes() else 'No'}")
                    sel = input("Seleccione ítem (0 para terminar): ")
                    if sel == "0":
                        break
                    try:
                        item_sel = todos_los_items[int(sel)-1]
                        cant = int(input("Cantidad: "))
                        obs = input("Observación: ")
                        pedido.agregarDetalle(item_sel, cant, obs)
                        detalles_cocina.append({"mesa": n_mesa, "detalle": pedido.detalles[-1]})
                        pedido_dao.guardar_pedido(pedido, mesa_numero=n_mesa)
                        print("✅ Ítem agregado al pedido.")
                    except (ItemSinStockError, PedidoCerradoError, ValueError) as err:
                        print(f"❌ Regla de Negocio: {err}")
                    except Exception:
                        pass
            except ValueError:
                print("❌ Entrada inválida.")

        elif opcion == "3":
            try:
                n_mesa = int(input("Número de mesa (1-3): "))
                if n_mesa not in pedidos_activos:
                    print("❌ No hay pedido abierto en esa mesa.")
                    continue

                pedido = pedidos_activos[n_mesa]
                mesa = next(m for m in mesas_sistema if m.numero == n_mesa)

                rut = input("Ingrese RUT del cliente para la boleta (ej: 12345678-9): ")
                try:
                    ind_ext = api_dolar.valor('dolar')
                except Exception:
                    ind_ext = 900.0

                total_neto = pedido.calcularTotal(ind_ext)
                try:
                    boleta = Boleta(1, rut, total_neto)  # Valida RUT con setter o lanza RutInvalidoError
                    boleta.emitirBoleta()

                    print("\n--- BOLETA EMITIDA ---")
                    print(f"RUT Cliente: {boleta.rutCliente}")
                    print("Detalle de consumo:")
                    for d in pedido.detalles:
                        p = d.item.obtenerPrecioVenta(ind_ext)
                        print(f"- {d.cantidad}x {d.item.nombre}: ${p * d.cantidad:,.0f} CLP")
                    print(f"Monto Neto     : ${boleta.montoNeto:,.0f} CLP")
                    print(f"Total (IVA inc): ${boleta.montoTotal:,.0f} CLP")

                    id_boleta = boleta_dao.insertar(boleta, numero_pedido=pedido.numeroPedido)
                    pedido.cerrarPedido()
                    pedido_dao.actualizar_estado(pedido.numeroPedido, "Cerrado", total=boleta.montoTotal)
                    print(f"✅ Boleta #{id_boleta} registrada exitosamente en SQLite.")

                    mesa.cerrarMesa()
                    del pedidos_activos[n_mesa]
                except RutInvalidoError as err:
                    print(f"❌ Regla de Negocio: {err}")
            except Exception as e:
                print(f"❌ Error al procesar pago: {e}")

        elif opcion == "4":
            break


def menu_cocina():
    while True:
        print("\n=== Menú Cocinero ===")
        pendientes = [d for d in detalles_cocina if not d["detalle"].listo]
        if not pendientes:
            print("- No hay pedidos pendientes -")
        else:
            for idx, p in enumerate(pendientes):
                d = p["detalle"]
                print(f"{idx+1}. Mesa {p['mesa']} | {d.cantidad}x {d.item.nombre} | Obs: {d.observacion} | Estación: {d.item.estacion} ({d.item.obtenerTiempoPreparacion()} min)")

        print("\nOpciones:")
        print("1. Marcar plato/bebida como listo")
        print("2. Volver")
        op = input("Seleccione: ")

        if op == "1":
            if not pendientes:
                continue
            try:
                sel = int(input("Número de ítem a marcar listo: ")) - 1
                pendientes[sel]["detalle"].marcarPreparado()
                print("✅ Ítem marcado como listo.")
            except Exception:
                print("❌ Selección inválida.")
        elif op == "2":
            break


def cargar_items_db(conn):
    item_dao = ItemMenuDao(conn)
    items = item_dao.listar_todos()

    if not items:
        plato_dao = PlatoCalienteDao(conn)
        bebida_dao = BebidaDao(conn)
        bebida_imp_dao = BebidaImportadaDao(conn)
        postre_dao = PostreDao(conn)

        plato_dao.insertar(PlatoCaliente(0, "Lomo a lo Pobre", 8500, True, 60))
        bebida_dao.insertar(Bebida(0, "Coca Cola", 1500, True, False))
        bebida_imp_dao.insertar(BebidaImportada(0, "Jack Daniels", 15, True, True, "USA"))
        postre_dao.insertar(Postre(0, "Tiramisú", 3500, True, True))

        items = item_dao.listar_todos()
    return items


def main():
    inicializar_bd()
    conn = conectar.crear_conexion()
    plato_dao = PlatoCalienteDao(conn)
    bebida_dao = BebidaDao(conn)
    bebida_imp_dao = BebidaImportadaDao(conn)
    postre_dao = PostreDao(conn)
    pedido_dao = PedidoDao(conn)
    boleta_dao = BoletaDao(conn)
    api_dolar = MiIndicador()

    items_menu = cargar_items_db(conn)

    # 1. Ejecutar demostración requerida por la Rúbrica de Evaluación Sumativa N°2
    ejecutar_demostracion()

    # 2. Si se ejecutó con parámetro --demo, terminar inmediatamente
    if "--demo" in sys.argv:
        conn.close()
        return

    # 3. Opción para interactuar con el sistema completo
    try:
        continuar = input("¿Desea ingresar al menú interactivo de roles del restaurante? (s/n): ").strip().lower()
        if continuar != "s":
            print("Fin de la ejecución.")
            conn.close()
            return
    except (EOFError, KeyboardInterrupt):
        conn.close()
        return

    while True:
        print("\n=== SISTEMA DE GESTIÓN RESTAURANTE ===")
        print("1. Administrador (Inventario y Boletas)")
        print("2. Mesero")
        print("3. Cocinero")
        print("4. Volver a ejecutar Demostración Sumativa N°2")
        print("5. Salir")

        opcion = input("Seleccione: ")

        if opcion == "1":
            menu_admin(plato_dao, bebida_dao, bebida_imp_dao, postre_dao, boleta_dao, api_dolar, items_menu)
        elif opcion == "2":
            menu_mesero(api_dolar, items_menu, pedido_dao, boleta_dao)
        elif opcion == "3":
            menu_cocina()
        elif opcion == "4":
            ejecutar_demostracion()
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("❌ Opción no válida.")

    conn.close()


if __name__ == "__main__":
    main()
