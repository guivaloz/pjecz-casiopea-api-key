"""
Cit Citas, routers
"""

from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave, safe_curp, safe_email, safe_string
from ..models.cit_citas import CitCita
from ..models.cit_clientes import CitCliente
from ..models.oficinas import Oficina
from ..models.permisos import Permiso
from ..schemas.cit_citas import CitCitaOut, OneCitCitaOut

cit_citas = APIRouter(prefix="/api/v5/cit_citas")


@cit_citas.get("/{cit_cita_id}", response_model=OneCitCitaOut)
async def detalle_cit_citas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cita_id: int,
):
    """Detalle de una cita a partir de su ID"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    cit_cita = database.query(CitCita).get(cit_cita_id)
    if not cit_cita:
        message = "No existe esa cita"
        return OneCitCitaOut(success=False, message=message, errors=[message])
    if cit_cita.estatus != "A":
        message = "No está habilitada esa cita"
        return OneCitCitaOut(success=False, message=message, errors=[message])
    return OneCitCitaOut(success=True, message=f"Detalle de {cit_cita_id}", data=CitCitaOut.model_validate(cit_cita))


@cit_citas.get("", response_model=CustomPage[CitCitaOut])
async def paginado_cit_citas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    curp: str = None,
    email: str = None,
    estado: str = None,
    inicio: date = None,
    inicio_desde: date = None,
    inicio_hasta: date = None,
    oficina_clave: str = None,
):
    """Paginado de citas"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(CitCita)
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitCita.creado >= desde_dt).filter(CitCita.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0)
        consulta = consulta.filter(CitCita.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(
            year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59
        )
        consulta = consulta.filter(CitCita.creado <= hasta_dt)
    if curp is not None or email is not None:
        consulta = consulta.join(CitCliente)
        if curp is not None:
            curp = safe_curp(curp)
            if curp:
                consulta = consulta.filter(CitCliente.curp == curp)
        if email is not None:
            email = safe_email(email)
            if email:
                consulta = consulta.filter(CitCliente.email == email)
    if estado is not None:
        estado = safe_string(estado)
        if estado in CitCita.ESTADOS:
            consulta = consulta.filter(CitCita.estado == estado)
    if inicio is not None:
        desde_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=0, minute=0, second=0)
        hasta_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitCita.inicio >= desde_dt).filter(CitCita.inicio <= hasta_dt)
    if inicio is None and inicio_desde is not None:
        desde_dt = datetime(year=inicio_desde.year, month=inicio_desde.month, day=inicio_desde.day, hour=0, minute=0, second=0)
        consulta = consulta.filter(CitCita.inicio >= desde_dt)
    if inicio is None and inicio_hasta is not None:
        hasta_dt = datetime(
            year=inicio_hasta.year, month=inicio_hasta.month, day=inicio_hasta.day, hour=23, minute=59, second=59
        )
        consulta = consulta.filter(CitCita.inicio <= hasta_dt)
    if oficina_clave is not None:
        try:
            oficina_clave = safe_clave(oficina_clave)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave de la oficina")
        consulta = consulta.join(Oficina).filter(Oficina.clave == oficina_clave)
    return paginate(consulta.filter_by(estatus="A").order_by(CitCita.id.desc()))
