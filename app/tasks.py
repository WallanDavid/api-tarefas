from celery import shared_task
import time

@shared_task
def process_task(task_id: int):
    print(f"Iniciando tarefa {task_id}...")
    time.sleep(5)
    print(f"Tarefa {task_id} concluída.")
    return f"Tarefa {task_id} finalizada"
