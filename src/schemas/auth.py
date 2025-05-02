from pydantic import BaseModel, EmailStr, Field


class AuthBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)


class AuthRegister(AuthBase):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
