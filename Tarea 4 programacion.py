#ejercicio
import datetime
import logging

#configuracion del sistema logs
logging.basicconfiguration(
        filename='sistem_logs.txt',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
)

#Excepcion personalizada
class ErrorSistemaFJ(Exception):
        "excepcion base para el sistema software FJ"
        pass

class DatosInvalidError(ErrorSistemaFJ):
        "se lanza cuando los datos de entrada no cumplen con las validaciones"
        pass

class ServicioNoDisponibleError(ErrorSistemaFJ):
        "Se lanza cuando se intenta contratar un servicio inactivo o inexistente"
        pass

class ReservainvalidError(ErrorSistemaFJ):
        "Se lanza ante conflictos o fallos en la logica de reserva"
        pass

#Clase abstracta
from abc import ABC, abstractmethod

class EntidadBase(ABC):
        def __init__(self, id):
                self.id = id

        @property
        def id(self):
                return self._id

        @abstractmethod
        def obtener_detalles(self):
                pass

#Clase cliente
class Cliente(EntidadBase):
        def __init__(self, id, nombre, correo):
                super().__init__(id)
                self.nombre = nombre
                self.correo = correo

        @property
        def nombre(self):
                return self._nombre

        @nombre.setter
        def nombre(self, valor):
                if not valor:
                        raise DatosInvalidError("El nombre del cliente no puede estar vacío.")
                self._nombre = valor

        @property
        def correo(self):
                return self._correo

        @correo.setter
        def correo(self, valor):
                if "@" not in valor:
                        raise DatosInvalidError("El correo del cliente no es válido.")
                self._correo = valor

        def obtener_detalles(self):
                return f"Cliente ID: {self.id}, Nombre: {self.nombre}, Correo: {self.correo}"

#Clase abstracta servicio
class Servicio(ABC):
        def __init__(self, codigo, nombre_servicio, precio):
                self.id = codigo
                self.nombre = nombre_servicio
                self.precio = precio

        @abstractmethod
        def calcular_costo(self):
                pass

        @abstractmethod
        def obtener_detalles(self):
                pass
        