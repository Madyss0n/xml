@echo off
chcp 65001 > nul
echo ============================================
echo 🔧 Диагностика и запуск
echo ============================================
echo.

echo Проверка Python...
python --version
echo.

echo Проверка установленных пакетов...
python -c "import sys; print('Путь Python:', sys.executable)"
echo.

echo Попытка найти streamlit...
python -c "import streamlit; print('✅ Streamlit найден, версия:', streamlit.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ Streamlit не найден!
    echo Устанавливаю...
    python -m pip install streamlit
)

echo.
echo ============================================
echo 🚀 Запуск приложения...
echo ============================================
python -m streamlit run app.py --server.port 8501 --server.address localhost
pause