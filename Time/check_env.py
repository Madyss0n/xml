# check_env.py - Проверка окружения
import sys
import subprocess
import importlib

print("=" * 50)
print("🔍 Диагностика окружения")
print("=" * 50)
print()

print(f"🐍 Версия Python: {sys.version}")
print(f"📁 Путь Python: {sys.executable}")
print()

# Проверяем установленные пакеты
packages = ['streamlit', 'pandas', 'openpyxl', 'xlrd', 'numpy']
print("📦 Проверка установленных пакетов:")
for pkg in packages:
    try:
        module = importlib.import_module(pkg)
        version = getattr(module, '__version__', 'unknown')
        print(f"   ✅ {pkg}: {version}")
    except ImportError:
        print(f"   ❌ {pkg}: НЕ УСТАНОВЛЕН")

print()
print("=" * 50)
print("🚀 Попытка запуска Streamlit...")
print("=" * 50)

# Пытаемся запустить Streamlit
try:
    import streamlit
    print("✅ Streamlit успешно импортирован")
    print(f"   Версия: {streamlit.__version__}")
    print(f"   Путь: {streamlit.__file__}")
except Exception as e:
    print(f"❌ Ошибка импорта Streamlit: {e}")

print()
print("=" * 50)
print("💡 Для запуска приложения выполните:")
print("   streamlit run app.py")
print("   или")
print("   python -m streamlit run app.py")
print("=" * 50)
input("\nНажмите Enter для выхода...")