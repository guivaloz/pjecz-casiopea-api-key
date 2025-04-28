"""
Usuarios-Oficinas, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class UsuarioOficinaOut(BaseModel):
    """Esquema para entregar usuarios-oficinas"""

    id: int
    oficina_id: int
    oficina_nombre: str
    usuario_id: int
    usuario_nombre: str
    descripcion: str
    model_config = ConfigDict(from_attributes=True)


class OneUsuarioOficinaOut(OneBaseOut):
    """Esquema para entregar un usuario-oficina"""

    data: UsuarioOficinaOut
