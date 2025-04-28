"""
Entradas-Salidas, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class EntradaSalidaOut(BaseModel):
    """Esquema para entregar entradas-salidas"""

    id: int
    usuario_id: int
    usuario_nombre: str
    tipo: str
    direccion_ip: str
    creado: datetime
    model_config = ConfigDict(from_attributes=True)


class OneEntradaSalidaOut(OneBaseOut):
    """Esquema para entregar una entrada-salida"""

    data: EntradaSalidaOut | None = None
