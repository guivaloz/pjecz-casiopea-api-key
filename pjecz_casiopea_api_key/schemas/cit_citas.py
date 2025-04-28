"""
Cit Citas, esquemas de pydantic
"""

from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitCitaCancelIn(BaseModel):
    """Esquema para cancelar una cita"""

    id: int
    cit_cliente_id: int


class CitCitaIn(BaseModel):
    """Esquema para crear una cita"""

    cit_cliente_id: int
    cit_servicio_id: int
    fecha: date
    hora_minuto: time
    oficina_id: int
    notas: str


class CitCitaOut(BaseModel):
    """Esquema para entregar citas"""

    id: int
    cit_cliente_id: int
    cit_cliente_nombre: str
    cit_cliente_curp: str
    cit_cliente_email: str
    cit_servicio_id: int
    cit_servicio_clave: str
    cit_servicio_descripcion: str
    oficina_id: int
    oficina_clave: str
    oficina_descripcion: str
    oficina_descripcion_corta: str
    inicio: datetime
    termino: datetime
    notas: str
    estado: str
    asistencia: bool
    codigo_asistencia: str
    creado: datetime
    puede_cancelarse: bool
    model_config = ConfigDict(from_attributes=True)


class OneCitCitaOut(OneBaseOut):
    """Esquema para entregar un cita"""

    data: CitCitaOut | None = None


class CitCitasCreadosPorDiaOut(BaseModel):
    """Esquema para entregar cantidades de citas creadas por dia"""

    creado: date
    cantidad: int


class CitCitasCreadosPorDiaDistritoOut(BaseModel):
    """Esquema para entregar cantidades de citas creadas por dia"""

    creado: date
    distrito: str
    cantidad: int


class CitCitasAgendadasPorServicioOficinaOut(BaseModel):
    """Esquema para entregar cantidades de citas agendadas por servicio y oficina"""

    oficina: str
    servicio: str
    cantidad: int


class CitCitasDisponiblesCantidadOut(OneBaseOut):
    """Esquema para entregar la cantidad de citas disponibles"""

    cantidad: int
