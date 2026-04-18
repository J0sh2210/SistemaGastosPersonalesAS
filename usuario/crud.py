from sqlalchemy.orm import Session
from .models import Cliente, CuentaUsuario
from .auth import hash_password

def crear_usuario(db: Session, username, password, nombre, apellido):
    cliente = Cliente(
        PrimerNombre=nombre,
        PrimerApellido=apellido
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    cuenta = CuentaUsuario(
        NombreUsuario=username,
        Contraseña=hash_password(password),
        IdCliente=cliente.IdCliente
    )

    db.add(cuenta)
    db.commit()

    return cuenta