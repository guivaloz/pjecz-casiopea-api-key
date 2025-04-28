"""
Cit Dias Disponibles, esquemas de pydantic
"""

from datetime import date

from pydantic import BaseModel

from ..dependencies.schemas_base import OneBaseOut


class CitDiaDisponibleOut(BaseModel):
    """Esquema para entregar dias disponibles"""

    fecha: date


class OneCitDiaDisponibleOut(OneBaseOut):
    """Esquema para entregar un dia disponible"""

    data: CitDiaDisponibleOut | None = None
