import json
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from ...models import Register, UpdateUser, UserData
from ...database import User
import phonenumbers
from passlib.context import CryptContext
from ...Auth import create_token, handletoken
from ...utils import check_is_None

user = APIRouter(prefix="/api/v1", tags=["User"])


def getHashedPassword(password: str) -> str:
    pwd = CryptContext(schemes=["bcrypt"])
    return pwd.hash(password)


@user.post(
    "/register",
    summary="Register Yourself",
    description="Register here to explore the API",
    response_description="Registered Successfully",
    status_code=status.HTTP_201_CREATED,
)
def registeruser(register: Register):
    phno = phonenumbers.parse(str(register.phoneno), region="IN")
    if not phonenumbers.is_valid_number(phno):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="The Phone Number is Invalid"
        )
    data = User.objects(email=register.email).values_list("email")
    if len(data) != 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The email address is already registered use login",
        )
    register.password = getHashedPassword(register.password)
    User(**register.model_dump()).save()
    return {"message": "Registered Successfully"}


@user.get(
    "/login",
    summary="Login To get the Access Token",
    description="Provide the Registered Email and Password to login to get the Access Token.",
    response_description="Access Token Generated",
    status_code=status.HTTP_200_OK,
)
def loginuser(email: EmailStr, password: str):
    datas = User.objects(email=email).scalar("id", "email", "name", "password").first()
    if datas is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"Email ID={email} Not Found",
                "help": "Register Yourself with email ID first.",
            },
        )
    pwd = CryptContext(schemes=["bcrypt"])
    if not pwd.verify(password, datas[3]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is Invalid")
    return {"message": "Login Success", "Access Token": create_token(email)}


@user.get(
    "/me",
    response_model=UserData,
    summary="Get Details About Yourself",
    description="Know your own Details by Token in the Header",
    response_description="Your Details",
)
def getMyself(uData: tuple = Depends(handletoken)):
    email = uData[2]
    data = User.objects(email=email).fields(password=0, id=0, carts=0).first().to_json()
    data = json.loads(data)
    return data


@user.put(
    "/update",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update your Data",
)
def updateuser(user: UpdateUser, uData: tuple = Depends(handletoken)):
    """Update your phone no or various fields.

    **Note** : But You Cannot Update Email ID once Registered."""
    data = User.objects(email=uData[2]).fields(id=0, carts=0).first()
    upassword = None
    if user.password is not None:
        upassword = getHashedPassword(user.password)
    dictupdate = {
        "$set": {
            "name": check_is_None(user.name, data.name),
            "phoneno": check_is_None(user.phoneno, data.phoneno),
            "age": check_is_None(user.age, data.age),
            "address": check_is_None(user.address, data.address),
            "city": check_is_None(user.city, data.city),
            "state": check_is_None(user.state, data.state),
            "pincode": check_is_None(user.pincode, data.pincode),
            "password": check_is_None(upassword, data.password),
        }
    }
    User.objects(email=uData[2]).update_one(__raw__=dictupdate)
    return {"message": "Updated Successfully"}
