import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import User, Server, Deployment, Pipeline
from .schemas import LoginRequest, TokenResponse, UserOut, ServerOut, DeploymentOut, PipelineOut
from .security import verify_password, create_token
from .deps import current_user

router = APIRouter(prefix="/api")

@router.post("/auth/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return TokenResponse(access_token=create_token(user.id))

@router.get("/auth/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _: User = Depends(current_user)):
    servers = db.query(Server).all()
    return {
        "servers": len(servers),
        "servers_up": sum(s.status == "UP" for s in servers),
        "servers_down": sum(s.status != "UP" for s in servers),
        "deployments": db.query(Deployment).count(),
        "pipelines": db.query(Pipeline).count(),
        "successful_pipelines": db.query(Pipeline).filter(Pipeline.status == "SUCCESS").count(),
        "failed_pipelines": db.query(Pipeline).filter(Pipeline.status == "FAILED").count(),
        "timestamp": int(time.time())
    }

@router.get("/servers", response_model=list[ServerOut])
def servers(db: Session = Depends(get_db), _: User = Depends(current_user)):
    return db.query(Server).order_by(Server.id).all()

@router.get("/deployments", response_model=list[DeploymentOut])
def deployments(db: Session = Depends(get_db), _: User = Depends(current_user)):
    return db.query(Deployment).order_by(Deployment.id.desc()).all()

@router.get("/pipelines", response_model=list[PipelineOut])
def pipelines(db: Session = Depends(get_db), _: User = Depends(current_user)):
    return db.query(Pipeline).order_by(Pipeline.id.desc()).all()

@router.get("/containers")
def containers(_: User = Depends(current_user)):
    try:
        import docker
        client = docker.from_env()
        result = []
        for c in client.containers.list(all=True):
            result.append({"id": c.short_id, "name": c.name, "image": c.image.tags[0] if c.image.tags else c.image.short_id, "status": c.status})
        return result
    except Exception:
        return []

@router.get("/health")
def health():
    return {"status": "healthy"}

@router.get("/metrics")
def metrics(_: User = Depends(current_user)):
    return {"cpu": [32, 41, 37, 52, 48, 44, 39], "memory": [61, 55, 63, 68, 66, 64, 62], "disk": [48, 52, 57, 61, 64, 67, 70]}
