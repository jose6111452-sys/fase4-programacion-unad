from abc import ABC, abstractmethod
from datetime import datetime

# =============================
# ARCHIVO DE LOGS
# =============================

def registrar_log(mensaje):
    with open("logs.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{datetime.now()} - {mensaje}\n")


# =============================
# EXCEPCIONES PERSONALIZADAS
# =============================

class ClienteError(Exception):
    pass


class ServicioError(Exception):
    pass


class ReservaError(Exception):
    pass


# =============================
# CLASE ABSTRACTA PERSONA
# =============================

class Persona(ABC):

    @abstractmethod
    def mostrar_informacion(self):
        pass


# =============================
# CLASE CLIENTE
# =============================

class Cliente(Persona):

    def __init__(self, nombre, documento, correo):

        if not nombre.strip():
            raise ClienteError("El nombre no puede estar vacío")

        if len(documento) < 5:
            raise ClienteError("Documento inválido")

        if "@" not in correo:
            raise ClienteError("Correo inválido")

        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo

    def get_nombre(self):
        return self.__nombre

    def mostrar_informacion(self):
        return f"Cliente: {self.__nombre} - Documento: {self.__documento}"


# =============================
# CLASE ABSTRACTA SERVICIO
# =============================

class Servicio(ABC):

    def __init__(self, nombre, tarifa_base):

        if tarifa_base <= 0:
            raise ServicioError("La tarifa debe ser positiva")

        self.nombre = nombre
        self.tarifa_base = tarifa_base

    @abstractmethod
    def calcular_costo(self, horas):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# =============================
# SERVICIO RESERVA DE SALAS
# =============================

class ReservaSala(Servicio):

    def calcular_costo(self, horas, impuesto=0):
        total = (self.tarifa_base * horas)
        total += total * impuesto
        return total

    def descripcion(self):
        return "Servicio de reserva de salas empresariales"


# =============================
# SERVICIO ALQUILER EQUIPOS
# =============================

class AlquilerEquipo(Servicio):

    def calcular_costo(self, horas, descuento=0):
        total = self.tarifa_base * horas
        total -= total * descuento
        return total

    def descripcion(self):
        return "Servicio de alquiler de equipos tecnológicos"


# =============================
# SERVICIO ASESORIA
# =============================

class Asesoria(Servicio):

    def calcular_costo(self, horas, extra=0):
        return (self.tarifa_base * horas) + extra

    def descripcion(self):
        return "Servicio de asesoría especializada"


# =============================
# CLASE RESERVA
# =============================

class Reserva:

    def __init__(self, cliente, servicio, horas):

        if horas <= 0:
            raise ReservaError("Las horas deben ser mayores que cero")

        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "Pendiente"

    def confirmar(self):
        self.estado = "Confirmada"
        registrar_log(f"Reserva confirmada para {self.cliente.get_nombre()}")

    def cancelar(self):
        self.estado = "Cancelada"
        registrar_log(f"Reserva cancelada para {self.cliente.get_nombre()}")

    def procesar(self):

        try:
            costo = self.servicio.calcular_costo(self.horas)
            self.confirmar()

        except Exception as error:
            registrar_log(f"Error procesando reserva: {error}")
            raise ReservaError("No fue posible procesar la reserva") from error

        else:
            print("Reserva procesada correctamente")
            print(f"Costo total: ${costo}")

        finally:
            print("Proceso de reserva finalizado")


# =============================
# LISTAS PRINCIPALES
# =============================

clientes = []
servicios = []
reservas = []


# =============================
# SIMULACIÓN DE OPERACIONES
# =============================

print("===== SISTEMA SOFTWARE FJ =====")


# OPERACIÓN 1
try:
    cliente1 = Cliente("Juan Pérez", "12345", "juan@gmail.com")
    clientes.append(cliente1)
    print(cliente1.mostrar_informacion())

except ClienteError as error:
    print(error)
    registrar_log(error)


# OPERACIÓN 2
try:
    cliente2 = Cliente("", "123", "correo")
    clientes.append(cliente2)

except ClienteError as error:
    print(f"Error cliente: {error}")
    registrar_log(error)


# OPERACIÓN 3
try:
    sala = ReservaSala("Sala VIP", 50000)
    servicios.append(sala)
    print(sala.descripcion())

except ServicioError as error:
    print(error)
    registrar_log(error)


# OPERACIÓN 4
try:
    equipo = AlquilerEquipo("Computadores", 30000)
    servicios.append(equipo)
    print(equipo.descripcion())

except ServicioError as error:
    print(error)
    registrar_log(error)


# OPERACIÓN 5
try:
    asesoria = Asesoria("Asesoría TI", 80000)
    servicios.append(asesoria)
    print(asesoria.descripcion())

except ServicioError as error:
    print(error)
    registrar_log(error)


# OPERACIÓN 6
try:
    servicio_invalido = ReservaSala("Sala básica", -100)

except ServicioError as error:
    print(f"Error servicio: {error}")
    registrar_log(error)


# OPERACIÓN 7
try:
    reserva1 = Reserva(cliente1, sala, 4)
    reservas.append(reserva1)
    reserva1.procesar()

except ReservaError as error:
    print(error)
    registrar_log(error)


# OPERACIÓN 8
try:
    reserva2 = Reserva(cliente1, equipo, -2)
    reservas.append(reserva2)
    reserva2.procesar()

except ReservaError as error:
    print(f"Error reserva: {error}")
    registrar_log(error)


# OPERACIÓN 9
try:
    reserva3 = Reserva(cliente1, asesoria, 2)
    reservas.append(reserva3)
    reserva3.cancelar()
    print("Reserva cancelada correctamente")

except ReservaError as error:
    print(error)
    registrar_log(error)


# OPERACIÓN 10
try:
    costo = sala.calcular_costo(5, impuesto=0.19)
    print(f"Costo con impuesto: ${costo}")

except Exception as error:
    print(error)
    registrar_log(error)


print("===== FIN DEL SISTEMA =====")
