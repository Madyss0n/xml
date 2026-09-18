@echo off
chcp 65001 > nul
echo 🚀 Запуск Табель учета...
echo.
echo 📊 Открывается приложение в браузере...
echo.
echo Если браузер не открылся, перейдите по адресу:
echo http://localhost:8501
echo.

REM Пробуем самый надежный способ
python -c "import streamlit.web.cli as stcli; import sys; sys.argv = ['streamlit', 'run', 'app.py', '--server.port', '8501']; stcli.main()"

if errorlevel 1 (
    echo.
    echo ❌ Ошибка запуска!
    echo Попробуйте запустить вручную:
    echo python -m streamlit run app.py
    echo.
    pause
)