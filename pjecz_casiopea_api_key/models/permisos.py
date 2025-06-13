"""
Permisos, modelos
"""

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class Permiso(Base, UniversalMixin):
    """Permiso"""

    VER = 1
    MODIFICAR = 2
    CREAR = 3
    BORRAR = 3
    ADMINISTRAR = 4
    NIVELES = {
        1: "VER",
        2: "VER y MODIFICAR",
        3: "VER, MODIFICAR y CREAR",
        4: "ADMINISTRAR",
    }

    # Nombre de la tabla
    __tablename__ = "permisos"

    # Clave primaria
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Claves foráneas
    rol_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id"))
    rol: Mapped["Rol"] = relationship(back_populates="permisos")
    modulo_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("modulos.id"))
    modulo: Mapped["Modulo"] = relationship(back_populates="permisos")

    # Columnas
    nombre: Mapped[str] = mapped_column(String(256), unique=True)
    nivel: Mapped[int]

    @property
    def rol_nombre(self):
        """Nombre del rol"""
        return self.rol.nombre

    @property
    def modulo_nombre(self):
        """Nombre del modulo"""
        return self.modulo.nombre

    def __repr__(self):
        """Representación"""
        return f"<Permiso {self.id}>"
