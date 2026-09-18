@echo off
chcp 65001 > nul
echo 🚀 Запуск приложения Табель учета...
echo.
echo 📊 Отключаем аналитику Streamlit...
echo.

python -m streamlit run app.py --server.port 8501 --server.address localhost --server.enableCORS false --server.enableXsrfProtection false --browser.gatherUsageStats false

pause