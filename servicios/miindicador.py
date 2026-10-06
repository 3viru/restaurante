import requests

class MiIndicador:
    BASE_URL = "https://mindicador.cl/api/"

    def __init__(self, timeout=5):
        self.__timeout = timeout

    def valor(self, codigo):
        url = self.BASE_URL + codigo
        respuesta = requests.get(url, timeout=self.__timeout)
        datos = respuesta.json()
        return datos["serie"][0]["valor"]
