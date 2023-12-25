from pydantic import BaseModel, Field

class UserLoginRequest(BaseModel):
    user_name : str = Field(default=None)
    pass_word : str = Field(default=None)