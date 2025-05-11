"""
Usuarios, esquemas de pydantic
"""

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class UsuarioOut(BaseModel):
    """Esquema para entregar usuarios"""

    distrito_clave: str
    distrito_nombre: str
    autoridad_clave: str
    autoridad_descripcion: str
    email: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    puesto: str
    model_config = ConfigDict(from_attributes=True)


class OneUsuarioOut(OneBaseOut):
    """Esquema para entregar un usuario"""

    data: UsuarioOut | None = None


class UsuarioInDB(UsuarioOut):
    """Usuario en base de datos"""

    id: uuid.UUID
    username: str
    permissions: dict
    hashed_password: str
    disabled: bool
    api_key: str
    api_key_expiracion: datetime
