"""
Cit Servicios, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.cit_categorias import CitCategoria
from ..models.cit_servicios import CitServicio
from ..models.permisos import Permiso
from ..schemas.cit_servicios import CitServicioOut, OneCitServicioOut

cit_servicios = APIRouter(prefix="/api/v5/cit_servicios")


@cit_servicios.get("/{clave}", response_model=OneCitServicioOut)
async def detalle(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de un servicio a partir de su clave"""
    if current_user.permissions.get("CIT SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    clave = safe_clave(clave)
    if clave == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
    try:
        cit_servicio = database.query(CitServicio).filter_by(clave=clave).one()
    except (MultipleResultsFound, NoResultFound):
        return OneCitServicioOut(success=False, message="No existe ese servicio")
    if cit_servicio.es_activo is False:
        return OneCitServicioOut(success=False, message="No está activo ese servicio")
    if cit_servicio.estatus != "A":
        return OneCitServicioOut(success=False, message="Este servicio está eliminado")
    return OneCitServicioOut(success=True, message=f"Detalle de {clave}", data=CitServicioOut.model_validate(cit_servicio))


@cit_servicios.get("", response_model=CustomPage[CitServicioOut])
async def paginado(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_categoria_clave: str = None,
):
    """Paginado de servicios"""
    if current_user.permissions.get("CIT SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(CitServicio)
    if cit_categoria_clave is not None:
        cit_categoria_clave = safe_clave(cit_categoria_clave)
        if cit_categoria_clave == "":
            return CustomPage(success=False, message="No es válida la clave de la categoria")
        consulta = consulta.join(CitCategoria).filter(CitCategoria.clave == cit_categoria_clave)
    return paginate(
        consulta.filter(CitServicio.es_activo == True).filter(CitServicio.estatus == "A").order_by(CitServicio.clave)
    )
