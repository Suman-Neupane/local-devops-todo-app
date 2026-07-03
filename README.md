# Local DevOps Todo App

![CI Pipeline](https://github.com/your-username/todo-devops-project/actions/workflows/ci.yml/badge.svg)

A complete Todo web application built to demonstrate modern DevOps practices.

## Tech Stack
- **Backend:** Python + Flask
- **Frontend:** HTML + CSS + JS (Vanilla, Dark Mode)
- **Testing:** pytest
- **Containerization:** Docker
- **Orchestration:** Docker Compose
- **CI/CD:** GitHub Actions

## Run Locally (Docker Compose)

The easiest way to run the application is using Docker Compose:

```bash
docker compose up -d
```

Access the app at: http://localhost:8080

## Run Locally (Manual)

### 1. Install Dependencies
```bash
pip install -r app/requirements.txt
```

### 2. Run Tests
```bash
PYTHONPATH=. pytest app/tests/ -v
```

### 3. Start App
```bash
python app/app.py
```

## GitHub Actions CI

This project includes a continuous integration pipeline (`.github/workflows/ci.yml`) that runs on every push and pull request. It automatically:
1. Checks out the code
2. Installs dependencies
3. Runs the pytest suite
4. Builds the Docker image to ensure it's healthy
