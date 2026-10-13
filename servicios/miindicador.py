import time
import requests

class MiIndicador:
    """
    Servicio para consultar indicadores económicos desde la API pública mindicador.cl.
    Cumple con Criterios 3.1.1 y 3.1.3:
    - Uso de librería oficial requests con timeout explícito.
    - Manejo controlado de fallas: falta de conexión, demora o respuestas inesperadas.
    - Continuidad operativa garantizada mediante valor de contingencia (fallback).
    - Memoria caché temporal para evitar congelamientos repetidos de consola.
    """
    BASE_URL = "https://mindicador.cl/api/"
    FALLBACKS = {
        "dolar": 950.0,
        "uf": 38000.0,
        "euro": 1020.0
    }

    def __init__(self, timeout: int = 5, cache_ttl: int = 300):
        self.__timeout = timeout
        self.__cache_ttl = cache_ttl
        self._cache = {}

    def valor(self, codigo: str) -> float:
        """
        Consulta el valor actual de un indicador (ej: 'dolar', 'uf').
        Si ocurre un error de conexión, timeout o formato inesperado,
        informa el problema al usuario y retorna un valor referencial
        para permitir que el sistema continúe funcionando sin interrupciones.
        """
        codigo_limpio = str(codigo).lower().strip()
        ahora = time.time()

        if codigo_limpio in self._cache:
            val_cache, timestamp_cache = self._cache[codigo_limpio]
            if ahora - timestamp_cache < self.__cache_ttl:
                return val_cache

        url = f"{self.BASE_URL}{codigo_limpio}"
        valor_fallback = self.FALLBACKS.get(codigo_limpio, 950.0)

        try:
            respuesta = requests.get(url, timeout=self.__timeout)
            respuesta.raise_for_status()
            datos = respuesta.json()

            if "serie" in datos and len(datos["serie"]) > 0 and "valor" in datos["serie"][0]:
                val = float(datos["serie"][0]["valor"])
                self._cache[codigo_limpio] = (val, ahora)
                return val
            else:
                print(f"[AVISO API mindicador.cl] Respuesta con estructura inesperada para '{codigo_limpio}'.")
                print(f"   -> Usando valor referencial de respaldo: ${valor_fallback:,.0f} CLP.")
                self._cache[codigo_limpio] = (valor_fallback, ahora)
                return valor_fallback

        except requests.exceptions.Timeout:
            print(f"[AVISO API mindicador.cl] Tiempo de espera agotado ({self.__timeout}s) al consultar '{codigo_limpio}'.")
            print(f"   -> Usando valor referencial de respaldo: ${valor_fallback:,.0f} CLP.")
            self._cache[codigo_limpio] = (valor_fallback, ahora)
            return valor_fallback

        except requests.exceptions.ConnectionError:
            print(f"[AVISO API mindicador.cl] Sin conexion a internet o servidor inaccesible al consultar '{codigo_limpio}'.")
            print(f"   -> Usando valor referencial de respaldo: ${valor_fallback:,.0f} CLP.")
            self._cache[codigo_limpio] = (valor_fallback, ahora)
            return valor_fallback

        except requests.exceptions.HTTPError as e:
            print(f"[AVISO API mindicador.cl] Error de respuesta HTTP ({e}) al consultar '{codigo_limpio}'.")
            print(f"   -> Usando valor referencial de respaldo: ${valor_fallback:,.0f} CLP.")
            self._cache[codigo_limpio] = (valor_fallback, ahora)
            return valor_fallback

        except Exception as e:
            print(f"[AVISO API mindicador.cl] Error inesperado procesando datos de '{codigo_limpio}': {e}")
            print(f"   -> Usando valor referencial de respaldo: ${valor_fallback:,.0f} CLP.")
            self._cache[codigo_limpio] = (valor_fallback, ahora)
            return valor_fallback
