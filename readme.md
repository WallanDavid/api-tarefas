# ✅ API de Tarefas

Uma API de gerenciamento de tarefas assíncronas com FastAPI, Celery e Redis, empacotada com Docker Compose.

## 🚀 Tecnologias

- Python 3.11
- FastAPI
- SQLAlchemy + SQLite
- Celery + Redis
- Docker + Docker Compose

## 📦 Instalação com Docker

Pré-requisitos: Docker e Docker Compose instalados.

### 1. Clone o projeto

```bash
git clone https://github.com/seu-usuario/api-tarefas.git
cd api-tarefas
```

### 2. Suba os containers

```bash
docker-compose up --build
```

O servidor FastAPI estará disponível em `http://localhost:8000`, e o Celery worker será iniciado em segundo plano.

## 🔍 Testando a API

Abra o navegador em:

```
http://localhost:8000/docs
```

Você verá a documentação Swagger com as seguintes rotas:

### ▶️ Criar tarefa (POST /tasks/)

Cria uma nova tarefa com título e descrição.

```json
{
  "title": "Estudar FastAPI",
  "description": "Aprender a usar Celery com Redis"
}
```

### 📋 Listar tarefas (GET /tasks/)

Retorna todas as tarefas registradas.

### 🛠 Atualizar status (PATCH /tasks/{task_id})

Atualiza o status da tarefa. Exemplo:

```json
{
  "status": "concluido"
}
```

Valores aceitos:

- `"pendente"`
- `"em andamento"`
- `"concluido"`

## 📁 Estrutura do Projeto

```
task_api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── tasks.py
│   └── celery_worker.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── wait-for-it.sh
```

## 🛠 Comandos úteis

Subir os containers:

```bash
docker-compose up --build
```

Parar os containers:

```bash
docker-compose down
```

Ver logs do worker:

```bash
docker-compose logs -f worker
```

## ℹ️ Observações

- O Celery usa Redis como broker e backend.
- O worker é responsável por processar tarefas após o `POST /tasks/`.
- O banco de dados utilizado é SQLite (ideal para testes locais).

## 📄 Licença

MIT © 2025
