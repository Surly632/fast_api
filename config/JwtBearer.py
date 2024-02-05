from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from fastapi import  HTTPException, Request
import os


class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials: HTTPAuthorizationCredentials = await super(
            JwtBearer, self
        ).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid Authentication Scheme"
                )

            verify_status = self.verify_token(credentials.credentials)
            if not verify_status:
                raise HTTPException(status_code=403, detail="Invalid token")

            elif verify_status:
                return credentials.credentials

            else:
                raise HTTPException(status_code=403, detail="Invalid Token")
        else:
            raise HTTPException(
                status_code=403, detail="Authentication Scheme Not Found!"
            )

    def verify_token(self, token: str):
        try:
            secret_key = os.getenv("SECRET_KEY")
            jwt_algorithm = os.getenv("ALGORITHM")
            payload = jwt.decode(token, secret_key, jwt_algorithm)
            if payload:
                return True
        except Exception as e:
            return False

    async def get_current_user(self, request: Request):
        token = request.headers.get("Authorization").split("Bearer ")[-1]
        user_data = jwt.decode(token,os.getenv('SECRET_KEY'),os.getenv('ALGORITHM'))
        return user_data
