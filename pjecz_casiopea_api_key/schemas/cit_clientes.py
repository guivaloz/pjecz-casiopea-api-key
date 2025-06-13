"""
Cit Clientes, esquemas de pydantic
"""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitClienteOut(BaseModel):
    """Esquema para entregar clientes"""

    nombres: str
    apellido_primero: str
    apellido_segundo: str
    nombre: str
    curp: str
    telefono: str
    email: str
    limite_citas_pendientes: int
    autoriza_mensajes: bool
    enviar_boletin: bool
    es_adulto_mayor: bool
    es_mujer: bool
    es_identidad: bool
    es_discapacidad: bool
    creado: datetime
    model_config = ConfigDict(from_attributes=True)


class OneCitClienteOut(OneBaseOut):
    """Esquema para entregar un cliente"""

    data: CitClienteOut | None = None
