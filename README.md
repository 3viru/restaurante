# Sistema de Administración de Restaurante

**Asignatura:** Programación Orientada a Objeto Seguro (TI3V21)  
**Evaluación:** Sumativa N°2 (Unidad 2 - POO en Python)  
**Institución:** INACAP  

---

## 📋 Descripción del Proyecto
Software administrativo y de control de comandas para un restaurante, desarrollado en Python bajo el paradigma de **Programación Orientada a Objetos Segura**.

El sistema modela la operación completa entre mesas, garzones (meseros), cocina caliente/fría, barra y caja de facturación con validación de RUT chileno (Módulo 11) y conversión de divisas en tiempo real.

---

## 🚀 Ejecución del Proyecto

Para ejecutar la demostración completa exigida por la **Rúbrica de la Evaluación Sumativa N°2**:

```bash
python main.py
```

El script `main.py`:
1. Ejecuta de forma automática y secuencial la demostración de los **4 criterios clave**:
   - Subtipos y método polimórfico (`obtenerPrecioVenta`, `obtenerTiempoPreparacion`).
   - Encapsulamiento con `@property` y validación en setters (`ValueError` controlado).
   - Transacción con líneas de detalle (**Composición** de `DetallePedido` y **Agregación** de `ItemMenu`).
   - Dos reglas de negocio como excepciones de dominio (`ItemSinStockError` y `MesaOcupadaError`) provocadas a propósito y capturadas con `try/except`.
2. Al finalizar la demostración, ofrece ingresar al **Menú Interactivo de Roles** (Administrador, Mesero, Cocinero) con persistencia en SQLite.

Para correr exclusivamente la suite de demostración y salir:
```bash
python main.py --demo
```

---

## 📂 Estructura del Repositorio

```text
Restaurante/
├── main.py                          # Script principal de demostración y menú interactivo
├── conectar.py                      # Conexión SQLite con PRAGMA foreign_keys = ON
├── restaurante.db                   # Base de datos SQLite
├── requirements.txt                 # Dependencias (requests)
├── README.md                        # Documentación general del repositorio
├── diagrama_clases.mmd              # Definición Mermaid del diagrama de clases UML
├── INFORME_EVALUACION_SUMATIVA_2.md # Borrador completo del informe PDF (Actividad N°3)
├── model/                           # Clases del modelo del negocio (una clase por archivo)
│   ├── trabajador.py                # Clase base Trabajador
│   ├── mesero.py                    # Subclase Mesero
│   ├── cocinero.py                  # Subclase Cocinero
│   ├── itemmenu.py                  # Clase base ItemMenu (validación en setter)
│   ├── platocaliente.py             # Subtipo PlatoCaliente (estación Cocina Caliente)
│   ├── bebida.py                    # Subtipo Bebida (estación Barra)
│   ├── bebidaimportada.py           # Subtipo BebidaImportada (cálculo en USD)
│   ├── postre.py                    # Subtipo Postre (estación Cocina Fría)
│   ├── mesa.py                      # Entidad Mesa (valida capacidad y estado)
│   ├── pedido.py                    # Transacción con composición de detalles
│   ├── detallepedido.py             # Línea de detalle con agregación de ítem
│   ├── boleta.py                    # Facturación con validación Módulo 11 de RUT
│   ├── item_sin_stock_error.py      # Excepción de dominio: Regla 1 (Stock)
│   ├── mesa_ocupada_error.py        # Excepción de dominio: Regla 2 (Mesa ocupada)
│   ├── pedido_cerrado_error.py      # Excepción de dominio: Pedido cerrado
│   └── rut_invalido_error.py        # Excepción de dominio: RUT inválido
├── dao/                             # Capa de persistencia en SQLite
│   ├── dao.py                       # Clase base DAO
│   ├── itemmenu_dao.py              # DAO polimórfico con LEFT JOIN
│   ├── platocaliente_dao.py         # DAO para platos calientes
│   ├── bebida_dao.py                # DAO para bebidas
│   ├── bebidaimportada_dao.py       # DAO para bebidas importadas
│   ├── postre_dao.py                # DAO para postres
│   ├── pedido_dao.py                # DAO para pedidos y líneas de detalle
│   ├── boleta_dao.py                # DAO para boletas emitidas
│   ├── trabajador_dao.py            # DAO para trabajadores
│   └── mesero_dao.py                # DAO para meseros
└── servicios/
    └── miindicador.py               # Servicio REST HTTP hacia mindicador.cl (USD)
```

---

## 📊 Diagrama UML de Clases

Puede visualizarse en el archivo [`diagrama_clases.mmd`](diagrama_clases.mmd) o en [Mermaid Live Editor](https://mermaid.live).

---

## 📝 Documento del Informe

El texto completo estructurado para el **Informe en PDF de la Actividad N°3** se encuentra redactado en [`INFORME_EVALUACION_SUMATIVA_2.md`](INFORME_EVALUACION_SUMATIVA_2.md), listo para ser exportado a PDF adjuntando las capturas de la ejecución.
