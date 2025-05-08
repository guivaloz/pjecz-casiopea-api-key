"""
Usuarios, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyNotValidParamError
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave, safe_email, safe_string
from ..models.autoridades import Autoridad
from ..models.oficinas import Oficina
from ..models.usuarios import Usuario
from ..models.permisos import Permiso
from ..schemas.usuarios import UsuarioOut, OneUsuarioOut

usuarios = APIRouter(prefix="/api/v5/usuarios")


@usuarios.get("/{email}", response_model=OneUsuarioOut)
async def detalle_usuario(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    email: str,
):
    """Detalle de un usuario a partir de su email"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        email = safe_email(email)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válido el email")
    try:
        usuario = database.query(Usuario).filter_by(email=email).one()
    except (MultipleResultsFound, NoResultFound):
        return OneUsuarioOut(success=False, message="No existe ese usuario")
    if usuario.estatus != "A":
        message = "No está habilitado ese usuario"
        return OneUsuarioOut(success=False, message=message)
    return OneUsuarioOut(success=True, message=f"Detalle de {email}", data=UsuarioOut.model_validate(usuario))


@usuarios.get("", response_model=CustomPage[UsuarioOut])
async def paginado_usuarios(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    apellido_paterno: str = None,
    apellido_materno: str = None,
    autoridad_clave: str = None,
    email: str = None,
    nombres: str = None,
    oficina_clave: str = None,
):
    """Paginado de usuarios"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(Usuario)
    if apellido_paterno is not None:
        apellido_paterno = safe_string(apellido_paterno)
        if apellido_paterno != "":
            consulta = consulta.filter(Usuario.apellido_paterno.contains(apellido_paterno))
    if apellido_materno is not None:
        apellido_materno = safe_string(apellido_materno)
        if apellido_materno != "":
            consulta = consulta.filter(Usuario.apellido_materno.contains(apellido_materno))
    if autoridad_clave is not None:
        try:
            autoridad_clave = safe_clave(autoridad_clave)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave de la autoridad")
        consulta = consulta.join(Autoridad).filter(Autoridad.clave == autoridad_clave)
    if email is not None:
        try:
            email = safe_email(email, search_fragment=True)
        except ValueError as error:
            raise MyNotValidParamError("El email no es válido") from error
        consulta = consulta.filter(Usuario.email.contains(email))
    if nombres is not None:
        nombres = safe_string(nombres)
        if nombres != "":
            consulta = consulta.filter(Usuario.nombres.contains(nombres))
    if oficina_clave is not None:
        try:
            oficina_clave = safe_clave(oficina_clave)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave de la oficina")
        consulta = consulta.join(Oficina).filter(Oficina.clave == oficina_clave)
    return paginate(consulta.filter(Usuario.estatus == "A").order_by(Usuario.email))
