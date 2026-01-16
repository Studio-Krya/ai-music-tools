from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    name: str
    age: int

class UserDTO(BaseModel):
    id: int
    name: str
    age: int

class UsersResponse(BaseModel):
    data: List[UserDTO]