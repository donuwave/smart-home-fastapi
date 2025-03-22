from datetime import timedelta, datetime
from typing import Optional
from fastapi import status, HTTPException
import bcrypt
import jwt

from api_v1.auth.schema import CreateToken
from config.settings import app_settings

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


async def hash_password(password_user: str) -> bytes:
    salt = bcrypt.gensalt()
    password_bytes = password_user.encode()
    return bcrypt.hashpw(password_bytes, salt)


async def create_access_token(user_id: int) -> str:
    jwt_payload = {
        "user_id": user_id,
        "sub": "sub",
    }

    token_req = CreateToken(
        token_data=jwt_payload,
        token_type=ACCESS_TOKEN_TYPE,
        expire_minutes=app_settings.auth.access_token_expire_minutes,
    )

    return await create_token(token_req=token_req)


async def create_refresh_token(user_id: int) -> str:
    jwt_payload = {"user_id": user_id, "sub": "sub"}

    token_req = CreateToken(
        token_data=jwt_payload,
        token_type=REFRESH_TOKEN_TYPE,
        expire_minutes=app_settings.auth.refresh_token_expire_days,
    )

    return await create_token(token_req=token_req)


async def create_token(token_req: CreateToken) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_req.token_type}
    jwt_payload.update(token_req.token_data)

    return await encode_jwt(
        payload=jwt_payload, expire_minutes=token_req.expire_minutes
    )


async def validate_password(password_user: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=password_user.encode(), hashed_password=hashed_password
    )


async def encode_jwt(
    payload: dict,
    private_key: str = app_settings.auth.private_key_path.read_text(),
    algorithm: str = app_settings.auth.algorithm,
    expire_minutes: int = app_settings.auth.access_token_expire_minutes,
    expire_timedelta: Optional[timedelta] = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
    return encoded


async def decode_jwt(
    token: str,
    public_key=app_settings.auth.public_key_path.read_text(),
    algorithm: str = app_settings.auth.algorithm,
):
    try:
        decoded = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Токен просрочен"
        )
    except jwt.InvalidKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Токен невалидный"
        )


async def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)

    if current_token_type == token_type:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Инвалидный токен {current_token_type!r} {token_type!r}",
    )
