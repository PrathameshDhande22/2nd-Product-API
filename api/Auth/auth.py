from fastapi.security import APIKeyHeader
from fastapi import HTTPException, Security, status
from jwt import DecodeError
from .jwtoken import decode_token, check_expiry
from ..database import User

apikey = APIKeyHeader(
    name="Authorization",
    auto_error=False,
    description="Add the Authorization with Access Token in the Header to Explore the API",
)


def handletoken(token: str = Security(apikey)):
    """Checks the token if its expired or decode the token and checks in the database"""
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Add the Token in the Header",
        )
    replaceToken = token.removeprefix("Bearer ")
    try:
        payloadata = decode_token(token=replaceToken)
        datas = User.objects(email=payloadata.get("email")).scalar("name", "id", "email").first()
        if datas is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token !")
        if check_expiry(payloadata):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": "Your Access Token is Expired",
                    "help": "Login Again to create new Access Token",
                },
            )
        return datas
    except DecodeError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Token !")
