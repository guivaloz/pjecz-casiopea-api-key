"""
Usuarios-Roles, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class UsuarioRolOut(BaseModel):
    """Esquema para entregar usuarios-roles"""

    rol_nombre: str
    usuario_email: str
    usuario_nombre: str
    descripcion: str
    model_config = ConfigDict(from_attributes=True)


class OneUsuarioRolOut(OneBaseOut):
    """Esquema para entregar un usuario-rol"""

    data: UsuarioRolOut | None = None
