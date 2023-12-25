from pydantic import BaseModel, Field
from enum import Enum


class UserLoginRequest(BaseModel):
    user_name : str = Field(default=None)
    pass_word : str = Field(default=None)

class User(BaseModel):
    full_name: str
    user_name : str = Field(default=None)
    pass_word : str = Field(default=None)

class UserRegistrationRequest(BaseModel):
    full_name: str = Field(default=None)
    user_name : str = Field(default=None)
    pass_word : str = Field(default=None)