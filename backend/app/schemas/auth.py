from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    status: str = "ACTIVE"
    is_active: bool = True
    created_at: datetime
    last_login: Optional[datetime] = None
    days_inactive: Optional[int] = None
    prediction_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class UserStatusUpdate(BaseModel):
    status: str # "ACTIVE", "DISABLED", "INACTIVE"

class AdminUserListResponse(BaseModel):
    total: int
    active_count: int
    inactive_count: int
    disabled_count: int
    users: List[UserResponse]

class SearchSource(BaseModel):
    title: str
    url: str

class ChatMessageItem(BaseModel):
    role: str # "user" or "model" / "assistant"
    text: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessageItem]] = None

class ChatResponse(BaseModel):
    reply: str
    sources: List[SearchSource] = []
    search_performed: bool = False
