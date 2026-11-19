# EJERCICIO
import datetime
import logging
from abc import ABC, abstractmethod

# CONFIGURACION DEL SISTEMA LOGS
#Ejercicio tarea 4 de programación Steven Morales
import datetime
import logging
import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod

# Configuración del sistema de logs
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

# Excepciones personalizadas para el sistema software FJ
class ErrorSistemaFJ(Exception):
    """Excepción base para el sistema software FJ"""
    pass

class DatosInvalidError(ErrorSistemaFJ):
    """Se lanza cuando los datos de entrada no cumplen con las validaciones"""
    pass

class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta contratar un servicio inactivo o inexistente"""
    pass

class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza ante conflictos o fallos en la lógica de reserva"""
    pass

# clase abstracta entidad base
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

# clase cliente
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
        if not valor.strip():
            raise DatosInvalidError("El nombre del cliente no puede estar vacío.")
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
        if "@" not in valor or "." not in valor:
            raise DatosInvalidError("El correo del cliente no es válido.")
        self._correo = valor.strip()

    def obtener_detalles(self):
        return f"ID: {self.id} | Nombre: {self.nombre} | Correo: {self.correo}"

#clase abstracta servicio
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
class ReservaSala(Servicio):
    def __init__(self, codigo, nombre_servicio, precio, capacidad):
        super().__init__(codigo, nombre_servicio, precio)
        self.capacidad = capacidad

    def calcular_costo(self, horas: int, descuento: float = 0.0):
        try:
            if horas <= 0:
                raise DatosInvalidError("La cantidad de horas debe ser mayor a cero.")
            costo_base = self.precio * horas
            return costo_base * (1 - descuento)
        except DatosInvalidError as e:
            logging.error(f"Error al calcular costo de sala: {e}")
            raise

    def obtener_detalles(self):
        return f"[Sala] {self.nombre} (Cap: {self.capacidad}) - ${self.precio}/hora"

class AlquilerEquipo(Servicio):
    def __init__(self, codigo, nombre_servicio, costo_base, tipo_equipo):
        super().__init__(codigo, nombre_servicio, costo_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, dias: int, seguro: bool = True):
        try:
            if dias <= 0:
                raise DatosInvalidError("Los días de alquiler deben ser mayores a cero.")
            total = self.precio * dias
            if seguro:
                total += 20.0
            return total
        except DatosInvalidError as e:
            logging.error(f"Error calculando costo de equipo: {e}")
            raise

    def obtener_detalles(self):
        return f"[Equipo] {self.nombre} ({self.tipo_equipo}) - ${self.precio}/día"

class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo, nombre_servicio, costo_base, area):
        super().__init__(codigo, nombre_servicio, costo_base)
        self.area = area

    def calcular_costo(self, sesiones: int, impuesto_iva: float = 0.19):
        try:
            if sesiones <= 0:
                raise DatosInvalidError("Las sesiones deben ser mayores a cero.")
            subtotal = self.precio * sesiones
            return subtotal * (1 + impuesto_iva)
        except DatosInvalidError as e:
            logging.error(f"Error calculando costo de asesoría: {e}")
            raise

    def obtener_detalles(self):
        return f"[Asesoría] {self.nombre} (Área: {self.area}) - ${self.precio}/sesión"

