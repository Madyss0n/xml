# setup.py - Установочный скрипт
import os
import sys
import subprocess
import platform

def install_requirements():
    """Установка зависимостей"""
    print("📦 Установка зависимостей...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Зависимости установлены!")

def create_shortcut():
    """Создание ярлыка для запуска (только Windows)"""
    if platform.system() == "Windows":
        try:
            # Создаем .bat файл для запуска
            with open("run_app.bat", "w", encoding="utf-8") as f:
                f.write("""@echo off
echo 🚀 Запуск приложения Табель учета...
echo.
streamlit run app.py --server.port 8501 --server.address localhost
pause
""")
            print("✅ Создан файл run_app.bat для запуска")
        except Exception as e:
            print(f"⚠️ Не удалось создать ярлык: {e}")

def main():
    print("=" * 50)
    print("📊 Установка приложения Табель учета")
    print("=" * 50)
    print()
    
    # Проверка Python
    print(f"🐍 Python версия: {sys.version}")
    print()
    
    # Установка зависимостей
    install_requirements()
    print()
    
    # Создание ярлыка
    create_shortcut()
    print()
    
    print("=" * 50)
    print("✅ Установка завершена!")
    print()
    print("🚀 Для запуска приложения выполните:")
    print("   streamlit run app.py")
    print()
    print("   Или запустите файл run_app.bat (Windows)")
    print("=" * 50)

if __name__ == "__main__":
    main()