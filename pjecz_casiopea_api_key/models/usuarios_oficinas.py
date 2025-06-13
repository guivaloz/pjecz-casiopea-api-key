"""
Usuarios-Oficinas, modelos
"""

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class UsuarioOficina(Base, UniversalMixin):
    """UsuarioOficina"""

    # Nombre de la tabla
    __tablename__ = "usuarios_oficinas"

    # Clave primaria
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Clave foránea
    oficina_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("oficinas.id"))
    oficina: Mapped["Oficina"] = relationship(back_populates="usuarios_oficinas")
    usuario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuarios.id"))
    usuario: Mapped["Usuario"] = relationship(back_populates="usuarios_oficinas")

    # Columnas
    descripcion: Mapped[str] = mapped_column(String(256))

    @property
    def oficina_clave(self):
        """Oficina clave"""
        return self.oficina.clave

    @property
    def usuario_email(self):
        """Email del usuario"""
        return self.usuario.email

    @property
    def usuario_nombre(self):
        """Nombre del usuario"""
        return self.usuario.nombre

    def __repr__(self):
        """Representación"""
        return f"<UsuarioOficina {self.id}>"
