"""
Cit Clientes, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_email, safe_string, safe_telefono
from ..models.cit_clientes import CitCliente
from ..models.permisos import Permiso
from ..schemas.cit_clientes import CitClienteOut, OneCitClienteOut

cit_clientes = APIRouter(prefix="/api/v5/cit_clientes")


@cit_clientes.get("/{email}", response_model=OneCitClienteOut)
async def detalle_cit_clientes(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    email: str,
):
    """Detalle de un cliente a partir de su email"""
    if current_user.permissions.get("CIT CLIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        email = safe_email(email)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válido el email")
    try:
        cit_cliente = database.query(CitCliente).filter_by(email=email).one()
    except (MultipleResultsFound, NoResultFound):
        return OneCitClienteOut(success=False, message="No existe ese cliente")
    if cit_cliente.estatus != "A":
        return OneCitClienteOut(success=False, message="No está habilitado ese cliente")
    return OneCitClienteOut(success=True, message=f"Detalle de {email}", data=CitClienteOut.model_validate(cit_cliente))


@cit_clientes.get("", response_model=CustomPage[CitClienteOut])
async def paginado_cit_clientes(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    apellido_primero: str = None,
    apellido_segundo: str = None,
    curp: str = None,
    email: str = None,
    nombres: str = None,
    telefono: str = None,
):
    """Paginado de clientes"""
    if current_user.permissions.get("CIT CLIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(CitCliente)
    if apellido_primero is not None:
        apellido_primero = safe_string(apellido_primero)
        if apellido_primero:
            consulta = consulta.filter(CitCliente.apellido_primero.contains(apellido_primero))
    if apellido_segundo is not None:
        apellido_segundo = safe_string(apellido_segundo)
        if apellido_segundo:
            consulta = consulta.filter(CitCliente.apellido_segundo.startswith(apellido_segundo))
    if curp is not None:
        curp = safe_string(curp)
        if curp:
            consulta = consulta.filter(CitCliente.curp.contains(curp))
    if email is not None:
        email = safe_email(email, search_fragment=True)
        if email:
            consulta = consulta.filter(CitCliente.email.contains(email))
    if nombres is not None:
        nombres = safe_string(nombres)
        if nombres:
            consulta = consulta.filter(CitCliente.nombres.contains(nombres))
    if telefono is not None:
        telefono = safe_telefono(telefono)
        if telefono:
            consulta = consulta.filter(CitCliente.telefono == telefono)
    return paginate(consulta.filter_by(estatus="A").order_by(CitCliente.email))
