import jwt
import uuid

from fastapi import HTTPException, status

from datetime import datetime, timedelta, timezone

from src.settings import jwt_settings


def create_jwt_token(payload: dict, expire_delta: timedelta) -> str:
    to_encode = payload.copy()

    jti = str(uuid.uuid4())
    iat = datetime.now(timezone.utc)
    exp = iat + expire_delta

    to_encode.update({
        'jti': jti,
        'iat': iat,
        'exp': exp,
    })
    
    jwt_token = jwt.encode(
        to_encode,
        jwt_settings.JWT_PRIVATE_KEY,
        jwt_settings.JWT_ALGORITHM,
    )

    return jwt_token

def verify_jwt_token(jwt_token: str) -> dict:
    try:
        payload = jwt.decode(
            jwt_token,
            jwt_settings.JWT_PUBLIC_KEY,
            [jwt_settings.JWT_ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
    except jwt.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
