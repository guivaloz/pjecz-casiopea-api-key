"""
Cit Dias Inhábiles, esquemas de pydantic
"""

from datetime import date

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitDiaInhabilIn(BaseModel):
    """Esquema para recibir un día inhábil"""

    fecha: date
    descripcion: str


class CitDiaInhabilOut(CitDiaInhabilIn):
    """Esquema para entregar dias inhábiles"""

    id: int
    model_config = ConfigDict(from_attributes=True)


class OneCitDiaInhabilOut(OneBaseOut):
    """Esquema para entregar un día inhábil"""

    data: CitDiaInhabilOut | None = None
