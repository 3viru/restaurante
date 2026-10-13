# 🤖 CONTEXTO DEL PROYECTO PARA ASISTENTES IA (SUMATIVA N°3)

> **Propósito del archivo:** Este documento contiene el contexto integral, las especificaciones técnicas, las decisiones arquitectónicas y las directrices académicas del proyecto para que cualquier modelo de Inteligencia Artificial que trabaje en este repositorio en el futuro mantenga la coherencia técnica y cumpla con la rúbrica de evaluación.

---

## 1. Identificación Académica y del Proyecto

- **Institución:** INACAP - Sede Puente Alto
- **Carrera:** Ingeniería en Informática / Ciberseguridad
- **Asignatura:** Programación Orientada a Objeto Seguro (Código: `TI3V21`)
- **Periodo:** Semestre Primavera 2026
- **Docente:** Michael Arjel
- **Evaluación Actual:** **Evaluación Sumativa N°3** (Ponderación: 35 % de la nota final del módulo)
- **Plazo de Entrega:** Martes 13 de octubre de 2026, 23:59 horas (vía repositorio público de GitHub)
- **Negocio Asignado:** **Sistema de Administración de Restaurante**  
  *(Nota aclaratoria: Si el usuario o el entorno menciona "taller mecánico", fue una confusión inicial de digitación. El negocio oficial evaluado es estrictamente **Restaurante**).*

---

## 2. Rúbrica de Evaluación Oficial (Puntaje Máximo: 42 / 42 Puntos - Nota 7.0)

El proyecto está diseñado para alcanzar el nivel **Destacado (7 puntos)** en los 6 indicadores evaluados:

| Criterio | Nombre del Indicador | Nivel Destacado (7 pts) Requerido | Implementación en Código |
| :--- | :--- | :--- | :--- |
| **2.1.2** | Integración del sistema y cobertura de los 5 requisitos | Corre de principio a fin según el README. Cubre los 5 requisitos del negocio. **Las operaciones usan clases del modelo, no diccionarios ni listas sueltas**. | `main.py` con `ejecutar_demostracion()` y menú de roles. Todo detalle de cocina se maneja con objetos `Pedido` y `DetallePedido`. |
| **2.1.3** | Persistencia con DAO y consultas parametrizadas | **CRUD completo** de las entidades principales mediante DAOs separados del modelo. Transacción guardada con líneas de detalle. **Consultas 100% parametrizadas (`?`)**. Creación automática de tablas al iniciar. | Carpeta `dao/` independiente. DAOs con CRUD en `MesaDao`, `ItemMenuDao`, `PedidoDao`, `BoletaDao`, `TrabajadorDao`, `MeseroDao`. `PRAGMA foreign_keys = ON`. |
| **3.1.2** | Validación de entradas y seguridad | Todas las entradas del usuario se validan antes de usarse (tipo, formato, rango). El dato de la ficha se valida en el setter. **Un dato inválido se rechaza con mensaje sin detener el programa**. | Funciones defensivas `leer_entero()`, `leer_float()`, `leer_texto()`. Setters con validaciones (`ItemMenu.precioBase`, `Mesa.capacidad`, `Boleta.rutCliente` con algoritmo **Módulo 11**). |
| **3.1.1** | Consumo de servicios externos (API pública) | El precio usa el valor del indicador obtenido desde API pública con `requests`. Consulta en clase propia, no repartida por el código. | Clase [`servicios/miindicador.py`](servicios/miindicador.py) que consulta `https://mindicador.cl/api/dolar` para calcular precios de `BebidaImportada`. |
| **3.1.3** | Manejo de errores en API y continuidad operativa | **Define un tiempo máximo de espera (`timeout = 5`)**. Sin conexión, demora o respuesta inesperada, el programa informa el problema y sigue funcionando. | `MiIndicador` captura `Timeout`, `ConnectionError`, `HTTPError` y fallos de formato, mostrando advertencia amigable y retornando un fallback de contingencia. |
| **3.1.4** | README con seguridad y uso de IA | El README trae los **cuatro apartados pedidos en el orden exacto**. Decisiones de seguridad explicadas y uso de IA con ejemplos concretos y razones técnicas. | Archivo [`README.md`](README.md) redactado con la estructura oficial: 1) Integrantes y negocio, 2) Instalación paso a paso, 3) Decisiones de seguridad, 4) Uso de IA. |

