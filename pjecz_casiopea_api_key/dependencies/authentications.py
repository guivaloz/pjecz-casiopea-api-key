"""
Authentications
"""

import re
from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from starlette.status import HTTP_403_FORBIDDEN

from ..config.settings import get_settings
from ..dependencies.cryptography_api_key import decode_api_key
from ..models.usuarios import Usuario
from ..schemas.usuarios import UsuarioInDB
from .database import get_db
from .exceptions import MyAuthenticationError

API_KEY_REGEXP = r"^[a-zA-Z0-9-_=]+$"
X_API_KEY = APIKeyHeader(name="X-Api-Key")

settings = get_settings()


def get_user(
    usuario_email: str,
    database: Session = Depends(get_db),
) -> Optional[UsuarioInDB]:
    """Consultar un usuario por su email"""
    try:
        usuario = database.query(Usuario).filter(Usuario.email == usuario_email).one()
    except (MultipleResultsFound, NoResultFound):
        return None
    return UsuarioInDB(
        id=usuario.id,
        autoridad_clave=usuario.autoridad_clave,
        autoridad_descripcion=usuario.autoridad_descripcion,
        autoridad_descripcion_corta=usuario.autoridad_descripcion_corta,
        distrito_clave=usuario.distrito_clave,
        distrito_nombre=usuario.distrito_nombre,
        distrito_nombre_corto=usuario.distrito_nombre_corto,
        email=usuario.email,
        nombres=usuario.nombres,
        apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno,
        puesto=usuario.puesto,
        username=usuario.nombres,
        permissions=usuario.permissions,
        hashed_password=usuario.contrasena,
        disabled=usuario.estatus != "A",
        api_key=usuario.api_key,
        api_key_expiracion=usuario.api_key_expiracion,
    )


def authenticate_user(
    api_key: str = Depends(X_API_KEY),
    database: Session = Depends(get_db),
) -> UsuarioInDB:
    """Autentificar un usuario por su api_key"""

    # Validar con expresión regular
    if re.match(API_KEY_REGEXP, api_key) is None:
        raise MyAuthenticationError("La API key no pasó la validación")

    # Decodificar
    usuario_email = decode_api_key(api_key)
    if usuario_email == "":
        raise MyAuthenticationError("La API key no se pudo decodificar")

    # Consultar
    usuario = get_user(usuario_email, database)
    if usuario is None:
        raise MyAuthenticationError("La API key no se encontró el usuario")

    # Validar el api_key
    if usuario.api_key != api_key:
        raise MyAuthenticationError("La API key no es igual a la que está en la base de datos")

    # Validar el tiempo de expiración
    if usuario.api_key_expiracion < datetime.now():
        raise MyAuthenticationError("La API key ya expiró")

    # Validad que sea activo
    if usuario.disabled:
        raise MyAuthenticationError("El usuario fue eliminado")

    # Entregar
    return usuario


async def get_current_active_user(
    api_key: str = Depends(X_API_KEY),
    database: Session = Depends(get_db),
) -> UsuarioInDB:
    """Obtener el usuario activo actual"""

    # Try-except
    try:
        usuario = authenticate_user(api_key, database)
    except MyAuthenticationError as error:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(error)) from error

    # Entregar
    return usuario
