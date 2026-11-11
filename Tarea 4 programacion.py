# EJERCICIO
import datetime
import logging
from abc import ABC, abstractmethod

# CONFIGURACION DEL SISTEMA LOGS
logging.basicConfig(
    filename='sistem_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# EXCEPCIONES PERSONALIZADAS
class ErrorSistemaFJ(Exception):
    "Excepcion base para el sistema Software FJ"
    pass

class DatosInvalidError(ErrorSistemaFJ):
    "Se lanza cuando los datos no cumplen con las validaciones"
    pass

class ServicioNoDisponibleError(ErrorSistemaFJ):
    "Se lanza cuando se intenta contratar un servicio no disponible"
    pass

class ReservainvalidError(ErrorSistemaFJ):
    "Se lanza ante conflictos o fallos en una reserva"
    pass


# CLASE ABSTRACTA ENTIDAD BASE
class EntidadBase(ABC):

    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id

    @abstractmethod
    def obtener_detalles(self):
        pass


# CLASE CLIENTE
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
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidError(
                "El nombre del cliente no puede estar vacio."
            )
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str):
            raise DatosInvalidError("El correo no es valido.")

        valor = valor.strip()

        if "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatosInvalidError(
                "El correo del cliente no es valido."
            )

        self._correo = valor

    def obtener_detalles(self):
        return (
            f"Cliente ID: {self.id}, "
            f"Nombre: {self.nombre}, "
            f"Correo: {self.correo}"
        )


# CLASE ABSTRACTA SERVICIO
class Servicio(ABC):

    def __init__(self, codigo, nombre_servicio, precio):
        if not isinstance(nombre_servicio, str) or not nombre_servicio.strip():
            raise DatosInvalidError("El nombre del servicio no es valido.")

        if not isinstance(precio, (int, float)) or isinstance(precio, bool) or precio <= 0:
            raise DatosInvalidError("El precio debe ser mayor que cero.")

        self.id = codigo
        self.nombre = nombre_servicio.strip()
        self.precio = precio
        self.activo = True

    @abstractmethod
    def calcular_costo(self, duracion=1):
        pass

    @abstractmethod
    def obtener_detalles(self):
        pass


# SERVICIO DE RESERVA DE SALAS
class ReservaSalas(Servicio):

    def calcular_costo(self, duracion=1):
        return self.precio * duracion

    def obtener_detalles(self):
        return f"Sala: {self.nombre} - Precio por hora: ${self.precio}"


# SERVICIO DE ALQUILER DE EQUIPOS
class AlquilerEquipos(Servicio):

    def calcular_costo(self, duracion=1):
        return (self.precio * duracion) * 1.10

    def obtener_detalles(self):
        return f"Equipo: {self.nombre} - Precio por dia: ${self.precio}"


# SERVICIO DE ASESORIA ESPECIALIZADA
class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, duracion=1):
        return (self.precio * duracion) * 1.20

    def obtener_detalles(self):
        return f"Asesoria: {self.nombre} - Precio por hora: ${self.precio}"


# CLASE PARA GESTIONAR LAS RESERVAS
class Reserva:

    def __init__(self, codigo, cliente, servicio, duracion):
        if duracion <= 0:
            raise ReservainvalidError(
                "La duracion debe ser mayor que cero."
            )

        self.codigo = codigo
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):
        if not self.servicio.activo:
            raise ServicioNoDisponibleError(
                "El servicio no esta disponible."
            )

        self.estado = "Confirmada"
        logging.info(f"Reserva {self.codigo} confirmada.")

    def cancelar(self):
        self.estado = "Cancelada"
        logging.info(f"Reserva {self.codigo} cancelada.")

    def procesar(self):
        costo = self.servicio.calcular_costo(self.duracion)
        return costo

    def obtener_detalles(self):
        return (
            f"Reserva: {self.codigo}\n"
            f"Cliente: {self.cliente.nombre}\n"
            f"Servicio: {self.servicio.nombre}\n"
            f"Duracion: {self.duracion}\n"
            f"Estado: {self.estado}"
        )


