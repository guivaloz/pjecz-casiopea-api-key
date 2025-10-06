"""
Usuarios-Oficinas, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class UsuarioOficinaOut(BaseModel):
    """Esquema para entregar usuarios-oficinas"""

    oficina_clave: str
    oficina_nombre: str
    usuario_email: str
    usuario_nombre: str
    descripcion: str
    model_config = ConfigDict(from_attributes=True)


class OneUsuarioOficinaOut(BaseModel):
    """Esquema para entregar un usuario-oficina"""

    success: bool
    message: str
    data: UsuarioOficinaOut
