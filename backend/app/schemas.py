from datetime import datetime
from pydantic import BaseModel

class ProblemCreate(BaseModel):
    problem_text: str
    known_answer: str

class Problem(ProblemCreate):
    id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode: True

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenData(BaseModel):
    username: str | None = None

class Solution(BaseModel):
    solution: str