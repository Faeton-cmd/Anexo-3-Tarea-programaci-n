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