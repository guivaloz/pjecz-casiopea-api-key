"""
Oficinas, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class OficinaOut(BaseModel):
    """Esquema para entregar oficinas"""

    clave: str
    descripcion: str
    descripcion_corta: str
    domicilio_clave: str
    domicilio_completo: str
    domicilio_edificio: str
    es_jurisdiccional: bool
    model_config = ConfigDict(from_attributes=True)


class OneOficinaOut(OneBaseOut):
    """Esquema para entregar una oficina"""

    data: OficinaOut | None = None
