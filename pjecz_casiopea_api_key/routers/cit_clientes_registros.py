"""
Cit Clientes Registros, routers
"""

from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_email, safe_string, safe_telefono
from ..models.cit_clientes_registros import CitClienteRegistro
from ..models.permisos import Permiso
from ..schemas.cit_clientes_registros import CitClienteRegistroOut, OneCitClienteRegistroOut

cit_clientes_registros = APIRouter(prefix="/api/v5/cit_clientes_registros")


@cit_clientes_registros.get("/{cit_cliente_registro_id}", response_model=OneCitClienteRegistroOut)
async def detalle_cit_clientes_registros(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cliente_registro_id: int,
):
    """Detalle de un registro a partir de su ID"""
    if current_user.permissions.get("CIT CLIENTES REGISTROS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    cit_cliente_registro = database.query(CitClienteRegistro).get(cit_cliente_registro_id)
    if not cit_cliente_registro:
        message = "No existe ese registro"
        return OneCitClienteRegistroOut(success=False, message=message, errors=[message])
    if cit_cliente_registro.estatus != "A":
        message = "No está habilitada ese registro"
        return OneCitClienteRegistroOut(success=False, message=message, errors=[message])
    return OneCitClienteRegistroOut(
        success=True,
        message=f"Detalle de {cit_cliente_registro_id}",
        data=CitClienteRegistroOut.model_validate(cit_cliente_registro),
    )


@cit_clientes_registros.get("", response_model=CustomPage[CitClienteRegistroOut])
async def paginado_cit_clientes_registros(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    apellido_primero: str = None,
    apellido_segundo: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    curp: str = None,
    email: str = None,
    nombres: str = None,
    telefono: str = None,
):
    """Paginado de registros"""
    if current_user.permissions.get("CIT CLIENTES REGISTROS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(CitClienteRegistro)
    if apellido_primero is not None:
        apellido_primero = safe_string(apellido_primero)
        if apellido_primero:
            consulta = consulta.filter(CitClienteRegistro.apellido_primero.contains(apellido_primero))
    if apellido_segundo is not None:
        apellido_segundo = safe_string(apellido_segundo)
        if apellido_segundo:
            consulta = consulta.filter(CitClienteRegistro.apellido_segundo.startswith(apellido_segundo))
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitClienteRegistro.creado >= desde_dt).filter(CitClienteRegistro.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0)
        consulta = consulta.filter(CitClienteRegistro.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(
            year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59
        )
        consulta = consulta.filter(CitClienteRegistro.creado <= hasta_dt)
    if curp is not None:
        curp = safe_string(curp)
        if curp:
            consulta = consulta.filter(CitClienteRegistro.curp.contains(curp))
    if email is not None:
        email = safe_email(email, search_fragment=True)
        if email:
            consulta = consulta.filter(CitClienteRegistro.email.contains(email))
    if nombres is not None:
        nombres = safe_string(nombres)
        if nombres:
            consulta = consulta.filter(CitClienteRegistro.nombres.contains(nombres))
    if telefono is not None:
        telefono = safe_telefono(telefono)
        if telefono:
            consulta = consulta.filter(CitClienteRegistro.telefono == telefono)
    return paginate(consulta.filter_by(estatus="A").order_by(CitClienteRegistro.id.desc()))
