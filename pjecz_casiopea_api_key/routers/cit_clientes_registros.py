"""
Cit Clientes Registros, routers
"""

from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.pwgen import generar_cadena_para_validar
from ..dependencies.safe_string import safe_curp, safe_email, safe_string, safe_telefono, safe_uuid
from ..models.cit_clientes import CitCliente
from ..models.cit_clientes_registros import CitClienteRegistro
from ..models.permisos import Permiso
from ..schemas.cit_clientes_registros import CitClienteRegistroOut, OneCitClienteRegistroOut, CrearCitClienteRegistroIn

EXPIRACION_HORAS = 48

cit_clientes_registros = APIRouter(prefix="/api/v5/cit_clientes_registros")


@cit_clientes_registros.post("/solicitar", response_model=OneCitClienteRegistroOut)
async def solicitar(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    crear_cit_cliente_registro_in: CrearCitClienteRegistroIn,
):
    """Solicitar el registro de un cliente, se va a enviar un mensaje a su e-mail para validar que existe"""
    if current_user.permissions.get("CIT CLIENTES REGISTROS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Validar nombres
    nombres = safe_string(crear_cit_cliente_registro_in.nombres, save_enie=True)
    if nombres == "":
        return OneCitClienteRegistroOut(success=False, message="No son válidos los nombres")

    # Validar apellido_primero
    apellido_primero = safe_string(crear_cit_cliente_registro_in.apellido_primero, save_enie=True)
    if apellido_primero == "":
        return OneCitClienteRegistroOut(success=False, message="No es válido el primer apellido")

    # Se puede omitir apellido_segundo
    apellido_segundo = safe_string(crear_cit_cliente_registro_in.apellido_segundo, save_enie=True)

    # Validar CURP
    try:
        curp = safe_curp(crear_cit_cliente_registro_in.curp)
    except ValueError:
        return OneCitClienteRegistroOut(success=False, message="No es válido el CURP")

    # Validar telefono
    telefono = safe_telefono(crear_cit_cliente_registro_in.telefono)
    if telefono == "":
        return OneCitClienteRegistroOut(success=False, message="No es válido el teléfono")

    # Validar email
    try:
        email = safe_email(crear_cit_cliente_registro_in.email)
    except ValueError:
        return OneCitClienteRegistroOut(success=False, message="No es válido el email")

    # Verificar que no exista un cliente con ese CURP
    if database.query(CitCliente).filter_by(curp=curp).first() is not None:
        return OneCitClienteRegistroOut(success=False, message="No puede registrarse porque ya existe una cuenta con ese CURP")

    # Verificar que no exista un cliente con ese correo electrónico
    if database.query(CitCliente).filter_by(email=email).first() is not None:
        return OneCitClienteRegistroOut(success=False, message="No puede registrarse porque ya existe una cuenta con ese email")

    # Verificar que no haya un registro pendiente con ese CURP
    if (
        database.query(CitClienteRegistro).filter_by(curp=curp).filter_by(ya_registrado=False).filter_by(estatus="A").first()
        is not None
    ):
        return OneCitClienteRegistroOut(success=False, message="Ya hay una solicitud de registro para ese CURP")

    # Verificar que no haya un registro pendiente con ese correo electrónico
    if (
        database.query(CitClienteRegistro).filter_by(email=email).filter_by(ya_registrado=False).filter_by(estatus="A").first()
        is not None
    ):
        return OneCitClienteRegistroOut(success=False, message="Ya hay una solicitud de registro para ese correo electrónico")

    # Insertar
    cit_cliente_registro = CitClienteRegistro(
        nombres=nombres,
        apellido_primero=apellido_primero,
        apellido_segundo=apellido_segundo,
        curp=curp,
        telefono=telefono,
        email=email,
        expiracion=datetime.now() + timedelta(hours=EXPIRACION_HORAS),
        cadena_validar=generar_cadena_para_validar(),
    )
    database.add(cit_cliente_registro)
    database.commit()
    database.refresh(cit_cliente_registro)

    # TODO: Agregar tarea en el fondo para que se envie un mensaje via correo electrónico

    # Entregar
    return OneCitClienteRegistroOut.model_validate(cit_cliente_registro)


@cit_clientes_registros.get("/{cit_cliente_registro_id}", response_model=OneCitClienteRegistroOut)
async def detalle(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cliente_registro_id: str,
):
    """Detalle de un registro a partir de su ID"""
    if current_user.permissions.get("CIT CLIENTES REGISTROS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente_registro_id = safe_uuid(cit_cliente_registro_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la UUID")
    cit_cliente_registro = database.query(CitClienteRegistro).get(cit_cliente_registro_id)
    if not cit_cliente_registro:
        return OneCitClienteRegistroOut(success=False, message="No existe ese registro")
    if cit_cliente_registro.estatus != "A":
        return OneCitClienteRegistroOut(success=False, message="No está habilitada ese registro")
    return OneCitClienteRegistroOut(
        success=True,
        message=f"Detalle de {cit_cliente_registro_id}",
        data=CitClienteRegistroOut.model_validate(cit_cliente_registro),
    )


@cit_clientes_registros.get("", response_model=CustomPage[CitClienteRegistroOut])
async def paginado(
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
