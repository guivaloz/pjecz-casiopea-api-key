"""
Usuarios, modelos
"""

from datetime import datetime
from typing import List, Optional
import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin
from .permisos import Permiso


class Usuario(Base, UniversalMixin):
    """Usuario"""

    # Nombre de la tabla
    __tablename__ = "usuarios"

    # Clave primaria
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Claves foráneas
    autoridad_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("autoridades.id"))
    autoridad: Mapped["Autoridad"] = relationship(back_populates="usuarios")

    # Columnas
    email: Mapped[str] = mapped_column(String(256), unique=True)
    nombres: Mapped[str] = mapped_column(String(256))
    apellido_paterno: Mapped[str] = mapped_column(String(256))
    apellido_materno: Mapped[str] = mapped_column(String(256))
    puesto: Mapped[str] = mapped_column(String(256))
    api_key: Mapped[Optional[str]] = mapped_column(String(128))
    api_key_expiracion: Mapped[Optional[datetime]]
    contrasena: Mapped[Optional[str]] = mapped_column(String(256))

    # Hijos
    usuarios_roles: Mapped[List["UsuarioRol"]] = relationship("UsuarioRol", back_populates="usuario")
    usuarios_oficinas: Mapped[List["UsuarioOficina"]] = relationship("UsuarioOficina", back_populates="usuario")

    # Propiedades
    permisos_consultados = {}

    @property
    def nombre(self):
        """Junta nombres, apellido_paterno y apellido materno"""
        return self.nombres + " " + self.apellido_paterno + " " + self.apellido_materno

    @property
    def distrito_clave(self):
        """Distrito clave"""
        return self.autoridad.distrito.clave

    @property
    def distrito_nombre(self):
        """Distrito nombre"""
        return self.autoridad.distrito.nombre

    @property
    def distrito_nombre_corto(self):
        """Distrito nombre corto"""
        return self.autoridad.distrito.nombre_corto

    @property
    def autoridad_clave(self):
        """Autoridad clave"""
        return self.autoridad.clave

    @property
    def autoridad_descripcion(self):
        """Autoridad descripción"""
        return self.autoridad.descripcion

    @property
    def autoridad_descripcion_corta(self):
        """Autoridad descripción corta"""
        return self.autoridad.descripcion_corta

    @property
    def permissions(self):
        """Entrega un diccionario con todos los permisos"""
        if len(self.permisos_consultados) > 0:
            return self.permisos_consultados
        self.permisos_consultados = {}
        for usuario_rol in self.usuarios_roles:
            if usuario_rol.estatus == "A":
                for permiso in usuario_rol.rol.permisos:
                    if permiso.estatus == "A":
                        etiqueta = permiso.modulo.nombre
                        if etiqueta not in self.permisos_consultados or permiso.nivel > self.permisos_consultados[etiqueta]:
                            self.permisos_consultados[etiqueta] = permiso.nivel
        return self.permisos_consultados

    def can(self, modulo_nombre: str, permission: int):
        """¿Tiene permiso?"""
        if modulo_nombre in self.permisos:
            return self.permisos[modulo_nombre] >= permission
        return False

    def can_view(self, modulo_nombre: str):
        """¿Tiene permiso para ver?"""
        return self.can(modulo_nombre, Permiso.VER)

    def can_edit(self, modulo_nombre: str):
        """¿Tiene permiso para editar?"""
        return self.can(modulo_nombre, Permiso.MODIFICAR)

    def can_insert(self, modulo_nombre: str):
        """¿Tiene permiso para agregar?"""
        return self.can(modulo_nombre, Permiso.CREAR)

    def can_admin(self, modulo_nombre: str):
        """¿Tiene permiso para administrar?"""
        return self.can(modulo_nombre, Permiso.ADMINISTRAR)

    def __repr__(self):
        """Representación"""
        return f"<Usuario {self.email}>"
