@echo off
TITLE Zyra Mesh - Distillation as a Service (DaaS) Launcher
echo ============================================================
echo   Starting Zyra Mesh & Distillation as a Service (DaaS)
echo ============================================================
echo.

echo [1/2] Launching Backend FastAPI Server (Port 8000)...
start "Zyra Mesh Backend" cmd /k "cd /d %~dp0backend && .venv\Scripts\activate && uvicorn app.main:app --port 8000 --reload"

echo [2/2] Launching Frontend Dashboard (Port 3000)...
start "Zyra Mesh Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ============================================================
echo   Both services are starting up!
echo   - Frontend: http://localhost:3000 (or http://localhost:5173)
echo   - Backend API Docs: http://localhost:8000/docs
echo   - Distillation Studio: http://localhost:3000/distill
echo ============================================================
pause
