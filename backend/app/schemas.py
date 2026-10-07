from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    model_config = ConfigDict(from_attributes=True)

class ServerOut(BaseModel):
    id: int
    name: str
    host: str
    environment: str
    status: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    model_config = ConfigDict(from_attributes=True)

class DeploymentOut(BaseModel):
    id: int
    application: str
    version: str
    environment: str
    status: str
    commit_sha: str
    deployed_by: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PipelineOut(BaseModel):
    id: int
    name: str
    branch: str
    status: str
    duration_seconds: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
