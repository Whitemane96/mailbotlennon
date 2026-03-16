from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(Token):
    must_change_password: bool
    can_change_password: bool
    role: str


class TokenData(BaseModel):
    email: str | None = None


class UserBase(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    must_change_password: bool = False
    can_change_password: bool = True

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    created_at: datetime | None = None


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str


class AdminInviteUserRequest(BaseModel):
    email: EmailStr
    role: str = "user"
    can_change_password: bool = True


class AdminResetPasswordResponse(BaseModel):
    user_id: int
    temp_password: str


class AdminCreateUser(BaseModel):
    email: EmailStr
    role: str = "user"


class AdminCreatedUserResponse(BaseModel):
    email: EmailStr
    role: str
    temp_password: str
    must_change_password: bool
    can_change_password: bool


class AdminUpdateUserFlags(BaseModel):
    can_change_password: Optional[bool] = None
    is_active: Optional[bool] = None
    must_change_password: Optional[bool] = None
    role: Optional[Literal["admin", "manager", "user"]] = None


class EmailCheckResponse(BaseModel):
    exists: bool
    must_change_password: Optional[bool] = None
    role: Optional[str] = None