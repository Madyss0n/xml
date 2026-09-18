@echo off
chcp 65001 > nul
echo ============================================
echo 🚀 ЗАПУСК С АВТОМАТИЧЕСКИМ ПЕРЕЗАПУСКОМ
echo ============================================
echo.

:start
echo 📊 Запуск приложения...
python -m streamlit run app.py --server.port 8501 --server.address localhost --server.enableCORS false --server.enableXsrfProtection false

if errorlevel 1 (
    echo.
    echo ⚠️ Приложение остановилось с ошибкой
    echo Перезапуск через 5 секунд...
    timeout /t 5 /nobreak
    goto start
)

pause