from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from modules.auth import schemas
from modules.auth.dependencies import get_current_user
from modules.auth.service import create_access_token, verify_password
from modules.usuarios.models import Usuario

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.correo == payload.correo).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token({"sub": str(user.id_usuario), "rol": user.rol})
    return schemas.TokenResponse(access_token=token)


@router.get("/me", response_model=schemas.CurrentUser)
def me(current_user=Depends(get_current_user)):
    return schemas.CurrentUser(
        id_usuario=current_user.id_usuario,
        nombre=current_user.nombre,
        correo=current_user.correo,
        rol=current_user.rol,
    )
