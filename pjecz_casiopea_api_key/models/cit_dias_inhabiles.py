"""
Cit Dias Inhábiles, modelos
"""

from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class CitDiaInhabil(Base, UniversalMixin):
    """CitDiaInhabil"""

    # Nombre de la tabla
    __tablename__ = "cit_dias_inhabiles"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Columnas
    fecha: Mapped[date] = mapped_column(unique=True)
    descripcion: Mapped[str] = mapped_column(String(256))

    def __repr__(self):
        """Representación"""
        return f"<CitDiaInhabil {self.fecha}>"
