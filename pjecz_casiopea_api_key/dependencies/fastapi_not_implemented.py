"""
FastAPI not implemented schema
"""

from pydantic import BaseModel


class NotImplement(BaseModel):
    """Esquema para rutas no implementadas"""

    success: bool = False
    message: str = "Esta ruta no está implementada"
    data: list | None
