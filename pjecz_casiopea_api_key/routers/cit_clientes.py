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
from ..dependencies.safe_string import safe_curp, safe_email, safe_string, safe_telefono, safe_uuid
from ..models.cit_clientes import CitCliente
from ..models.permisos import Permiso
from ..schemas.cit_clientes import CitClienteOut, OneCitClienteOut

cit_clientes = APIRouter(prefix="/api/v5/cit_clientes")


@cit_clientes.get("/perfil", response_model=OneCitClienteOut)
async def perfil(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cliente_id: str = None,
    curp: str = None,
):
    """Perfil de un cliente a partir de su UUID"""
    if current_user.permissions.get("CIT CLIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Por defecto no hay cliente
    cit_cliente = None

    # Validar y consultar por cit_cliente_id
    if cit_cliente_id is not None and curp is None:
        try:
            cit_cliente_id = safe_uuid(cit_cliente_id)
        except ValueError:
            return OneCitClienteOut(success=False, message="No es válido el cit_cliente_id")
        cit_cliente = database.query(CitCliente).get(cit_cliente_id)
        if cit_cliente is None:
            return OneCitClienteOut(success=False, message="No existe ese cliente")

    # Validar y consultar por CURP
    if curp is not None and cit_cliente_id is None:
        try:
            curp = safe_curp(curp, is_optional=False, search_fragment=False)
        except ValueError:
            return OneCitClienteOut(success=False, message="No es válido el CURP")
        try:
            cit_cliente = database.query(CitCliente).filter_by(curp=curp).one()
        except (MultipleResultsFound, NoResultFound):
            return OneCitClienteOut(success=False, message="No existe un cliente con ese CURP")

    # Si no se proporcionó ninguno de los dos parámetros
    if cit_cliente is None:
        return OneCitClienteOut(success=False, message="No se proporcionó cit_cliente_id ni CURP, debe dar uno de los dos")

    # Validar que cliente NO esté deshabilitado
    if cit_cliente.estatus != "A":
        return OneCitClienteOut(success=False, message="No está habilitado ese cliente")

    # Entregar el perfil
    return OneCitClienteOut(success=True, message=f"Perfil de {cit_cliente_id}", data=CitClienteOut.model_validate(cit_cliente))


@cit_clientes.get("/{curp}", response_model=OneCitClienteOut)
async def detalle(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    curp: str,
):
    """Detalle de un cliente a partir de su curp"""
    if current_user.permissions.get("CIT CLIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        curp = safe_curp(curp, is_optional=False, search_fragment=False)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válido el CURP")
    try:
        cit_cliente = database.query(CitCliente).filter_by(curp=curp).one()
    except (MultipleResultsFound, NoResultFound):
        return OneCitClienteOut(success=False, message="No existe ese CURP")
    if cit_cliente.estatus != "A":
        return OneCitClienteOut(success=False, message="No está habilitado ese cliente")
    return OneCitClienteOut(success=True, message=f"Detalle de {curp}", data=CitClienteOut.model_validate(cit_cliente))


@cit_clientes.get("", response_model=CustomPage[CitClienteOut])
async def paginado(
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
        curp = safe_curp(curp, is_optional=True, search_fragment=True)
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
