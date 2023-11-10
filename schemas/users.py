from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    is_registered: bool = False
    password: str
    confirm_password: str


class UserLogin(UserBase):
    password: str


class UserInfo(UserBase):
    id: int
    fullname: str

