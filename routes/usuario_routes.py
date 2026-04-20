from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal

from models.usuario_model import RegistroUsuario, Cliente, Usuario, ActualizarUsuario
from services.auth_service import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


# Conexión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# REGISTRO
@router.post("/registro")
def registro(data: RegistroUsuario, db: Session = Depends(get_db)):
    try:
        cliente = Cliente(
            PrimerNombre=data.primerNombre,
            SegundoNombre=data.segundoNombre,
            PrimerApellido=data.primerApellido,
            SegundoApellido=data.segundoApellido,
            Estado="A"
        )

        db.add(cliente)
        db.commit()
        db.refresh(cliente)

        usuario = Usuario(
            NombreUsuario=data.username,
            Contraseña=hash_password(data.password),
            IdCliente=cliente.IdCliente
        )

        db.add(usuario)
        db.commit()

        return {
            "message": "Usuario registrado correctamente",
            "idCliente": cliente.IdCliente,
            "usuario": data.username
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# LOGIN + JWT
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.NombreUsuario == form_data.username
    ).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario no existe")

    if not verify_password(form_data.password, usuario.Contraseña):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    token = create_access_token({"sub": usuario.NombreUsuario})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# PERFIL (PROTEGIDO)
@router.get("/perfil")
def perfil(
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(get_current_user)
):
    usuario = db.query(Usuario).filter(
        Usuario.NombreUsuario == usuario_actual
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    cliente = db.query(Cliente).filter(
        Cliente.IdCliente == usuario.IdCliente
    ).first()

    return {
        "usuario": usuario.NombreUsuario,
        "nombre": cliente.PrimerNombre,
        "segundoNombre": cliente.SegundoNombre,
        "apellido": cliente.PrimerApellido,
        "segundoApellido": cliente.SegundoApellido
    }

@router.put("/perfil")
def actualizar_perfil(
    data: ActualizarUsuario,
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(get_current_user)
):
    # 1. Buscar usuario logeado
    usuario = db.query(Usuario).filter(
        Usuario.NombreUsuario == usuario_actual
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 2. Buscar cliente relacionado
    cliente = db.query(Cliente).filter(
        Cliente.IdCliente == usuario.IdCliente
    ).first()

    # 3. Actualizar datos
    cliente.PrimerNombre = data.primerNombre
    cliente.SegundoNombre = data.segundoNombre
    cliente.PrimerApellido = data.primerApellido
    cliente.SegundoApellido = data.segundoApellido

    db.commit()

    return {"message": "Perfil actualizado correctamente"}