---

## 3. Cobertura de los Cinco Requisitos Mínimos del Negocio

1. **Tres subtipos con un método polimórfico que se comporta distinto:**
   - Clase base: `ItemMenu` (`model/itemmenu.py`).
   - Subtipos: `PlatoCaliente`, `Bebida`, `BebidaImportada`, `Postre`.
   - Métodos polimórficos: `obtenerPrecioVenta(indExt)` (calcula en CLP o convierte desde USD para importados) y `obtenerTiempoPreparacion()`.
2. **Al menos un dato con validación en el setter:**
   - `ItemMenu.precioBase`: valida número positivo mayor a 0 (`ValueError`).
   - `Mesa.capacidad`: valida entero mayor a 0 (`ValueError`).
   - `Boleta.rutCliente`: valida algoritmo chileno Módulo 11 con ponderadores 2 a 7 (`RutInvalidoError`).
3. **Una transacción con líneas de detalle (Composición y Agregación):**
   - **Composición:** `Pedido` instancia internamente cada objeto `DetallePedido` mediante su método `agregarDetalle()`. Si el pedido se elimina, sus detalles desaparecen.
   - **Agregación:** `DetallePedido` recibe una referencia al objeto preexistente `ItemMenu`. Si el detalle se borra, el ítem del catálogo permanece.
4. **Dos reglas del negocio como excepciones de dominio propias:**
   - Regla 1: No se puede agregar un ítem sin stock disponible -> lanza `ItemSinStockError`.
   - Regla 2: No se puede abrir una mesa que ya está ocupada -> lanza `MesaOcupadaError`.
   - Ambas reglas se provocan a propósito en la suite de prueba y se capturan limpiamente con `try/except`.
5. **Un precio que dependa de un indicador externo:**
   - `BebidaImportada` almacena `precioBaseUSD` y calcula su precio final en CLP multiplicando por la cotización del dólar obtenida desde `mindicador.cl`.

---

## 4. Estructura del Árbol de Archivos

