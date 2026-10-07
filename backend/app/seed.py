from sqlalchemy.orm import Session
from .models import User, Server, Deployment, Pipeline
from .security import hash_password

def seed(db: Session):
    if not db.query(User).first():
        db.add(User(email="admin@example.com", password_hash=hash_password("admin123"), role="ADMIN"))
    if not db.query(Server).first():
        db.add_all([
            Server(name="production-api-01", host="10.0.0.10", environment="production", status="UP", cpu_percent=32, memory_percent=61, disk_percent=48),
            Server(name="production-api-02", host="10.0.0.11", environment="production", status="UP", cpu_percent=41, memory_percent=55, disk_percent=52),
            Server(name="database-01", host="10.0.0.20", environment="production", status="UP", cpu_percent=28, memory_percent=73, disk_percent=81),
            Server(name="worker-01", host="10.0.0.30", environment="production", status="DOWN", cpu_percent=0, memory_percent=0, disk_percent=0),
        ])
    if not db.query(Deployment).first():
        db.add_all([
            Deployment(application="frontend", version="v1.4.2", environment="production", status="SUCCESS", commit_sha="7e91ab2", deployed_by="admin@example.com"),
            Deployment(application="backend", version="v2.8.1", environment="production", status="SUCCESS", commit_sha="4b22c91", deployed_by="admin@example.com"),
            Deployment(application="payments", version="v3.1.0", environment="staging", status="FAILED", commit_sha="aa31f02", deployed_by="admin@example.com"),
        ])
    if not db.query(Pipeline).first():
        db.add_all([
            Pipeline(name="backend-ci", branch="main", status="SUCCESS", duration_seconds=261),
            Pipeline(name="frontend-ci", branch="main", status="SUCCESS", duration_seconds=184),
            Pipeline(name="payments-deploy", branch="release", status="FAILED", duration_seconds=322),
        ])
    db.commit()
