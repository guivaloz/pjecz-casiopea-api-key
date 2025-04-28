"""
Cit Horas Disponibles, esquemas de pydantic
"""

from datetime import time

from pydantic import BaseModel


class CitHoraDisponibleOut(BaseModel):
    """Esquema para entregar horas disponibles"""

    horas_minutos: time