```text
restaurante/
├── main.py                           # Demostración Sumativa N°3 y Menú interactivo por roles
├── conectar.py                       # Conexión SQLite con PRAGMA foreign_keys = ON
├── restaurante.db                    # Base de datos SQLite generada automáticamente
├── requirements.txt                  # Dependencias oficiales (requests)
├── README.md                         # Documentación obligatoria en 4 apartados según rúbrica
├── analisis.md                       # Informe técnico de cambios, código antiguo vs nuevo y matriz P01-P19
├── test_rubrica.py                   # Suite integral de pruebas unitarias automatizadas (13/13 OK)
├── diagrama_clases.mmd               # Definición Mermaid del diagrama de clases UML
├── INFORME_EVALUACION_SUMATIVA_2.md  # Informe histórico de la entrega previa
├── CONTEXTO_PROYECTO_IA.md           # Este archivo (guía de contexto para modelos de IA)
│
├── model/                            # Modelos de dominio orientados a objetos
│   ├── trabajador.py                 # Clase base Trabajador
│   ├── mesero.py                     # Subclase Mesero
│   ├── cocinero.py                   # Subclase Cocinero
│   ├── itemmenu.py                   # Clase base ItemMenu (validación en setter)
│   ├── platocaliente.py              # Subtipo PlatoCaliente
│   ├── bebida.py                     # Subtipo Bebida
│   ├── bebidaimportada.py            # Subtipo BebidaImportada (cálculo dinámico en USD)
│   ├── postre.py                     # Subtipo Postre
│   ├── mesa.py                       # Entidad Mesa (capacidad, estado, pedido activo)
│   ├── pedido.py                     # Transacción con composición de detalles
│   ├── detallepedido.py              # Línea de detalle con agregación de ítem
│   ├── boleta.py                     # Boleta con cálculo de IVA y algoritmo Módulo 11
│   ├── item_sin_stock_error.py       # Excepción de dominio: Regla de stock
│   ├── mesa_ocupada_error.py         # Excepción de dominio: Regla de mesa ocupada
│   ├── pedido_cerrado_error.py       # Excepción de dominio: Regla de pedido cerrado
│   └── rut_invalido_error.py         # Excepción de dominio: Regla de RUT inválido
│
├── dao/                              # Capa de persistencia en SQLite (Patrón DAO)
│   ├── dao.py                        # Clase base DAO con referencia a conexión y cursor
│   ├── mesa_dao.py                   # CRUD completo para la entidad Mesa
│   ├── trabajador_dao.py             # CRUD completo para Trabajador
│   ├── mesero_dao.py                 # CRUD completo para Mesero
│   ├── itemmenu_dao.py               # DAO polimórfico con Joined Table Inheritance (LEFT JOIN)
│   ├── platocaliente_dao.py          # DAO para subtipo PlatoCaliente
│   ├── bebida_dao.py                 # DAO para subtipo Bebida
│   ├── bebidaimportada_dao.py        # DAO para subtipo BebidaImportada
│   ├── postre_dao.py                 # DAO para subtipo Postre
│   ├── pedido_dao.py                 # Persistencia atómica de pedidos y detalles
│   └── boleta_dao.py                 # Persistencia de boletas emitidas
│
└── servicios/
    └── miindicador.py                # Cliente HTTP seguro para mindicador.cl (timeout y fallback)
```

---

## 5. Reglas Inviolables para Asistentes de IA Futuros

Si en el futuro se realizan modificaciones o refactorizaciones sobre este código, **se deben respetar estrictamente las siguientes invariantes técnicas**:

1. **Inyección SQL terminantemente prohibida:**
   - Jamás utilizar interpolación de cadenas (`f"..."`, `format()`, `%s` o `+`) para construir sentencias SQL.
   - Todas las consultas deben usar marcadores de posición parametrizados `?` de `sqlite3`.
2. **Persistencia obligatoria de claves foráneas:**
   - Mantener siempre `conn.execute("PRAGMA foreign_keys = ON")` al abrir conexiones.
3. **Uso estricto de clases del modelo:**
   - No reemplazar objetos del modelo por diccionarios (`dict`) o tuplas sueltas en la lógica del negocio (requisito explícito del Criterio 2.1.2 para obtener 7 puntos).
4. **Validación defensiva en capas:**
   - Los setters deben seguir lanzando `ValueError` o excepciones propias cuando se asignen valores que violen las reglas de integridad.
   - Las funciones de consola (`leer_entero`, `leer_float`) deben capturar errores de usuario para que el programa **nunca aborte** de manera abrupta.
5. **Continuidad operativa de la API:**
   - Cualquier consulta a servicios HTTP externos debe conservar un `timeout` explícito y un mecanismo de contingencia (`fallback`) con mensaje explicativo.
6. **Estructura fija del README.md:**
   - No alterar el orden de los 4 apartados principales del `README.md`, ya que la rúbrica evalúa que aparezcan en esa secuencia exacta.
7. **Preservación de placeholders de integrantes:**
   - La sección 1 del `README.md` (`### Integrantes del Equipo`) debe mantener estrictamente los marcadores de posición `*(Apellido Paterno, Apellido Materno, Nombres - RUT)*`. El usuario los completará manualmente antes de la entrega final. Jamás sobreescribirlos con nombres de prueba ni del Excel.

