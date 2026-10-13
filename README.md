# Sistema de Administración de Restaurante

**Asignatura:** Programación Orientada a Objeto Seguro (TI3V21)  
**Evaluación:** Sumativa N°3 (Unidades 2 y 3: POO, Persistencia y Seguridad en Python)  
**Institución:** INACAP - Sede Puente Alto  
**Docente:** Michael Arjel  

---

## 1. Integrantes y Negocio

### Negocio Asignado
**Sistema de Administración de Restaurante:** Software integral de gestión para restaurante bajo el paradigma de Programación Orientada a Objetos Segura. Administra el catálogo polimórfico de ítems (platos calientes, bebidas nacionales, bebidas importadas y postres), el estado de las mesas, la apertura y seguimiento de pedidos con composición de detalles, la cocina/estaciones de preparación, el consumo de la API de divisas para productos cotizados en moneda extranjera, y la facturación segura con validación de RUT bajo el algoritmo Módulo 11.

### Integrantes del Equipo
- **Integrante 1:** Sáez Otárola, Saúl Misael
- **Integrante 2:** Pérez Brogui, Bastián Mauricio

---

## 2. Cómo instalar y ejecutar el programa, paso a paso, desde un computador que solo tiene Python

El software fue desarrollado para ejecutarse de forma autónoma en cualquier computador que disponga de **Python 3.10 o superior**. Al iniciarse, el sistema crea automáticamente las tablas de la base de datos SQLite y precarga los registros iniciales si no existen.

### Paso 1: Clonar o descargar el repositorio
Descargue el repositorio o clónelo desde la consola:
```bash
git clone https://github.com/3viru/restaurante.git
cd restaurante
```

