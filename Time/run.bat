@echo off
chcp 65001 > nul
echo 🚀 Запуск приложения Табель учета...
echo.
streamlit run app.py --server.port 8501 --server.address localhost
pause