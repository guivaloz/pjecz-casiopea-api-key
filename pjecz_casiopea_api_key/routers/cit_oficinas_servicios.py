"""
Cit Oficinas Servicios, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave, safe_uuid
from ..models.cit_oficinas_servicios import CitOficinaServicio
from ..models.cit_servicios import CitServicio
from ..models.oficinas import Oficina
from ..models.permisos import Permiso
from ..schemas.cit_oficinas_servicios import CitOficinaServicioOut, OneCitOficinaServicioOut

cit_oficinas_servicios = APIRouter(prefix="/api/v5/cit_oficinas_servicios")


@cit_oficinas_servicios.get("/{cit_oficina_servicio_id}", response_model=OneCitOficinaServicioOut)
async def detalle(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_oficina_servicio_id: str,
):
    """Detalle de un servicio de una oficina a partir de su ID"""
    if current_user.permissions.get("CIT OFICINAS SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_oficina_servicio_id = safe_uuid(cit_oficina_servicio_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la UUID")
    cit_oficina_servicio = database.query(CitOficinaServicio).get(cit_oficina_servicio_id)
    if not cit_oficina_servicio:
        return OneCitOficinaServicioOut(success=False, message="No existe ese servicio de una oficina")
    if cit_oficina_servicio.estatus != "A":
        return OneCitOficinaServicioOut(success=False, message="No está habilitada ese servicio de una oficina")
    return OneCitOficinaServicioOut(
        success=True,
        message=f"Detalle de {cit_oficina_servicio_id}",
        data=CitOficinaServicioOut.model_validate(cit_oficina_servicio),
    )


@cit_oficinas_servicios.get("", response_model=CustomPage[CitOficinaServicioOut])
async def paginado(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_servicio_clave: str = None,
    oficina_clave: str = None,
):
    """Paginado de servicios de oficinas"""
    if current_user.permissions.get("CIT OFICINAS SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(CitOficinaServicio)
    if cit_servicio_clave is not None:
        try:
            cit_servicio_clave = safe_clave(cit_servicio_clave)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave de la oficina")
        consulta = consulta.join(CitServicio).filter(CitServicio.clave == cit_servicio_clave)
    if oficina_clave is not None:
        try:
            oficina_clave = safe_clave(oficina_clave)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave de la oficina")
        consulta = consulta.join(Oficina).filter(Oficina.clave == oficina_clave)
    return paginate(consulta.filter_by(estatus="A").order_by(CitOficinaServicio.descripcion))
