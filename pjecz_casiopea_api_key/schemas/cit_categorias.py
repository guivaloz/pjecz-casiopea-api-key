"""
Cit Categorías, esquemas de pydantic
"""

import uuid

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitCategoriaOut(BaseModel):
    """Esquema para entregar categorías"""

    id: uuid.UUID
    nombre: str
    model_config = ConfigDict(from_attributes=True)


class OneCitCategoriaOut(OneBaseOut):
    """Esquema para entregar una categoría"""

    data: CitCategoriaOut | None = None
