from fastapi import FastAPI, Depends, HTTPException
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

    # 🔁 Proteção contra falha do Redis/Celery — evita erro 500
    try:
        tasks.process_task.delay(db_task.id)
    except Exception as e:
        print(f"⚠️ Erro ao enviar tarefa para Celery: {e}")

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
