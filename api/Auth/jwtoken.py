from datetime import datetime, timedelta
import os
import jwt


def create_token(email: str) -> str:
    payload = {"email": email, "expiry": str(datetime.today() + timedelta(days=2))}
    encoded = jwt.encode(payload=payload, key=os.getenv("SECRET_KEY"), algorithm="HS256")
    return encoded


def decode_token(token: str) -> dict:
    decoded = jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=["HS256"])
    return decoded


def check_expiry(data: dict) -> bool:
    expiry_date = data.get("expiry")
    exp_date = datetime.fromisoformat(expiry_date)
    if datetime.today() > exp_date:
        return True
    return False
