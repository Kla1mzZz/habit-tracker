from pydantic import BaseModel, EmailStr, Field


class AuthBase(BaseModel):
    email: EmailStr

class AuthRegister(AuthBase):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=100)

class AuthLogin(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
