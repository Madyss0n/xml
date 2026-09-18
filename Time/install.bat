@echo off
chcp 65001 > nul
echo ============================================
echo 📊 Установка приложения Табель учета
echo ============================================
echo.

echo Проверка наличия Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    echo.
    echo Пожалуйста, установите Python с сайта:
    echo https://www.python.org/downloads/
    echo.
    echo ВАЖНО: При установке Python отметьте галочку
    echo "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python найден!
echo.

echo Проверка наличия pip...
pip --version > nul 2>&1
if errorlevel 1 (
    echo ❌ pip не найден!
    echo Обновление pip...
    python -m ensurepip --upgrade
)

echo.
echo Проверка наличия requirements.txt...
if not exist "requirements.txt" (
    echo ⚠️ Файл requirements.txt не найден, создаю...
    (
        echo streamlit>=1.28.0
        echo pandas>=2.0.0
        echo openpyxl>=3.1.0
        echo xlrd>=2.0.0
        echo numpy>=1.24.0
    ) > requirements.txt
    echo ✅ Файл requirements.txt создан
)

echo.
echo Установка зависимостей...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ Ошибка при установке зависимостей!
    echo Попробуйте установить вручную:
    echo python -m pip install streamlit pandas openpyxl xlrd numpy
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Зависимости установлены!
echo.

echo Проверка установки Streamlit...
python -c "import streamlit" > nul 2>&1
if errorlevel 1 (
    echo ⚠️ Streamlit не найден в Python, устанавливаю повторно...
    python -m pip install streamlit --force-reinstall
)

echo.
echo Создание файла для запуска...
(
    echo @echo off
    echo chcp 65001 > nul
    echo echo 🚀 Запуск приложения Табель учета...
    echo echo.
    echo echo 📊 Открывается приложение...
    echo echo.
    echo python -m streamlit run app.py --server.port 8501 --server.address localhost
    echo pause
) > run_app.bat

echo.
echo Создание файла для запуска (альтернативный)...
(
    echo @echo off
    echo chcp 65001 > nul
    echo echo 🚀 Запуск приложения Табель учета...
    echo echo.
    echo where streamlit > nul 2>&1
    echo if errorlevel 1 ^(
    echo     echo Использую python -m streamlit...
    echo     python -m streamlit run app.py --server.port 8501 --server.address localhost
    echo ^) else ^(
    echo     streamlit run app.py --server.port 8501 --server.address localhost
    echo ^)
    echo pause
) > run_app_alt.bat

echo.
echo ============================================
echo ✅ Установка завершена!
echo.
echo 🚀 Для запуска приложения запустите файл:
echo    run_app.bat
echo.
echo Если не запускается, попробуйте:
echo    run_app_alt.bat
echo.
echo Или выполните в командной строке:
echo    python -m streamlit run app.py
echo ============================================
echo.
pause