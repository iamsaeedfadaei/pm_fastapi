import string
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, constr, validator


class CoreModel(BaseModel):
    pass


def validate_username(username: str) -> str:
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(char in allowed for char in username), "کاراکترهای نام کاربری صحیح نیست"
    assert len(username) >= 3, "ظول نام کاربری باید بیشتر از سه کاراکتر باشد"
    return username


def validate_password(password: str) -> str:
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(char in allowed for char in password), "در رمز از کاراکترهای صحیح استفاده نشده است"
    assert len(password) >= 10 and len(password) <= 100, "ظول نام کاربری باید بین سه و صد کاراکتر باشد"


def validate_national_id(national_id: int) -> int:
    assert len(national_id) == 10, "کد ملی معتبر نیست"
    return national_id


class UserBase(BaseModel):
    email: EmailStr = Field(...)
    password: constr(min_length=10, max_length=100)
    username: str = Field(...)
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    national_id: str = Field(..., max_length=100)
    is_active: bool = True
    is_superuser: bool = False

    class Config:
        schema_extra = {
            "example": {
                "first_name": "نام",
                "last_name": "نام خانوادگی",
                "username": "نام کاربری",
                "email": "ایمیل",
                "national_id": "کد ملی",
                "password": "رمز (باید از بین کاراکترهای انگلیسی، اعداد با طول بین ده تا ۱۰۰ کاراکتر باشد)"
            }
        }


class UserCreate(CoreModel):
    email: EmailStr
    password: constr(min_length=10, max_length=100)
    username: str

    @validator("username", pre=True)
    def username_is_valid(cls, username: str) -> str:
        return validate_username(username)


class UserUpdate(CoreModel):
    email: EmailStr
    username: str

    @validator("username", pre=True)
    def username_is_valid(cls, username: str) -> str:
        return validate_username(username)


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: constr(min_length=10, max_length=100)

    class Config:
        schema_extra = {
            "example": {
                "email": "ایمیل",
                "password": "رمز"
            }
        }
