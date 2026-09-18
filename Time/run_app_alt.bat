@echo off
echo 🚀 Запуск приложения Табель учета...
echo.
if errorlevel 1 (
    echo Использую python -m streamlit...
    python -m streamlit run app.py --server.port 8501 --server.address localhost
) else (
    python -m streamlit run app.py --server.port 8501 --server.address localhost
)
pause
