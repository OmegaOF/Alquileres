from pydantic import BaseModel


class LoginRequest(BaseModel):
    correo: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUser(BaseModel):
    id_usuario: int
    nombre: str
    correo: str
    rol: str
