"""
Roles, esquemas de pydantic
"""

import uuid

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class RolOut(BaseModel):
    """Esquema para entregar roles"""

    id: uuid.UUID
    nombre: str
    model_config = ConfigDict(from_attributes=True)


class OneRolOut(OneBaseOut):
    """Esquema para entregar un rol"""

    data: RolOut | None = None
