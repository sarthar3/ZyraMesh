.PHONY: help install test test-backend test-frontend dev dev-backend dev-frontend build docker-up docker-down

help:
	@echo "Zyra Mesh Development Commands:"
	@echo "  make dev          - Run both backend and frontend locally"
	@echo "  make dev-backend  - Start FastAPI backend server"
	@echo "  make dev-frontend - Start React Vite frontend server"
	@echo "  make test         - Run backend and frontend test suites"
	@echo "  make build        - Build production bundles"
	@echo "  make docker-up    - Start Docker Compose containers"
	@echo "  make docker-down  - Stop Docker Compose containers"

install:
	cd backend && .venv\Scripts\pip install -r requirements.txt
	cd frontend && npm install

test-backend:
	cd backend && .venv\Scripts\pytest

test-frontend:
	cd frontend && npm run build

test: test-backend test-frontend

dev-backend:
	cd backend && .venv\Scripts\uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

build:
	cd frontend && npm run build

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down
