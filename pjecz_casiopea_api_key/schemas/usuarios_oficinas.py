"""
Usuarios-Oficinas, esquemas de pydantic
"""

import uuid

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class UsuarioOficinaOut(BaseModel):
    """Esquema para entregar usuarios-oficinas"""

    id: uuid.UUID
    oficina_clave: str
    oficina_nombre: str
    usuario_email: str
    usuario_nombre: str
    descripcion: str
    model_config = ConfigDict(from_attributes=True)


class OneUsuarioOficinaOut(OneBaseOut):
    """Esquema para entregar un usuario-oficina"""

    data: UsuarioOficinaOut
