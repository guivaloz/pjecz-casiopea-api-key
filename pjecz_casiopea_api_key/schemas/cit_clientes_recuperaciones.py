"""
Cit Clientes Recuperaciones, esquemas de pydantic
"""

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class CitClienteRecuperacionOut(BaseModel):
    """Esquema para entregar recuperaciones"""

    id: uuid.UUID
    expiracion: datetime
    model_config = ConfigDict(from_attributes=True)


class OneCitClienteRecuperacionOut(BaseModel):
    """Esquema para entregar una recuperación"""

    success: bool
    message: str
    data: CitClienteRecuperacionOut | None = None