# CLASE PRINCIPAL DEL SISTEMA SOFTWARE FJ
class SistemaSoftwareFJ:

    def __init__(self):
        # LISTAS INTERNAS
        self.clientes = []
        self.servicios = []
        self.reservas = []

    # REGISTRAR CLIENTES
    def registrar_cliente(self, cliente):
        try:
            for c in self.clientes:
                if c.id == cliente.id:
                    raise DatosInvalidError(
                        "El cliente ya esta registrado."
                    )

            self.clientes.append(cliente)
            logging.info(f"Cliente registrado: {cliente.nombre}")
            print("Cliente registrado correctamente.")

        except ErrorSistemaFJ as error:
            logging.error(f"Error al registrar cliente: {error}")
            print(f"Error: {error}")

    # REGISTRAR SERVICIOS
    def registrar_servicio(self, servicio):
        try:
            for s in self.servicios:
                if s.id == servicio.id:
                    raise DatosInvalidError(
                        "El servicio ya esta registrado."
                    )

            self.servicios.append(servicio)
            logging.info(f"Servicio registrado: {servicio.nombre}")
            print("Servicio registrado correctamente.")

        except ErrorSistemaFJ as error:
            logging.error(f"Error al registrar servicio: {error}")
            print(f"Error: {error}")

    # CREAR RESERVAS
    def crear_reserva(self, reserva):
        try:
            if reserva.cliente not in self.clientes:
                raise ReservainvalidError(
                    "El cliente no esta registrado."
                )

            if reserva.servicio not in self.servicios:
                raise ServicioNoDisponibleError(
                    "El servicio no esta registrado."
                )

            self.reservas.append(reserva)
            logging.info(f"Reserva creada: {reserva.codigo}")
            print("Reserva creada correctamente.")

        except ErrorSistemaFJ as error:
            logging.error(f"Error al crear reserva: {error}")
            print(f"Error: {error}")

    # MOSTRAR CLIENTES
    def mostrar_clientes(self):
        for cliente in self.clientes:
            print(cliente.obtener_detalles())

    # MOSTRAR SERVICIOS
    def mostrar_servicios(self):
        for servicio in self.servicios:
            print(servicio.obtener_detalles())

    # MOSTRAR RESERVAS
    def mostrar_reservas(self):
        for reserva in self.reservas:
            print(reserva.obtener_detalles())


# PRUEBAS BASICAS DEL SISTEMA
if __name__ == "__main__":

    sistema = SistemaSoftwareFJ()

    print("\n===== SISTEMA SOFTWARE FJ =====")

    # CREAR CLIENTES
    cliente1 = Cliente(1, "Maria", "maria@gmail.com")
    cliente2 = Cliente(2, "Carlos", "carlos@gmail.com")

    sistema.registrar_cliente(cliente1)
    sistema.registrar_cliente(cliente2)

    # CREAR SERVICIOS
    sala = ReservaSalas(101, "Sala de reuniones", 50000)
    equipo = AlquilerEquipos(102, "Computador", 30000)
    asesoria = AsesoriaEspecializada(
        103, "Asesoria empresarial", 80000
    )

    sistema.registrar_servicio(sala)
    sistema.registrar_servicio(equipo)
    sistema.registrar_servicio(asesoria)

    # CREAR RESERVAS
    reserva1 = Reserva(1, cliente1, sala, 2)
    reserva2 = Reserva(2, cliente2, equipo, 3)

    sistema.crear_reserva(reserva1)
    sistema.crear_reserva(reserva2)

    # CONFIRMAR Y PROCESAR RESERVAS
    reserva1.confirmar()
    reserva2.confirmar()

    print("\n===== COSTOS DE RESERVAS =====")
    print("Costo reserva 1:", reserva1.procesar())
    print("Costo reserva 2:", reserva2.procesar())

    # MOSTRAR INFORMACION
    print("\n===== CLIENTES REGISTRADOS =====")
    sistema.mostrar_clientes()

    print("\n===== SERVICIOS REGISTRADOS =====")
    sistema.mostrar_servicios()

    print("\n===== RESERVAS REGISTRADAS =====")
    sistema.mostrar_reservas()
