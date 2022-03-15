from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app import oauth2, schemas

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    access_token = oauth2.create_access_token(data = {"user_id": user_credentials.username})
    return {"access_token": access_token, "token_type": "bearer"}