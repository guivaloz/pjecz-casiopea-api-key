"""
Oficinas, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.distritos import Distrito
from ..models.domicilios import Domicilio
from ..models.oficinas import Oficina
from ..models.permisos import Permiso
from ..schemas.oficinas import OficinaOut, OneOficinaOut

oficinas = APIRouter(prefix="/api/v5/oficinas")


@oficinas.get("/{clave}", response_model=OneOficinaOut)
async def detalle(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de una oficina a partir de su clave"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    clave = safe_clave(clave)
    if clave == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
    try:
        oficina = database.query(Oficina).filter_by(clave=clave).one()
    except (MultipleResultsFound, NoResultFound):
        return OneOficinaOut(success=False, message="No existe esa oficina")
    if oficina.es_activo is False:
        return OneOficinaOut(success=False, message="No está activa ese oficina")
    if oficina.estatus != "A":
        return OneOficinaOut(success=False, message="Esta oficina está eliminada")
    return OneOficinaOut(success=True, message=f"Detalle de {clave}", data=OficinaOut.model_validate(oficina))


@oficinas.get("", response_model=CustomPage[OficinaOut])
async def paginado(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    distrito_clave: str = None,
    domicilio_clave: str = None,
):
    """Paginado de oficinas que pueden agendar citas"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(Oficina)
    if distrito_clave:
        distrito_clave = safe_clave(distrito_clave)
        if distrito_clave != "":
            consulta = consulta.join(Distrito).filter(Distrito.clave == distrito_clave)
    if domicilio_clave is not None:
        domicilio_clave = safe_clave(domicilio_clave)
        if domicilio_clave != "":
            consulta = consulta.join(Domicilio).filter(Domicilio.clave == domicilio_clave)
    consulta = consulta.filter(Oficina.puede_agendar_citas == True)
    return paginate(consulta.filter(Oficina.es_activo == True).filter(Oficina.estatus == "A").order_by(Oficina.clave))
