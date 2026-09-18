@echo off
chcp 1251 >nul
title УСТАНОВКА ВСЕХ МОДУЛЕЙ

echo ================================================================
echo         УСТАНОВКА ВСЕХ МОДУЛЕЙ
echo ================================================================
echo.

set PYTHON_PATH=C:\Program Files\Python312
set PYTHON_EXE=%PYTHON_PATH%\python.exe

echo Путь к Python: %PYTHON_EXE%
echo.

if not exist "%PYTHON_EXE%" (
    echo ❌ ОШИБКА: Python не найден!
    echo Проверьте путь: %PYTHON_PATH%
    echo.
    pause
    exit /b 1
)

echo [1/8] Обновление pip...
"%PYTHON_EXE%" -m pip install --upgrade pip

echo.
echo [2/8] Установка numpy...
"%PYTHON_EXE%" -m pip install numpy

echo.
echo [3/8] Установка pandas...
"%PYTHON_EXE%" -m pip install pandas

echo.
echo [4/8] Установка openpyxl...
"%PYTHON_EXE%" -m pip install openpyxl

echo.
echo [5/8] Установка streamlit...
"%PYTHON_EXE%" -m pip install streamlit

echo.
echo [6/8] Установка plotly...
"%PYTHON_EXE%" -m pip install plotly

echo.
echo [7/8] Установка xlrd...
"%PYTHON_EXE%" -m pip install xlrd

echo.
echo [8/8] Установка reportlab...
"%PYTHON_EXE%" -m pip install reportlab

echo.
echo Проверка установки...
"%PYTHON_EXE%" -c "import numpy; print('✅ numpy:', numpy.__version__)"
"%PYTHON_EXE%" -c "import pandas; print('✅ pandas:', pandas.__version__)"
"%PYTHON_EXE%" -c "import openpyxl; print('✅ openpyxl:', openpyxl.__version__)"
"%PYTHON_EXE%" -c "import streamlit; print('✅ streamlit:', streamlit.__version__)"
"%PYTHON_EXE%" -c "import plotly; print('✅ plotly:', plotly.__version__)"
"%PYTHON_EXE%" -c "import reportlab; print('✅ reportlab:', reportlab.__version__)"

echo.
echo ================================================================
echo         ВСЕ МОДУЛИ УСТАНОВЛЕНЫ!
echo ================================================================
echo.
echo Для запуска приложения выполните: run_app.bat
pause