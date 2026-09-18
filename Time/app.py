# app.py - ПОЛНАЯ ВЕРСИЯ С ДИЗАЙНОМ В СТИЛЕ МИФИ
import streamlit as st
import sys
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Добавляем папку modules в путь
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

# Настройка страницы
st.set_page_config(
    page_title="Табель учета рабочего времени",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS СТИЛИ В СТИЛЕ МИФИ
# ============================================================

st.markdown("""
<style>
    /* === ОБЩИЕ СТИЛИ === */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #f0f4f8 0%, #ffffff 100%);
    }
    
    /* === ШАПКА В СТИЛЕ МИФИ === */
    .mephi-header {
        background: linear-gradient(135deg, #0a1628 0%, #1a2a4a 50%, #0d47a1 100%);
        padding: 30px 40px 25px 40px;
        border-radius: 16px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(13, 71, 161, 0.25);
        position: relative;
        overflow: hidden;
    }
    
    .mephi-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .mephi-header .logo-row {
        display: flex;
        align-items: center;
        gap: 20px;
        position: relative;
        z-index: 1;
    }
    
    .mephi-header .logo-icon {
        font-size: 3rem;
        background: rgba(255,255,255,0.1);
        padding: 12px 16px;
        border-radius: 14px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.15);
    }
    
    .mephi-header .title-group h1 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .mephi-header .title-group .subtitle {
        color: rgba(255,255,255,0.7);
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 400;
        margin: 4px 0 0 0;
        letter-spacing: 0.3px;
    }
    
    .mephi-header .title-group .subtitle span {
        background: rgba(255,255,255,0.12);
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
    }
    
    .mephi-header .version-badge {
        margin-left: auto;
        background: rgba(255,255,255,0.1);
        padding: 6px 16px;
        border-radius: 20px;
        color: rgba(255,255,255,0.6);
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
    }
    
    /* === СТАТИСТИКА === */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin: 20px 0 30px 0;
    }
    
    .stat-card {
        background: #ffffff;
        padding: 20px 24px;
        border-radius: 14px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e8ecf1;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(13, 71, 161, 0.12);
        border-color: #0d47a1;
    }
    
    .stat-card .number {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: #0d47a1;
        line-height: 1.2;
    }
    
    .stat-card .label {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #8899aa;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }
    
    /* === КАРТОЧКИ МЕНЮ (ГРАДИЕНТНЫЕ КНОПКИ) === */
    .menu-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 24px;
        margin: 30px 0;
    }
    
    .menu-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 40px 32px 32px 32px;
        text-align: center;
        border: 1px solid #e8ecf1;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .menu-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #1a73e8 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
        border-radius: 16px;
    }
    
    .menu-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 16px 48px rgba(13, 71, 161, 0.2);
        border-color: transparent;
    }
    
    .menu-card:hover::before {
        opacity: 1;
    }
    
    .menu-card .icon {
        font-size: 3.6rem;
        margin-bottom: 16px;
        line-height: 1;
        position: relative;
        z-index: 1;
        transition: transform 0.4s ease;
    }
    
    .menu-card:hover .icon {
        transform: scale(1.1);
    }
    
    .menu-card .title {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 8px;
        position: relative;
        z-index: 1;
        transition: color 0.3s ease;
    }
    
    .menu-card:hover .title {
        color: #ffffff;
    }
    
    .menu-card .desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #666;
        line-height: 1.5;
        position: relative;
        z-index: 1;
        transition: color 0.3s ease;
    }
    
    .menu-card:hover .desc {
        color: rgba(255,255,255,0.8);
    }
    
    .menu-card .badge {
        display: inline-block;
        background: #e3f2fd;
        color: #0d47a1;
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        padding: 4px 16px;
        border-radius: 20px;
        letter-spacing: 0.3px;
        margin-top: 12px;
        position: relative;
        z-index: 1;
        transition: all 0.3s ease;
    }
    
    .menu-card:hover .badge {
        background: rgba(255,255,255,0.2);
        color: #ffffff;
    }
    
    .menu-card .badge-new {
        background: #e8f5e9;
        color: #2e7d32;
    }
    
    .menu-card:hover .badge-new {
        background: rgba(255,255,255,0.2);
        color: #ffffff;
    }
    
    /* === ГРАДИЕНТНЫЕ КНОПКИ === */
    .gradient-btn {
        background: linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #1a73e8 100%);
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        padding: 14px 32px;
        border: none;
        border-radius: 12px;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
        box-shadow: 0 4px 16px rgba(13, 71, 161, 0.3);
        width: 100%;
        text-align: center;
        display: inline-block;
        text-decoration: none;
    }
    
    .gradient-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(13, 71, 161, 0.4);
        background: linear-gradient(135deg, #0d47a1 0%, #1a73e8 50%, #42a5f5 100%);
    }
    
    .gradient-btn:active {
        transform: translateY(0px);
        box-shadow: 0 2px 8px rgba(13, 71, 161, 0.3);
    }
    
    /* === ФУТЕР === */
    .mephi-footer {
        text-align: center;
        padding: 30px 0 20px 0;
        border-top: 1px solid #e8ecf1;
        margin-top: 40px;
        font-family: 'Inter', sans-serif;
        color: #8899aa;
        font-size: 0.8rem;
    }
    
    .mephi-footer .footer-logo {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0d47a1;
    }
    
    /* === АДАПТИВНОСТЬ === */
    @media (max-width: 900px) {
        .menu-grid {
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        .mephi-header .title-group h1 {
            font-size: 1.6rem;
        }
        .mephi-header .version-badge {
            display: none;
        }
    }
    
    @media (max-width: 600px) {
        .menu-grid {
            grid-template-columns: 1fr;
            gap: 16px;
        }
        .stats-grid {
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }
        .stat-card .number {
            font-size: 1.5rem;
        }
        .mephi-header {
            padding: 20px;
        }
        .mephi-header .title-group h1 {
            font-size: 1.3rem;
        }
        .mephi-header .logo-icon {
            font-size: 2rem;
            padding: 8px 12px;
        }
        .menu-card {
            padding: 28px 20px;
        }
        .menu-card .icon {
            font-size: 2.8rem;
        }
    }
    
    /* === АНИМАЦИИ === */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.6s ease forwards;
    }
    
    .fade-in-delay-1 { animation-delay: 0.1s; }
    .fade-in-delay-2 { animation-delay: 0.2s; }
    .fade-in-delay-3 { animation-delay: 0.3s; }
    
    /* === СТАТУС ОНЛАЙН === */
    .status-online {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: #4caf50;
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        font-weight: 500;
        background: rgba(76, 175, 80, 0.1);
        padding: 4px 14px;
        border-radius: 20px;
    }
    
    .status-online::before {
        content: '';
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #4caf50;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.8); }
    }
    
    /* === САЙДБАР === */
    .sidebar-brand {
        text-align: center;
        padding: 20px 0 16px 0;
        border-bottom: 1px solid #e8ecf1;
        margin-bottom: 16px;
    }
    
    .sidebar-brand .icon {
        font-size: 2.2rem;
    }
    
    .sidebar-brand .name {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #0d47a1;
        margin-top: 4px;
    }
    
    .sidebar-brand .version {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        color: #8899aa;
    }
    
    /* === EXPANDER === */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #1a1a2e;
    }
    
    /* === МЕТРИКИ === */
    .stMetric {
        background: #ffffff;
        padding: 12px 16px;
        border-radius: 12px;
        border: 1px solid #e8ecf1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .stMetric .stMetricValue {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #0d47a1;
    }
    
    /* === DATAFRAME === */
    .stDataFrame {
        border-radius: 12px;
        border: 1px solid #e8ecf1;
        overflow: hidden;
    }
    
    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8f9fb;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        padding: 8px 20px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #0d47a1 0%, #1565c0 100%);
        color: #ffffff !important;
        box-shadow: 0 2px 12px rgba(13, 71, 161, 0.3);
    }
    
    /* === BUTTONS === */
    .stButton button {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #1a73e8 100%);
        color: #ffffff;
        border: none;
        box-shadow: 0 4px 16px rgba(13, 71, 161, 0.3);
    }
    
    .stButton button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(13, 71, 161, 0.4);
    }
    
    /* === FILE UPLOADER === */
    .stFileUploader {
        border: 2px dashed #d0d4db;
        border-radius: 12px;
        padding: 20px;
        background: #fafbfc;
        transition: border-color 0.3s;
    }
    
    .stFileUploader:hover {
        border-color: #0d47a1;
    }
    
    /* === EXPANDER === */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #1a1a2e;
        background: #f8f9fb;
        border-radius: 10px;
        padding: 8px 16px;
    }
    
    /* === INFO, SUCCESS, WARNING, ERROR === */
    .stAlert {
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        border-left: 4px solid;
    }
    
    .stAlert .stAlertIcon {
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# ИНИЦИАЛИЗАЦИЯ
# ============================================================

if 'page' not in st.session_state:
    st.session_state.page = 'main'

if 'org_name' not in st.session_state:
    st.session_state.org_name = ''
if 'org_okpo' not in st.session_state:
    st.session_state.org_okpo = ''
if 'org_department' not in st.session_state:
    st.session_state.org_department = ''

def go_to_mifi():
    st.session_state.page = 'mifi'
    st.rerun()

def go_to_hostel():
    st.session_state.page = 'hostel'
    st.rerun()

def go_to_main():
    st.session_state.page = 'main'
    st.rerun()

# ============================================================
# ШАПКА В СТИЛЕ МИФИ
# ============================================================

st.markdown("""
<div class="mephi-header fade-in">
    <div class="logo-row">
        <div class="logo-icon">🏛️</div>
        <div class="title-group">
            <h1>Табель учета рабочего времени</h1>
            <div class="subtitle">
                Технологический институт НИЯУ МИФИ
                <span>ТИ НИЯУ МИФИ</span>
            </div>
        </div>
        <div class="version-badge">
            <span class="status-online">Система работает</span>
            <span style="margin-left: 12px; opacity: 0.5;">v6.0</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# БОКОВАЯ ПАНЕЛЬ
# ============================================================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="icon">📊</div>
        <div class="name">Табель учета</div>
        <div class="version">v6.0 · ТИ НИЯУ МИФИ</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🏢 Реквизиты организации", expanded=False):
        st.markdown("**Для заполнения табеля Т-13**")
        org_name = st.text_input("Наименование организации", value=st.session_state.org_name, key="org_name_input")
        org_okpo = st.text_input("Код по ОКПО", value=st.session_state.org_okpo, key="org_okpo_input")
        org_department = st.text_input("Структурное подразделение", value=st.session_state.org_department, key="org_department_input")
        
        if st.button("💾 Сохранить", use_container_width=True):
            st.session_state.org_name = org_name
            st.session_state.org_okpo = org_okpo
            st.session_state.org_department = org_department
            st.success("✅ Реквизиты сохранены!")
    
    if st.session_state.page != 'main':
        if st.button("🏠 На главную", use_container_width=True, key="nav_main"):
            go_to_main()
    
    st.markdown("---")
    st.markdown("""
    <div style="padding: 8px 0; font-family: 'Inter', sans-serif; color: #8899aa; font-size: 0.75rem;">
        <div style="font-weight: 600; color: #555; margin-bottom: 4px;">О системе</div>
        <div>Версия 6.0</div>
        <div>Стиль МИФИ</div>
        <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #f0f0f0;">
            © 2026 ТИ НИЯУ МИФИ
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# ГЛАВНАЯ СТРАНИЦА
# ============================================================

if st.session_state.page == 'main':
    # Статистика
    st.markdown("""
    <div class="stats-grid fade-in">
        <div class="stat-card">
            <div class="number">3</div>
            <div class="label">Инструмента</div>
        </div>
        <div class="stat-card">
            <div class="number">📋</div>
            <div class="label">Excel импорт</div>
        </div>
        <div class="stat-card">
            <div class="number">📄</div>
            <div class="label">PDF отчеты</div>
        </div>
        <div class="stat-card">
            <div class="number">🔄</div>
            <div class="label">Преобразование</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Карточки меню
    st.markdown('<div class="menu-grid">', unsafe_allow_html=True)
    
    # Карточка 1: МИФИ
    st.markdown("""
    <div class="menu-card fade-in fade-in-delay-1">
        <div class="icon">🏛️</div>
        <div class="title">МИФИ</div>
        <div class="desc">Технологический институт<br>НИЯУ МИФИ</div>
        <span class="badge">Основное приложение</span>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🏛️ Перейти в МИФИ", use_container_width=True, key="btn_mifi"):
        go_to_mifi()
    
    # Карточка 2: Общежитие АТОМ
    st.markdown("""
    <div class="menu-card fade-in fade-in-delay-2">
        <div class="icon">🏠</div>
        <div class="title">Общежитие АТОМ</div>
        <div class="desc">Студенческое общежитие<br>с отдельным форматом учета</div>
        <span class="badge badge-new">Новое приложение</span>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🏠 Перейти в Общежитие АТОМ", use_container_width=True, key="btn_hostel"):
        go_to_hostel()
    
    # Карточка 3: Преобразование
    st.markdown("""
    <div class="menu-card fade-in fade-in-delay-3">
        <div class="icon">🔄</div>
        <div class="title">Преобразование табеля</div>
        <div class="desc">Привести файл из Firebird к формату<br>с правильным ФИО</div>
        <span class="badge badge-new">Утилита</span>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 Преобразовать табель", use_container_width=True, key="btn_convert"):
        go_to_mifi()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Информационный баннер
    st.markdown("""
    <div style="background: #f0f8ff; border-radius: 14px; padding: 20px 28px; border-left: 4px solid #0d47a1; margin: 24px 0;">
        <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap;">
            <div style="font-size: 1.5rem;">💡</div>
            <div style="flex: 1; font-family: 'Inter', sans-serif; color: #333; font-size: 0.95rem;">
                <strong>Быстрый старт:</strong> Загрузите Excel файл с табелем и получите 
                автоматический расчет отработанных часов, графики и готовые отчеты в формате Т-13.
                <br><br>
                <strong>🔄 Преобразование табеля:</strong> Если у вас есть файлы из Firebird с разбитыми данными,
                используйте утилиту для приведения к правильному формату.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Футер
    st.markdown("""
    <div class="mephi-footer">
        <div class="footer-logo">🏛️ ТИ НИЯУ МИФИ</div>
        <div style="margin-top: 4px;">Табель учета рабочего времени · v6.0</div>
        <div style="margin-top: 2px; font-size: 0.7rem;">© 2026 Технологический институт НИЯУ МИФИ</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# МОДУЛИ
# ============================================================

elif st.session_state.page == 'mifi':
    try:
        from modules import mifi
        mifi.main()
    except ImportError as e:
        st.error(f"❌ Ошибка загрузки модуля МИФИ: {e}")
        if st.button("🏠 Вернуться на главную"):
            go_to_main()
    except Exception as e:
        st.error(f"❌ Ошибка выполнения модуля МИФИ: {e}")
        if st.button("🏠 Вернуться на главную"):
            go_to_main()

elif st.session_state.page == 'hostel':
    try:
        from modules import hostel
        hostel.main()
    except ImportError as e:
        st.error(f"❌ Ошибка загрузки модуля Общежитие АТОМ: {e}")
        if st.button("🏠 Вернуться на главную"):
            go_to_main()
    except Exception as e:
        st.error(f"❌ Ошибка выполнения модуля Общежитие АТОМ: {e}")
        if st.button("🏠 Вернуться на главную"):
            go_to_main()