# clase reserva
class Reserva:
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, cantidad_tiempo: int):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad_tiempo = cantidad_tiempo
        self.estado = "Creada"
        self.costo_total = 0.0

    def procesar_reserva(self):
        try:
            logging.info(f"Iniciando procesamiento de reserva {self.id_reserva}")
            if not isinstance(self.cliente, Cliente):
                raise ReservaInvalidaError("La reserva no tiene un cliente válido asociado.")

            if isinstance(self.servicio, ReservaSala):
                self.costo_total = self.servicio.calcular_costo(self.cantidad_tiempo, descuento=0.1)
            elif isinstance(self.servicio, AlquilerEquipo):
                self.costo_total = self.servicio.calcular_costo(self.cantidad_tiempo, seguro=True)
            elif isinstance(self.servicio, AsesoriaEspecializada):
                self.costo_total = self.servicio.calcular_costo(self.cantidad_tiempo)
            else:
                raise ServicioNoDisponibleError("El tipo de servicio no es reconocido.")

            self.estado = "Confirmada"
            logging.info(f"Reserva {self.id_reserva} confirmada. Total: ${self.costo_total:.2f}")
            return True, f"¡Reserva {self.id_reserva} confirmada con éxito!\nCosto Total: ${self.costo_total:.2f}"

        except (ReservaInvalidaError, ServicioNoDisponibleError, DatosInvalidError) as e:
            self.estado = "Fallida"
            logging.error(f"Excepción controlada en reserva {self.id_reserva}: {e}")
            return False, f"Error Controlado: {e}"
        except Exception as e:
            self.estado = "Error Crítico"
            logging.critical(f"Error inesperado en reserva {self.id_reserva}: {e}")
            return False, f"Error Crítico: {e}"


