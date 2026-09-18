@echo off
chcp 65001 > nul
echo ============================================
echo 🚀 ЗАПУСК ПРИЛОЖЕНИЯ ТАБЕЛЬ УЧЕТА
echo ============================================
echo.

echo Проверка окружения...
python check_env.py

echo.
echo ============================================
echo 🚀 Запуск Streamlit...
echo ============================================
echo.

REM Пробуем разные способы запуска
echo 1. Пробую: python -m streamlit run app.py
python -m streamlit run app.py --server.port 8501 --server.address localhost --server.enableCORS false --server.enableXsrfProtection false

if errorlevel 1 (
    echo.
    echo ⚠️ Способ 1 не сработал, пробую способ 2...
    echo.
    
    echo 2. Пробую: streamlit run app.py
    streamlit run app.py --server.port 8501 --server.address localhost --server.enableCORS false --server.enableXsrfProtection false
    
    if errorlevel 1 (
        echo.
        echo ⚠️ Способ 2 не сработал, пробую способ 3...
        echo.
        
        echo 3. Пробую: python -c "import streamlit.web.cli as stcli; import sys; sys.argv = ['streamlit', 'run', 'app.py', '--server.port', '8501']; stcli.main()"
        python -c "import streamlit.web.cli as stcli; import sys; sys.argv = ['streamlit', 'run', 'app.py', '--server.port', '8501']; stcli.main()"
        
        if errorlevel 1 (
            echo.
            echo ❌ Все способы запуска не сработали!
            echo.
            echo Возможные причины:
            echo 1. Streamlit не установлен - запустите install.bat
            echo 2. Порт 8501 занят - попробуйте другой порт
            echo 3. Ошибка в коде app.py
            echo.
            echo Для диагностики запустите: python check_env.py
            echo.
            pause
            exit /b 1
        )
    )
)

echo.
echo ✅ Приложение запущено!
pause