### Paso 2: (Opcional pero recomendado) Crear un entorno virtual
Para aislar las dependencias del proyecto:
- **En Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **En Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Paso 3: Instalar las dependencias oficiales
El proyecto únicamente requiere la librería oficial `requests` para el consumo de la API económica:
```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar el programa

El sistema ofrece dos modalidades de ejecución:

1. **Modo Demostración Rápida (Suite automatizada de los 5 requisitos de evaluación):**
   Ejecuta secuencialmente la validación de polimorfismo, setters, transacciones, excepciones de dominio y consumo de API externa, terminando de inmediato sin interacción manual:
   ```bash
   python main.py --demo
   ```

2. **Modo Completo e Interactivo (Demostración + Menú de Roles con Persistencia):**
   Ejecuta la suite de verificación técnica y luego permite interactuar con el sistema a través de los roles de **Administrador**, **Mesero** y **Cocinero**:
   ```bash
   python main.py
   ```

### Paso 5: (Alternativa) Ejecutar el programa sin usar la consola (Doble clic en Windows)

Si prefiere ejecutar el sistema de forma visual sin escribir comandos en la terminal:

1. **Opción A (Archivo lanzador .bat - Recomendada):**
   Haga doble clic sobre el archivo `ejecutar.bat` ubicado en la carpeta raíz del proyecto. El programa abrirá automáticamente su ventana interactiva y permanecerá visible al finalizar.

2. **Opción B (Doble clic directo):**
   Haga doble clic directamente sobre el archivo `main.py` en el Explorador de Archivos de Windows para iniciar la aplicación.

---

## 3. Decisiones de Seguridad: Cómo se evita la inyección SQL y qué entradas se validan

### 3.1 Prevención de Inyección SQL (Criterio 2.1.3)
La inyección de código SQL es una de las vulnerabilidades más críticas en aplicaciones con bases de datos relacionales. En este sistema, la inyección SQL se previene de forma total y estricta mediante las siguientes directrices:

1. **Consultas 100% Parametrizadas (Prepared Statements):**
   Ninguna sentencia SQL se construye mediante concatenación de strings (`+`), operadores de formato (`%s`) o plantillas literales (`f-strings`). Todas las consultas utilizan exclusivamente el mecanismo nativo de parametrización de `sqlite3` con marcadores de posición posicionales `?`:
   ```python
   # ❌ VULNERABLE (Descartado totalmente):
   # cursor.execute(f"SELECT * FROM itemmenu WHERE id = {id_usuario}")

   # ✅ SEGURO (Implementado en todas las clases DAO):
   cursor.execute("SELECT * FROM itemmenu WHERE id = ?", (id_item,))
   ```
   De esta manera, el motor de base de datos trata cualquier entrada provista por el usuario estrictamente como un dato literal, neutralizando cualquier intento de inyección de comandos o manipulación de la sintaxis SQL.

2. **Integridad Referencial con Claves Foráneas:**
   En cada apertura de conexión dentro de [`conectar.py`](conectar.py), se fuerza la directiva:
   ```python
   conn.execute("PRAGMA foreign_keys = ON")
   ```
   Esto asegura que SQLite verifique la integridad referencial de los pedidos, detalles de comanda y boletas, impidiendo registros huérfanos o relaciones inconsistentes.

3. **Aislamiento en Capa DAO (Data Access Object):**
   Las sentencias SQL residen exclusivamente dentro de los archivos de la carpeta `dao/`. El modelo de negocio (`model/`) y la capa de presentación (`main.py`) desconocen por completo el dialecto SQL utilizado, garantizando separación de responsabilidades.

---

### 3.2 Validación de Entradas (Criterios 3.1.2 y 3.1.3)

Para garantizar la integridad de los datos y la continuidad del sistema ante errores de los usuarios, se implementó una estrategia de validación en dos capas:

#### A. Validación en los Setters del Modelo de Dominio (`@property` y `@setter`)
Cada clase de negocio encapsula sus atributos privados (`__atributo`) y restringe las mutaciones mediante setters que validan tipo, formato y rango, lanzando `ValueError` o excepciones propias si el dato es inadmisible:

- **`ItemMenu.precioBase.setter`:** Exige que el precio sea un número estrictamente positivo (`> 0`). Si se intenta asignar un valor menor o igual a cero, se rechaza y no se modifica el estado.
- **`ItemMenu.nombre.setter`:** Exige que la cadena no esté vacía ni conformada exclusivamente por espacios en blanco.
- **`Mesa.capacidad.setter`:** Valida que la capacidad sea un entero positivo mayor a 0 personas.
- **`Boleta.rutCliente.setter` y `validarRut()`:** Implementa el algoritmo matemático chileno **Módulo 11** (ponderadores decrecientes 2 a 7 sobre el cuerpo numérico). Si el dígito verificador es incorrecto, el setter rechaza el RUT levantando la excepción propia `RutInvalidoError`.
- **`Boleta.montoNeto.setter`:** Valida que el monto neto sea mayor o igual a cero y recalcula automáticamente el `montoTotal` con el 19% de IVA de manera coherente.

#### B. Validación Defensiva en la Entrada de Usuario (`main.py`)
En la capa de interfaz de consola, las funciones auxiliares `leer_entero()`, `leer_float()`, `leer_texto()` y `leer_confirmacion()` interceptan cualquier dato erróneo antes de enviarlo a la lógica de negocio:
- Si el usuario ingresa texto cuando se solicita un número entero o decimal, se captura la excepción `ValueError`, se despliega un mensaje informativo claro (`"❌ Entrada inválida: debe ingresar un número entero."`) y se vuelve a solicitar el dato sin detener ni abortar el programa.
- Se verifican los rangos mínimos y máximos (por ejemplo, números de mesa válidos o límites de cantidad de productos).

#### C. Tolerancia a Fallos en el Consumo de la API (`servicios/miindicador.py`)
El servicio `MiIndicador` implementa un límite de espera (`timeout = 5` segundos) y maneja de forma controlada las fallas de red:
- **Sin conexión:** `requests.exceptions.ConnectionError`.
- **Tiempo agotado:** `requests.exceptions.Timeout`.
- **Respuestas no válidas:** Errores HTTP o formato JSON corrupto.
Ante cualquiera de estos escenarios, el programa emite una advertencia en pantalla, recurre a un valor referencial de contingencia (`fallback`) y **continúa su funcionamiento sin interrupciones**.

---

## 4. Uso de Inteligencia Artificial: Ejemplos Concretos de Adopción, Modificación y Descarte

Durante el desarrollo de la solución con apoyo de herramientas de IA, se aplicaron criterios técnicos rigurosos para evaluar las recomendaciones generadas:

### 4.1 Ejemplo N°1: Descarte de Flags Booleanos en favor de Excepciones de Dominio (Criterio 2.1.2)
- **Código Inicial Sugerido por la IA:**  
  La IA propuso inicialmente gestionar las reglas de negocio (como la falta de stock de un producto o el intento de abrir una mesa que ya estaba ocupada) utilizando retornos booleanos simples en los métodos:
  ```python
  # Sugerencia inicial descartada:
  def agregarDetalle(self, item, cant):
      if not item.disponible:
          print("Error: Sin stock")
          return False
      # ... agregar detalle
      return True
  ```
- **Decisión y Modificación Técnica Adoptada:**  
  Se **descartó** el uso de retornos centinela (`False`) y validaciones basadas en `print()`. En su lugar, se crearon clases de excepción propias del dominio (`ItemSinStockError`, `MesaOcupadaError`, `PedidoCerradoError`) lanzadas con la instrucción `raise` desde el método responsable y capturadas mediante bloques `try/except` en la capa de coordinación.
- **Razón Técnica:**  
  1. En el desarrollo de software seguro y orientado a objetos, el retorno de valores booleanos no obliga al método invocador a verificar el resultado; si el programador olvida revisar el booleano, el flujo continúa y la aplicación puede operar sobre un estado transaccional inconsistente.
  2. Acoplar la lógica del negocio con impresiones directas en consola (`print`) rompe el principio de responsabilidad única (SRP), impidiendo que el modelo sea reutilizado en interfaces gráficas o servicios web.
  3. El uso de excepciones de dominio desacopla la detección de la anomalía de su tratamiento visual, cumpliendo con la exigencia de programación defensiva establecida en la rúbrica.

---

### 4.2 Ejemplo N°2: Modificación de la Persistencia hacia Consultas Parametrizadas y Transacciones Atómicas (Criterio 2.1.3)
- **Código Inicial Sugerido por la IA:**  
  En los primeros borradores generados por la IA para la sincronización de las líneas de detalle de un pedido en SQLite, se proponían concatenaciones de texto para armar los `INSERT`:
  ```python
  # Sugerencia inicial insegura:
  query = f"INSERT INTO detalles_pedido VALUES ({num_pedido}, {item_id}, {cant})"
  cursor.execute(query)
  ```
- **Decisión y Modificación Técnica Adoptada:**  
  Se **descartó tajantemente** cualquier uso de interpolación de variables dentro de cadenas SQL. Se reformuló toda la capa DAO para emplear exclusivamente tuplas de parámetros con placeholders `?` y transacciones protegidas con bloques `try/except` y `conexion.rollback()`.
- **Razón Técnica:**  
  La interpolación de strings en SQL expone al sistema a inyección SQL directa de segundo orden o manipulación maliciosa de observaciones de pedidos. Al utilizar sentencias parametrizadas, el controlador SQLite compila la instrucción antes de enlazar los valores, garantizando inmunidad frente a cargas maliciosas. Asimismo, el uso de `rollback()` asegura que si falla la inserción de una línea de detalle, la transacción completa se descarte, preservando la consistencia de la base de datos.

---

### 4.3 Ejemplo N°3: Adopción y Ajuste del Patrón Joined Table Inheritance en los DAOs
- **Código Adoptado y Optimizado:**  
  Se adoptó la propuesta de modelar la jerarquía de herencia de `ItemMenu` (`PlatoCaliente`, `Bebida`, `BebidaImportada`, `Postre`) mediante el patrón relacional *Joined Table Inheritance*, donde la tabla `itemmenu` almacena los atributos compartidos y tablas secundarias almacenan los atributos específicos vinculados por clave foránea (`id`).
- **Ajuste Técnico:**  
  Se implementó un método polimórfico `obtener_por_id()` y `listar_todos()` mediante `LEFT JOIN` que analiza qué campos específicos están presentes para instanciar en tiempo de ejecución el subtipo exacto en memoria, combinándolo con el consumo de la API de divisas para calcular dinámicamente los precios de ítems importados.

---

### 4.4 Ejemplo N°4: Detección y Resolución de Casos Borde de Concurrencia y Persistencia (Criterios 2.1.3 y 3.1.3)
- **Problema Analizado con IA:**  
  Durante una auditoría exhaustiva del flujo de producción, la IA detectó que si el programa se reiniciaba mientras existían mesas abiertas, el diccionario en memoria `pedidos_activos` se reiniciaba vacío, dejando las mesas marcadas como "Ocupadas" en SQLite e imposibilitando cerrarlas o agregar ítems desde la consola. Asimismo, detectó riesgos de colisión de identificadores correlativos al abrir múltiples mesas concurrentemente antes de agregar ítems, congelamientos recurrentes de 5 segundos al consultar la API externa sin caché, y posibles fallos de integridad referencial al eliminar productos con ventas históricas.
- **Decisión y Modificación Técnica Adoptada:**  
  1. Se implementó la restauración automática de comandas abiertas en SQLite al arrancar `main()`, permitiendo que el mesero y cocinero continúen atendiendo mesas abiertas tras cualquier reinicio.
  2. Se configuró la persistencia inmediata de cada pedido al momento de abrir la mesa, garantizando correlativos únicos y seguros.
  3. Se incorporó una memoria caché en `MiIndicador` con TTL de 5 minutos, reduciendo las llamadas redundantes a la red y eliminando tiempos de espera en la interfaz.
  4. Se blindó la eliminación en `ItemMenuDao` con validación defensiva en capa de aplicación, orientando al usuario con mensajes claros en vez de exponer excepciones crudas del motor de base de datos.
- **Razón Técnica:**  
  Garantiza la verdadera continuidad operativa del sistema en escenarios reales de restaurante, protegiendo tanto la integridad relacional de la base de datos como la resiliencia de la interfaz de usuario.