# Aplicacion grafica 
class AppSoftwareFJ:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Sistema Integral de Gestión")
        self.root.geometry("650x500")
        self.root.config(bg="#f0f0f0")

        # Almacenamiento en memoria (Listas internas exigidas por la guía)
        self.clientes = {}
        self.servicios = {
            "Sala Ejecutiva (Sala)": ReservaSala("S01", "Sala Ejecutiva", 50.0, 10),
            "Laptop Gamer (Equipo)": AlquilerEquipo("E01", "Laptop Gamer", 30.0, "Cómputo"),
            "Consultoría Arquitectura (Asesoría)": AsesoriaEspecializada("A01", "Consultoría Arquitectura", 100.0, "Ingeniería")
        }

        # Estilo con Pestañas (Notebook)
        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_clientes = ttk.Frame(notebook)
        self.tab_servicios = ttk.Frame(notebook)
        self.tab_reservas = ttk.Frame(notebook)

        notebook.add(self.tab_clientes, text=" Gestión de Clientes")
        notebook.add(self.tab_servicios, text=" Servicios Disponibles")
        notebook.add(self.tab_reservas, text=" Gestión de Reservas")

        self.crear_pestana_clientes()
        self.crear_pestana_servicios()
        self.crear_pestana_reservas()

    def crear_pestana_clientes(self):
        frame = ttk.LabelFrame(self.tab_clientes, text=" Registrar Nuevo Cliente ")
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        ttk.Label(frame, text="ID Cliente:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.txt_id_cliente = ttk.Entry(frame, width=30)
        self.txt_id_cliente.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Nombre Completo:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.txt_nombre_cliente = ttk.Entry(frame, width=30)
        self.txt_nombre_cliente.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Correo Electrónico:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.txt_correo_cliente = ttk.Entry(frame, width=30)
        self.txt_correo_cliente.grid(row=2, column=1, padx=10, pady=10)

        btn_registrar = ttk.Button(frame, text="Guardar Cliente", command=self.registrar_cliente)
        btn_registrar.grid(row=3, column=0, columnspan=2, pady=15)

        # Listado visual de clientes
        self.lbl_lista_clientes = tk.Text(frame, height=8, width=55)
        self.lbl_lista_clientes.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.lbl_lista_clientes.insert(tk.END, "Clientes registrados aparecerán aquí...\n")
        self.lbl_lista_clientes.config(state=tk.DISABLED)

    def registrar_cliente(self):
        id_c = self.txt_id_cliente.get()
        nombre = self.txt_nombre_cliente.get()
        correo = self.txt_correo_cliente.get()

        try:
            if not id_c.strip():
                raise DatosInvalidError("El ID del cliente no puede estar vacío.")
            
            nuevo_cli = Cliente(id_c, nombre, correo)
            self.clientes[id_c] = nuevo_cli
            
            messagebox.showinfo("Éxito", f"Cliente {nombre} registrado correctamente.")
            logging.info(f"Cliente registrado vía Tkinter: {id_c}")
            
            # Actualizar caja de texto
            self.lbl_lista_clientes.config(state=tk.NORMAL)
            self.lbl_lista_clientes.insert(tk.END, f"{nuevo_cli.obtener_detalles()}\n")
            self.lbl_lista_clientes.config(state=tk.DISABLED)

            # Limpiar campos
            self.txt_id_cliente.delete(0, tk.END)
            self.txt_nombre_cliente.delete(0, tk.END)
            self.txt_correo_cliente.delete(0, tk.END)

        except DatosInvalidError as e:
            messagebox.showerror("Error de Validación", str(e))
            logging.warning(f"Error registrando cliente: {e}")
        except Exception as e:
            messagebox.showerror("Error Crítico", str(e))

    def crear_pestana_servicios(self):
        frame = ttk.LabelFrame(self.tab_servicios, text=" Catálogo de Servicios Software FJ ")
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.txt_servicios_info = tk.Text(frame, height=12, width=60)
        self.txt_servicios_info.pack(padx=10, pady=10)
        
        detalles_texto = "Servicios prediseñados en el sistema:\n\n"
        for key, servicio in self.servicios.items():
            detalles_texto += f"• {key} ➔ {servicio.obtener_detalles()}\n"

        self.txt_servicios_info.insert(tk.END, detalles_texto)
        self.txt_servicios_info.config(state=tk.DISABLED)

    def crear_pestana_reservas(self):
        frame = ttk.LabelFrame(self.tab_reservas, text=" Procesar Nueva Reserva ")
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        ttk.Label(frame, text="ID Reserva:").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.txt_id_reserva = ttk.Entry(frame, width=25)
        self.txt_id_reserva.grid(row=0, column=1, padx=10, pady=8)

        ttk.Label(frame, text="ID Cliente Existente:").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self.txt_reserva_cliente = ttk.Entry(frame, width=25)
        self.txt_reserva_cliente.grid(row=1, column=1, padx=10, pady=8)

        ttk.Label(frame, text="Seleccionar Servicio:").grid(row=2, column=0, sticky="w", padx=10, pady=8)
        self.combo_servicios = ttk.Combobox(frame, values=list(self.servicios.keys()), width=30, state="readonly")
        self.combo_servicios.grid(row=2, column=1, padx=10, pady=8)
        self.combo_servicios.current(0)

        ttk.Label(frame, text="Cantidad Tiempo (Horas/Días/Sesiones):").grid(row=3, column=0, sticky="w", padx=10, pady=8)
        self.txt_tiempo = ttk.Entry(frame, width=25)
        self.txt_tiempo.grid(row=3, column=1, padx=10, pady=8)

        btn_procesar = ttk.Button(frame, text="Procesar y Validar Reserva", command=self.procesar_reserva_gui)
        btn_procesar.grid(row=4, column=0, columnspan=2, pady=15)

    def procesar_reserva_gui(self):
        id_res = self.txt_id_reserva.get()
        id_cli = self.txt_reserva_cliente.get()
        key_serv = self.combo_servicios.get()
        tiempo_str = self.txt_tiempo.get()

        try:
            if not id_res.strip() or not id_cli.strip() or not tiempo_str.strip():
                raise DatosInvalidError("Todos los campos de la reserva son obligatorios.")

            if id_cli not in self.clientes:
                raise ReservaInvalidaError(f"El cliente con ID '{id_cli}' no está registrado. Regístrelo primero en la pestaña Clientes.")

            try:
                tiempo = int(tiempo_str)
            except ValueError:
                raise DatosInvalidError("El tiempo debe ser un número entero válido.")

            cliente_obj = self.clientes[id_cli]
            servicio_obj = self.servicios[key_serv]

            reserva = Reserva(id_res, cliente_obj, servicio_obj, tiempo)
            exito, mensaje = reserva.procesar_reserva()

            if exito:
                messagebox.showinfo("Reserva Exitosa", mensaje)
            else:
                messagebox.showwarning("Reserva Fallida (Controlada)", mensaje)

        except (DatosInvalidError, ReservaInvalidaError) as e:
            messagebox.showerror("Error Controlado", str(e))
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un fallo: {e}")


# Ejecucion de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AppSoftwareFJ(root)
    root.mainloop()