---

## 6. Registro de Sesión: Auditoría, Refactorización y Guion Docente (Octubre 2026)

Durante la sesión de auditoría con IA se integraron los requerimientos del archivo docente oficial **`06 - Restaurante - Guion de pruebas.xlsx`** (19 pruebas presenciales P01 a P19 que ejecuta el profesor Michael Arjel) y se realizaron las siguientes correcciones de fondo (documentadas en detalle en [`analisis.md`](analisis.md)):

1. **Desacoplamiento de stock en pedidos (P12 y P15):**
   - Se eliminó la instrucción errónea `item.disponible = False` en `model/pedido.py` y `main.py`. Los pedidos cotidianos no deben deshabilitar los platos del catálogo general.
2. **Visor de detalle de pedidos con observaciones (P13):**
   - Se creó la función `mostrar_detalle_pedido()` y se expuso en los menús de Administrador y Mesero, permitiendo consultar los pedidos guardados y ver todas sus líneas con observaciones especiales (ej: `"sin cebolla"`).
3. **Polimorfismo puro con estación de cocina (P09, P10, P11):**
   - Se agregó `@property def estacion(self) -> str: return "Cocina General"` a la clase base `ItemMenu`, evitando `AttributeError` y mostrando estación y tiempos de preparación en el catálogo interactivo.
4. **Compatibilidad en constructores y entidades (`test_rubrica.py`):**
   - `BebidaImportada` ahora soporta `precioBaseUSD` flexiblemente (posicional o kwargs).
   - `Mesa` estandarizó su estado por defecto a `"Disponible"` e incorporó setters para `estado` y `tienePedidoAbierto`.
5. **Mesas 1 a 5 precargadas (P14):**
   - Se garantizó la precarga de la Mesa 4 para la prueba de impedimento de doble comanda activa (`MesaOcupadaError`).
6. **Robustez y arranque limpio (P01, P04, P18, P19):**
   - El sistema arranca directamente en el Menú Principal con opción de demostración formal (`main.py --demo` o mediante la opción 4 del menú).
   - Sanitización para precios en formato chileno (`$9.000` -> `9000.0`).
   - Bloques `else:` en menús de Mesero y Cocinero para entradas fuera de rango (`99`).
7. **Certificación alcanzada:**
   - `test_rubrica.py` pasa 13/13 pruebas unitarias en verde.
   - `main.py --demo` ejecuta la suite de demostración al 100%.
   - `restaurante.db` queda inicializada con esquema limpio y mesas 1 a 5.
   - Archivo [`analisis.md`](analisis.md) generado con el código antiguo vs. código nuevo para trazabilidad docente.
8. **Blindaje Integral contra Casos Borde y Producción (Octubre 2026):**
   - **Persistencia de sesión:** `main()` restaura automáticamente los pedidos activos desde SQLite al iniciar, evitando bloqueo de mesas tras reinicios.
   - **Moneda extranjera:** Visor de pedidos activos calcula el total con la cotización del dólar en vivo (`api_dolar.valor('dolar')`).
   - **Concurrencia de comanda:** Reserva inmediata de pedidos en SQLite evitando colisiones de ID entre mesas.
   - **Cocina sincronizada:** El estado preparado (`listo = 1`) se persiste de inmediato en SQLite desde el menú de cocina.
   - **Sanitización monetaria:** `leer_float()` acepta formatos con signo peso y punto de miles chileno (`$8.500` -> `8500.0`).
   - **Alta disponibilidad:** `MiIndicador` incorpora caché temporal de 5 minutos, eliminando pausas repetitivas de red.
   - **Protección relacional:** `ItemMenuDao.eliminar()` valida defensivamente pedidos históricos antes de borrar, impidiendo caídas por clave foránea.
   - **Identidad de boleta:** `BoletaDao.insertar()` asigna el ID autoincremental al objeto `Boleta.numeroBoleta`.
