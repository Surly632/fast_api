from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import Text, delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer
from fastapi import APIRouter, Depends, HTTPException, Header, Request
import bcrypt

from model.pydantic.UserModel import UserModel as user_model
from dependency.db_dependency import get_db
from service.UserService import UserService
from model.database.NoteModel import UserModel as db_user_model
from service.JwtService import JwtService

user_service = UserService()

router = APIRouter(prefix="/user")


@router.post("/create")
async def create_user(user_data: user_model, db: AsyncSession = Depends(get_db)):
    user_data_dict = user_data.dict()
    hashed_pass = user_data_dict.get("password").encode("utf-8")
    hashed_pass = bcrypt.hashpw(hashed_pass, bcrypt.gensalt())
    user_data_dict.update({"password": hashed_pass.decode("utf-8")})
    db_user_data = db_user_model(**user_data_dict)
    return await user_service.create_user(db_user_data, db)


@router.post("/login")
async def login_user(req: Request, db: AsyncSession = Depends(get_db)):
    user_data = await req.json()
    username = user_data.get("username")
    password = user_data.get("password")
    password_byte = password.encode("utf-8")

    statement = select(db_user_model).where(db_user_model.username == username)
    user_data_from_db = await db.execute(statement)
    fetched_user_data = user_data_from_db.fetchone()
    user_instance = fetched_user_data[0]

    db_username = user_instance.username
    db_password = user_instance.password
    db_password_byte = db_password.encode("utf-8")
    matched_pass = bcrypt.checkpw(password_byte, db_password_byte)
    if matched_pass:
        jwt_service = JwtService()
        data = {"username": username, "issuer": "abm_himel", "sub": username}
        token = jwt_service.generate_token(data)
        return {"success": True, "token": token}
    else:
        raise HTTPException(status_code=403, detail="password did not match")


from config.JwtBearer import JwtBearer


@router.get("/getuserdetails", dependencies=[Depends(JwtBearer())])
async def userDetails(
    current_user: HTTPAuthorizationCredentials = Depends(JwtBearer().get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(db_user_model)
    execution = await db.execute(stmt)
    res = execution.scalars().all()
    # print(res[0].first_name)
    user_dict = [k.to_dict() for k in res]
    return {"user data": user_dict}


@router.post("/update")
async def update_user(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.json()
    user_id = request.query_params.get("id")
    print(payload)
    if not user_id:
        raise HTTPException(
            status_code=400, detail="User ID not provided in the payload"
        )
    statement = select(db_user_model).where(db_user_model.id == user_id)
    existing_user = await db.execute(statement)
    row = existing_user.scalar()
    print(f"row is: {row}")
    if row is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    row.update({key: value for key, value in payload.items()})

    await db.commit()

    return {"message": "User updated successfully"}


@router.delete("/delete")
async def delete_user(req: Request, db: AsyncSession = Depends(get_db)):
    user_id = req.query_params.get("id")
    statement = delete(db_user_model).where(db_user_model.id == user_id)
    res = await db.execute(statement)
    await db.commit()
    if res.rowcount > 0:
        return {"success": True, "message": "User Deleted"}
    else:
        raise HTTPException(status_code=404, detail=f"user with id {user_id} not found")


from pydantic import BaseModel


class Test(BaseModel):
    id: str
    name: str
    email: str


from fastapi import Request


@router.post("/test")
async def test_api(test_data: Test, req: Request):
    # Accessing header information
    authorization_header = req.headers.get("Authorization")
    jwt_token = (
        authorization_header.split("Bearer ")[-1] if authorization_header else None
    )
    print(f"jwt token: {jwt_token}")

    return {"message": "Success"}
