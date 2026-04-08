from pydantic import BaseModel


class LoginResponse(BaseModel):
    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    gender: str
    image: str
    accessToken: str
    refreshToken: str
