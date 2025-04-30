"""
Permisos, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class PermisoOut(BaseModel):
    """Esquema para entregar permisos"""

    id: str
    rol_id: str
    rol_nombre: str
    modulo_id: str
    modulo_nombre: str
    nombre: str
    nivel: int
    model_config = ConfigDict(from_attributes=True)


class OnePermisoOut(OneBaseOut):
    """Esquema para entregar un permiso"""

    data: PermisoOut | None = None
