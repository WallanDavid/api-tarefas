import os

arquivos = {
    "requirements.txt": """fastapi
uvicorn[standard]
celery[redis]
redis
sqlalchemy
pydantic
""",
    "Dockerfile": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
""",
    "docker-compose.yml": """version: "3.9"

services:
  api:
    build: .
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - redis

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  worker:
    build: .
    command: celery -A app.celery_worker.celery_app worker --loglevel=info
    depends_on:
      - redis
""",
    "app/__init__.py": "",
    "app/database.py": """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
""",
    "app/models.py": """from sqlalchemy import Column, Integer, String
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="pendente")  # pendente | em_andamento | concluido
""",
    "app/schemas.py": """from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str

class TaskCreate(TaskBase):
    pass

class TaskUpdateStatus(BaseModel):
    status: str

class TaskOut(TaskBase):
    id: int
    status: str

    class Config:
        orm_mode = True
""",
    "app/tasks.py": """from celery import shared_task
import time

@shared_task
def process_task(task_id: int):
    print(f"Iniciando tarefa {task_id}...")
    time.sleep(5)
    print(f"Tarefa {task_id} concluída.")
    return f"Tarefa {task_id} finalizada"
""",
    "app/celery_worker.py": """from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.autodiscover_tasks(["app"])
""",
    "app/main.py": """from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database, tasks
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Tarefas")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    tasks.process_task.delay(db_task.id)
    return db_task

@app.get("/tasks/", response_model=list[schemas.TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@app.patch("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, status: schemas.TaskUpdateStatus, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    task.status = status.status
    db.commit()
    db.refresh(task)
    return task
"""
}

# Cria as pastas necessárias
os.makedirs("app", exist_ok=True)

# Cria e escreve os arquivos
for caminho, conteudo in arquivos.items():
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)

print("✅ Projeto gerado com sucesso!")
