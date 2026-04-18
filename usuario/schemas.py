from pydantic import BaseModel

# REGISTRO
class RegistroUsuario(BaseModel):
    username: str
    password: str
    primerNombre: str
    segundoNombre: str | None = None
    primerApellido: str
    segundoApellido: str | None = None


#LOGIN 
class LoginUsuario(BaseModel):
    username: str
    password: str

