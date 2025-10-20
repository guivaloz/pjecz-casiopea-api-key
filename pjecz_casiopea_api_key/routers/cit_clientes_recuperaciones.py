"""
Cit Clientes Recuperaciones, routers
"""

from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_curp, safe_email, safe_uuid
from ..models.cit_clientes import CitCliente
from ..models.cit_clientes_recuperaciones import CitClienteRecuperacion
from ..models.permisos import Permiso
from ..schemas.cit_clientes_recuperaciones import CitClienteRecuperacionOut, OneCitClienteRecuperacionOut

cit_clientes_recuperaciones = APIRouter(prefix="/api/v5/cit_clientes_recuperaciones")


@cit_clientes_recuperaciones.get("/{cit_cliente_recuperacion_id}", response_model=OneCitClienteRecuperacionOut)
async def detalle(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cliente_recuperacion_id: str,
):
    """Detalle de una recuperación a partir de su ID"""
    if current_user.permissions.get("CIT CLIENTES RECUPERACIONES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente_recuperacion_id = safe_uuid(cit_cliente_recuperacion_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la UUID")
    cit_cliente_recuperacion = database.query(CitClienteRecuperacion).get(cit_cliente_recuperacion_id)
    if not cit_cliente_recuperacion:
        return OneCitClienteRecuperacionOut(success=False, message="No existe esa recuperación")
    if cit_cliente_recuperacion.estatus != "A":
        return OneCitClienteRecuperacionOut(success=False, message="No está habilitada esa recuperación")
    return OneCitClienteRecuperacionOut(
        success=True,
        message=f"Detalle de {cit_cliente_recuperacion_id}",
        data=CitClienteRecuperacionOut.model_validate(cit_cliente_recuperacion),
    )


@cit_clientes_recuperaciones.get("", response_model=CustomPage[CitClienteRecuperacionOut])
async def paginado(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    curp: str = None,
    email: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
):
    """Paginado de recuperaciones"""
    if current_user.permissions.get("CIT CLIENTES RECUPERACIONES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(CitClienteRecuperacion)

    # Filtrar por CURP y e-mail
    if curp is not None or email is not None:
        consulta = consulta.join(CitCliente)
        if curp is not None:
            try:
                curp = safe_curp(curp, is_optional=False, search_fragment=False)
                consulta = consulta.filter(CitCliente.curp == curp)
            except ValueError:
                return CustomPage(success=False, message="No es válido el CURP")
        if email is not None:
            try:
                email = safe_email(email, search_fragment=False)
                consulta = consulta.filter(CitCliente.email == email)
            except ValueError:
                return CustomPage(success=False, message="No es válido el e-mail")

    # Filtrar por fechas de creación
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitClienteRecuperacion.creado >= desde_dt).filter(CitClienteRecuperacion.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0)
        consulta = consulta.filter(CitClienteRecuperacion.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(
            year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59
        )
        consulta = consulta.filter(CitClienteRecuperacion.creado <= hasta_dt)

    # Entregar
    return paginate(consulta.filter(CitClienteRecuperacion.estatus == "A").order_by(CitClienteRecuperacion.id.desc()))
