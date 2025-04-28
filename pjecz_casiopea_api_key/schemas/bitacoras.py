"""
Bitácoras, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class BitacoraOut(BaseModel):
    """Esquema para entregar bitácoras"""

    id: int
    modulo_id: int
    modulo_nombre: str
    usuario_id: int
    usuario_nombre: str
    descripcion: str
    url: str
    creado: datetime
    model_config = ConfigDict(from_attributes=True)


class OneBitacoraOut(OneBaseOut):
    """Esquema para entregar una bitácora"""

    data: BitacoraOut | None = None
