"""
Cit Clientes, esquemas de pydantic
"""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitClienteOut(BaseModel):
    """Esquema para entregar clientes"""

    id: int
    nombres: str
    apellido_primero: str
    apellido_segundo: str
    nombre: str
    curp: str
    telefono: str
    email: str
    contrasena_md5: str
    contrasena_sha256: str
    renovacion: date
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


class CitClientesCreadosPorDiaOut(BaseModel):
    """Esquema para entregar cantidades de clientes creados por dia"""

    creado: date
    cantidad: int
