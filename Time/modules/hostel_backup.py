# modules/hostel.py - ПОЛНАЯ ВЕРСИЯ С ДИЗАЙНОМ
import os
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import io
import warnings
import re
import tempfile
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
warnings.filterwarnings('ignore')

# ============================================================
# CSS СТИЛИ ДЛЯ МОДУЛЯ ОБЩЕЖИТИЕ
# ============================================================

st.markdown("""
<style>
    .hostel-header {
        background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #0d47a1 100%);
        padding: 24px 32px;
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(13, 71, 161, 0.2);
    }
    .hostel-header h1 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .hostel-header p {
        color: rgba(255,255,255,0.7);
        font-family: 'Inter', sans-serif;
        margin: 4px 0 0 0;
        font-size: 0.95rem;
    }
    .hostel-header .badge-hostel {
        background: rgba(255,255,255,0.12);
        padding: 2px 14px;
        border-radius: 20px;
        font-size: 0.7rem;
        color: rgba(255,255,255,0.6);
        border: 1px solid rgba(255,255,255,0.08);
    }
    .gradient-btn-hostel {
        background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #0d47a1 100%);
        color: #ffffff !important;
        font-weight: 600;
        padding: 12px 28px;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 16px rgba(26, 35, 126, 0.3);
        transition: all 0.3s ease;
        width: 100%;
        text-align: center;
        cursor: pointer;
    }
    .gradient-btn-hostel:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(26, 35, 126, 0.4);
        background: linear-gradient(135deg, #1a237e 0%, #0d47a1 50%, #1565c0 100%);
    }
    .hostel-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 20px 24px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e8ecf1;
        margin: 12px 0;
    }
    .hostel-gradient-section {
        background: linear-gradient(135deg, #e8eaf6 0%, #f0f8ff 100%);
        padding: 16px 20px;
        border-radius: 12px;
        border-left: 4px solid #1a237e;
        margin: 16px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# РЕГИСТРАЦИЯ ШРИФТОВ ДЛЯ PDF
# ============================================================

def register_fonts():
    """Регистрация шрифтов для поддержки кириллицы в PDF"""
    try:
        font_paths = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/ariali.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/arialbi.ttf",
            "C:/Windows/Fonts/times.ttf",
            "C:/Windows/Fonts/timesi.ttf",
            "C:/Windows/Fonts/timesbd.ttf",
            "C:/Windows/Fonts/timesbi.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            "C:/Windows/Fonts/calibrii.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
            "C:/Windows/Fonts/calibriz.ttf",
            "C:/Windows/Fonts/verdana.ttf",
            "C:/Windows/Fonts/verdanai.ttf",
            "C:/Windows/Fonts/verdanab.ttf",
            "C:/Windows/Fonts/verdanaz.ttf",
        ]
        
        registered = False
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('RussianFont', font_path))
                    registered = True
                    break
                except:
                    continue
        
        if not registered:
            fonts_dir = "C:/Windows/Fonts"
            if os.path.exists(fonts_dir):
                for file in os.listdir(fonts_dir):
                    if file.endswith('.ttf') and not file.startswith('.'):
                        try:
                            font_path = os.path.join(fonts_dir, file)
                            pdfmetrics.registerFont(TTFont('RussianFont', font_path))
                            registered = True
                            break
                        except:
                            continue
        
        return registered
    except:
        return False

FONT_REGISTERED = register_fonts()

def get_pdf_font_name():
    if FONT_REGISTERED and 'RussianFont' in pdfmetrics.getRegisteredFontNames():
        return 'RussianFont'
    return 'Helvetica'

# ============================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ СО ВРЕМЕНЕМ
# ============================================================

def safe_format_time(val):
    """Безопасное форматирование времени"""
    if val is None or pd.isna(val):
        return ''
    if isinstance(val, pd.Timestamp):
        if pd.isna(val):
            return ''
        return val.strftime('%H:%M:%S')
    if isinstance(val, datetime):
        return val.strftime('%H:%M:%S')
    if isinstance(val, timedelta):
        return str(val)
    if isinstance(val, str):
        return val
    return str(val)

def time_to_minutes(time_val):
    """Преобразование времени в минуты"""
    if time_val is None or pd.isna(time_val):
        return 0
    
    if isinstance(time_val, pd.Timestamp):
        return time_val.hour * 60 + time_val.minute
    
    if isinstance(time_val, datetime):
        return time_val.hour * 60 + time_val.minute
    
    if isinstance(time_val, timedelta):
        return time_val.total_seconds() / 60
    
    if isinstance(time_val, str):
        time_val = time_val.strip()
        if ':' in time_val:
            parts = time_val.split(':')
            if len(parts) >= 2:
                try:
                    h = int(parts[0])
                    m = int(parts[1])
                    s = int(parts[2]) if len(parts) > 2 else 0
                    return h * 60 + m + s / 60
                except:
                    pass
        # Пробуем распарсить как timedelta
        try:
            if 'day' in time_val.lower():
                match = re.search(r'(\d+)\s+days?,\s+(\d{1,2}):(\d{2}):(\d{2})', time_val.lower())
                if match:
                    days = int(match.group(1))
                    h = int(match.group(2))
                    m = int(match.group(3))
                    s = int(match.group(4))
                    return days * 24 * 60 + h * 60 + m + s / 60
            else:
                match = re.search(r'(\d{1,2}):(\d{2}):(\d{2})', time_val)
                if match:
                    h = int(match.group(1))
                    m = int(match.group(2))
                    s = int(match.group(3))
                    return h * 60 + m + s / 60
                match = re.search(r'(\d{1,2}):(\d{2})', time_val)
                if match:
                    h = int(match.group(1))
                    m = int(match.group(2))
                    return h * 60 + m
        except:
            pass
    
    return 0

def minutes_to_time_str(minutes):
    """Преобразование минут в строку ЧЧ:ММ"""
    if minutes < 0:
        minutes = 0
    h = int(minutes // 60)
    m = int(minutes % 60)
    return f"{h}:{m:02d}"

def format_hours(hours):
    """Форматирование часов в ЧЧ:ММ"""
    if hours == 0:
        return "0:00"
    total_minutes = int(round(hours * 60))
    h = total_minutes // 60
    m = total_minutes % 60
    return f"{h}:{m:02d}"

def parse_datetime_from_value(value):
    """Парсит время из значения (может быть строка с датой или просто время)"""
    if value is None or pd.isna(value):
        return None
    
    if isinstance(value, (datetime, pd.Timestamp)):
        return value
    
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        
        match = re.match(r'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})', value)
        if match:
            try:
                return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except:
                pass
        
        match = re.match(r'(\d{1,2}):(\d{2})(?::(\d{2}))?', value)
        if match:
            h = int(match.group(1))
            m = int(match.group(2))
            s = int(match.group(3)) if match.group(3) else 0
            return datetime(2000, 1, 1, h, m, s)
    
    return None

def calculate_time_diff(in_val, out_val):
    """Расчет разницы между временем входа и выхода"""
    if in_val is None or out_val is None:
        return 0
    
    in_min = time_to_minutes(in_val)
    out_min = time_to_minutes(out_val)
    
    diff = out_min - in_min
    if diff < 0:
        diff += 24 * 60
    
    return diff

# ============================================================
# ПАРСИНГ ГОРИЗОНТАЛЬНОГО ФАЙЛА
# ============================================================

def convert_horizontal_to_vertical(uploaded_file):
    """
    Преобразование горизонтального формата в вертикальный
    """
    debug_info = []
    
    try:
        df_raw = pd.read_excel(uploaded_file, header=None)
        df_raw = df_raw.dropna(how='all')
        
        debug_info.append(f"📄 Файл прочитан, строк: {len(df_raw)}")
        
        if df_raw.empty:
            debug_info.append("❌ Файл пуст!")
            return None, None, None, debug_info
        
        header_row_idx = 2
        if header_row_idx >= len(df_raw):
            debug_info.append("❌ Строка с заголовком не найдена!")
            return None, None, None, debug_info
        
        debug_info.append(f"🔍 Заголовок на строке: {header_row_idx}")
        header_row = df_raw.iloc[header_row_idx]
        
        employee_col = 1
        debug_info.append(f"🔍 Колонка с сотрудниками: {employee_col}")
        
        date_columns = []
        debug_info.append("🔍 Поиск колонок с датами...")
        
        for col_idx, val in enumerate(header_row):
            if val is None or pd.isna(val):
                continue
            val_str = str(val).strip()
            
            if '[Вход]' in val_str or '[Выход]' in val_str or '[Присутствие]' in val_str:
                date_match = re.search(r'(\d{2}\.\d{2}\.\d{4})', val_str)
                date_str = date_match.group(1) if date_match else None
                
                col_type = 'unknown'
                if '[Вход]' in val_str:
                    col_type = 'in'
                elif '[Выход]' in val_str:
                    col_type = 'out'
                elif '[Присутствие]' in val_str:
                    col_type = 'presence'
                
                if date_str:
                    existing = None
                    for i, (in_col, out_col, presence_col, dt, header) in enumerate(date_columns):
                        if dt == date_str:
                            existing = i
                            break
                    
                    if existing is not None:
                        in_col, out_col, presence_col, dt, header = date_columns[existing]
                        if col_type == 'in':
                            date_columns[existing] = (col_idx, out_col, presence_col, dt, val_str)
                        elif col_type == 'out':
                            date_columns[existing] = (in_col, col_idx, presence_col, dt, val_str)
                        elif col_type == 'presence':
                            date_columns[existing] = (in_col, out_col, col_idx, dt, val_str)
                    else:
                        if col_type == 'in':
                            date_columns.append((col_idx, None, None, date_str, val_str))
                        elif col_type == 'out':
                            date_columns.append((None, col_idx, None, date_str, val_str))
                        elif col_type == 'presence':
                            date_columns.append((None, None, col_idx, date_str, val_str))
        
        date_columns.sort(key=lambda x: x[3] if x[3] else '')
        debug_info.append(f"🔍 Найдено колонок с датами: {len(date_columns)}")
        
        if not date_columns:
            debug_info.append("❌ Не найдены колонки с датами!")
            return None, None, None, debug_info
        
        employees = []
        for idx in range(header_row_idx + 1, len(df_raw)):
            row = df_raw.iloc[idx]
            if row.isna().all():
                continue
            
            if employee_col < len(row):
                employee = row.iloc[employee_col]
                if employee is None or pd.isna(employee):
                    continue
                
                employee = str(employee).strip()
                if employee == 'nan' or employee == '':
                    continue
                
                if 'Итого' in employee or 'Всего' in employee or 'итого' in employee.lower():
                    continue
                
                employees.append(employee)
        
        debug_info.append(f"👥 Найдено сотрудников: {len(employees)}")
        
        result_data = []
        days_processed = 0
        
        for in_col, out_col, presence_col, date_str, header_name in date_columns:
            days_processed += 1
            
            if result_data:
                result_data.append(['', '', '', ''])
            
            day_name = ''
            if '[' in header_name:
                day_part = header_name.split('[')[0].strip()
                day_name = day_part
            else:
                day_name = header_name
            
            result_data.append([
                'Сотрудник', 
                f"{date_str} {day_name}[Вход]" if date_str else f"{day_name}[Вход]",
                f"{date_str} {day_name}[Выход]" if date_str else f"{day_name}[Выход]",
                f"{date_str} {day_name}[Присутствие]" if date_str else f"{day_name}[Присутствие]"
            ])
            
            for employee in employees:
                emp_row = None
                for idx in range(header_row_idx + 1, len(df_raw)):
                    row = df_raw.iloc[idx]
                    if row.isna().all():
                        continue
                    if employee_col < len(row):
                        emp_val = row.iloc[employee_col]
                        if emp_val is None or pd.isna(emp_val):
                            continue
                        if str(emp_val).strip() == employee:
                            emp_row = row
                            break
                
                if emp_row is None:
                    continue
                
                in_val = ''
                out_val = ''
                presence_val = ''
                
                if in_col is not None and in_col < len(emp_row):
                    val = emp_row.iloc[in_col]
                    if val is not None and not pd.isna(val) and str(val).strip() not in ['', 'nan']:
                        in_val = str(val).strip()
                
                if out_col is not None and out_col < len(emp_row):
                    val = emp_row.iloc[out_col]
                    if val is not None and not pd.isna(val) and str(val).strip() not in ['', 'nan']:
                        out_val = str(val).strip()
                
                if presence_col is not None and presence_col < len(emp_row):
                    val = emp_row.iloc[presence_col]
                    if val is not None and not pd.isna(val) and str(val).strip() not in ['', 'nan']:
                        presence_val = str(val).strip()
                
                result_data.append([employee, in_val, out_val, presence_val])
        
        debug_info.append(f"📅 Обработано дней: {days_processed}")
        
        blocks = []
        current_block = None
        
        for row in result_data:
            if len(row) >= 4 and row[0] == 'Сотрудник':
                if current_block is not None:
                    blocks.append(current_block)
                current_block = {
                    'header': row,
                    'data': []
                }
            elif current_block is not None and row[0] and row[0] != '':
                current_block['data'].append(row)
        
        if current_block is not None:
            blocks.append(current_block)
        
        debug_info.append(f"📦 Создано блоков: {len(blocks)}")
        
        flat_data = []
        for block in blocks:
            day_date = ''
            for col in block['header']:
                if '[' in str(col):
                    match = re.search(r'(\d{2}\.\d{2}\.\d{4})', str(col))
                    if match:
                        day_date = match.group(1)
                        break
            
            for row in block['data']:
                if len(row) >= 4:
                    in_time = row[1] if len(row) > 1 else ''
                    out_time = row[2] if len(row) > 2 else ''
                    hours = calculate_time_diff(in_time, out_time)
                    
                    flat_data.append({
                        'Дата': day_date,
                        'Сотрудник': row[0],
                        'Вход': row[1],
                        'Выход': row[2],
                        'Присутствие': row[3],
                        'Часы (float)': hours,
                        'Часы (ЧЧ:ММ)': format_hours(hours)
                    })
        
        df_vertical = pd.DataFrame(flat_data)
        
        if not df_vertical.empty:
            df_vertical = df_vertical.sort_values(['Дата', 'Сотрудник']).reset_index(drop=True)
        
        debug_info.append(f"📋 Сформировано записей: {len(df_vertical)}")
        
        df_summary = df_vertical.groupby('Сотрудник').agg({
            'Часы (float)': 'sum',
            'Дата': 'count'
        }).reset_index()
        df_summary.columns = ['Сотрудник', 'Всего часов (float)', 'Кол-во дней']
        df_summary['Всего часов'] = df_summary['Всего часов (float)'].apply(format_hours_to_time)
        df_summary = df_summary.sort_values('Всего часов (float)', ascending=False).reset_index(drop=True)
        
        debug_info.append(f"✅ Сводка: {len(df_summary)} сотрудников")
        
        return df_vertical, df_summary, blocks, debug_info
        
    except Exception as e:
        debug_info.append(f"❌ Ошибка: {str(e)}")
        import traceback
        debug_info.append(traceback.format_exc())
        return None, None, None, debug_info

def format_hours_to_time(hours):
    """Преобразование часов в формат ЧЧ:ММ"""
    if hours is None or hours == 0:
        return "00:00"
    total_minutes = int(round(hours * 60))
    h = total_minutes // 60
    m = total_minutes % 60
    return f"{h:02d}:{m:02d}"

def export_to_excel_formatted(df_vertical, df_summary, blocks_info):
    """Экспорт в Excel с сохранением форматирования"""
    
    output = io.BytesIO()
    wb = Workbook()
    wb.remove(wb.active)
    
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    border = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )
    center_alignment = Alignment(horizontal='center', vertical='center')
    
    # Лист "В день"
    ws_day = wb.create_sheet("В день")
    current_row = 1
    
    for block_idx, block in enumerate(blocks_info):
        if block_idx > 0:
            current_row += 1
        
        header = block['header']
        for col_idx, value in enumerate(header):
            cell = ws_day.cell(row=current_row, column=col_idx + 1, value=value)
            cell.fill = header_fill
            cell.font = header_font
            cell.border = border
            cell.alignment = center_alignment
        
        current_row += 1
        
        for row_data in block['data']:
            for col_idx, value in enumerate(row_data):
                cell = ws_day.cell(row=current_row, column=col_idx + 1, value=value)
                cell.border = border
                cell.alignment = center_alignment
            current_row += 1
    
    # Лист "Сводка"
    ws_summary = wb.create_sheet("Сводка")
    headers = ['№', 'Сотрудник', 'Всего часов', 'Кол-во дней']
    for col_idx, header in enumerate(headers):
        cell = ws_summary.cell(row=1, column=col_idx + 1, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
        cell.alignment = center_alignment
    
    for row_idx, row in df_summary.iterrows():
        row_num = row_idx + 2
        ws_summary.cell(row=row_num, column=1, value=row_idx + 1).border = border
        ws_summary.cell(row=row_num, column=1).alignment = center_alignment
        ws_summary.cell(row=row_num, column=2, value=row.get('Сотрудник', '')).border = border
        ws_summary.cell(row=row_num, column=2).alignment = center_alignment
        ws_summary.cell(row=row_num, column=3, value=row.get('Всего часов', '00:00')).border = border
        ws_summary.cell(row=row_num, column=3).alignment = center_alignment
        ws_summary.cell(row=row_num, column=4, value=row.get('Кол-во дней', 0)).border = border
        ws_summary.cell(row=row_num, column=4).alignment = center_alignment
    
    wb.save(output)
    output.seek(0)
    return output.getvalue()

def export_to_pdf(df, title="Отчет по табелю (Общежитие АТОМ)", selected_cols=None):
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), 
                                rightMargin=20, leftMargin=20, 
                                topMargin=20, bottomMargin=20)
        
        font_name = get_pdf_font_name()
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontName=font_name,
            fontSize=16,
            alignment=1,
            spaceAfter=20
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=9
        )
        
        story = []
        story.append(Paragraph(f"<b>{title}</b>", title_style))
        story.append(Paragraph(f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}", normal_style))
        story.append(Spacer(1, 15))
        
        if selected_cols is None:
            display_cols = ['Дата', 'Сотрудник', 'Вход', 'Выход', 'Часы (ЧЧ:ММ)']
        else:
            display_cols = selected_cols
        
        available_cols = [col for col in display_cols if col in df.columns]
        if not available_cols:
            available_cols = ['Дата', 'Сотрудник', 'Вход', 'Выход', 'Часы (ЧЧ:ММ)']
        
        df_display = df.head(1000)
        table_data = [available_cols]
        for _, row in df_display.iterrows():
            row_data = []
            for col in available_cols:
                val = str(row.get(col, ''))
                if len(val) > 50:
                    val = val[:47] + '...'
                row_data.append(val)
            table_data.append(row_data)
        
        col_widths = []
        for col in available_cols:
            if col in ['Сотрудник']:
                col_widths.append(2.5 * inch)
            elif col in ['Дата', 'Вход', 'Выход', 'Часы (ЧЧ:ММ)']:
                col_widths.append(1.2 * inch)
            else:
                col_widths.append(1.5 * inch)
        
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E6EEF8')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
            ('TOPPADDING', (0, 1), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Всего записей: {len(df_display)}", normal_style))
        if len(df) > 1000:
            story.append(Paragraph(f"<i>Показаны первые 1000 записей из {len(df)}</i>", normal_style))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        st.error(f"Ошибка при создании PDF: {str(e)}")
        return None

def export_summary_to_pdf(df_summary, title="Сводка по сотрудникам (Общежитие АТОМ)", selected_cols=None):
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), 
                                rightMargin=30, leftMargin=30, 
                                topMargin=30, bottomMargin=30)
        
        font_name = get_pdf_font_name()
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontName=font_name,
            fontSize=16,
            alignment=1,
            spaceAfter=20
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=10
        )
        
        story = []
        story.append(Paragraph(f"<b>{title}</b>", title_style))
        story.append(Paragraph(f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}", normal_style))
        story.append(Spacer(1, 15))
        
        if selected_cols is None:
            display_cols = ['№', 'Сотрудник', 'Всего часов', 'Кол-во дней']
        else:
            display_cols = selected_cols
        
        available_cols = []
        for col in display_cols:
            if col == '№':
                available_cols.append(col)
            elif col in df_summary.columns:
                available_cols.append(col)
        
        if not available_cols or available_cols == ['№']:
            available_cols = ['№', 'Сотрудник', 'Всего часов', 'Кол-во дней']
        
        table_data = [available_cols]
        for idx, row in df_summary.iterrows():
            row_data = []
            for col in available_cols:
                if col == '№':
                    row_data.append(str(idx + 1))
                else:
                    val = str(row.get(col, ''))
                    if len(val) > 40:
                        val = val[:37] + '...'
                    row_data.append(val)
            table_data.append(row_data)
        
        col_widths = []
        for col in available_cols:
            if col in ['Сотрудник']:
                col_widths.append(3.5 * inch)
            elif col in ['Всего часов', 'Кол-во дней']:
                col_widths.append(1.2 * inch)
            elif col == '№':
                col_widths.append(0.5 * inch)
            else:
                col_widths.append(1.0 * inch)
        
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E6EEF8')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
            ('TOPPADDING', (0, 1), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Всего сотрудников: {len(df_summary)}", normal_style))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        st.error(f"Ошибка при создании PDF: {str(e)}")
        return None

# ============================================================
# КОМПОНЕНТ ДЛЯ УПРАВЛЕНИЯ КОЛОНКАМИ
# ============================================================

def render_column_controls(df, prefix="hostel_col_"):
    """Рендерит галочки над столбцами и меню восстановления"""
    
    exclude_cols = ['Часы (float)']
    all_cols = [col for col in df.columns if col not in exclude_cols]
    
    if 'hostel_hidden_cols' not in st.session_state:
        st.session_state.hostel_hidden_cols = []
    
    st.markdown("---")
    st.markdown("#### 📋 Управление столбцами")
    st.markdown("Снимите галочку, чтобы скрыть столбец")
    
    cols_per_row = 5
    rows = [all_cols[i:i+cols_per_row] for i in range(0, len(all_cols), cols_per_row)]
    
    counter = 0
    
    for row_cols in rows:
        cols = st.columns(cols_per_row)
        for idx, col_name in enumerate(row_cols):
            if idx < len(cols):
                is_checked = col_name not in st.session_state.hostel_hidden_cols
                checked = cols[idx].checkbox(
                    col_name, 
                    value=is_checked,
                    key=f"{prefix}{counter}_{col_name}",
                    help=f"Показать/скрыть столбец '{col_name}'"
                )
                if checked and col_name in st.session_state.hostel_hidden_cols:
                    st.session_state.hostel_hidden_cols.remove(col_name)
                elif not checked and col_name not in st.session_state.hostel_hidden_cols:
                    st.session_state.hostel_hidden_cols.append(col_name)
                counter += 1
    
    if st.session_state.hostel_hidden_cols:
        st.markdown("---")
        st.markdown("#### 🔄 Скрытые столбцы")
        st.markdown(f"Скрыто: **{len(st.session_state.hostel_hidden_cols)}** столбцов")
        
        hidden_cols = st.session_state.hostel_hidden_cols.copy()
        for hidden_col in hidden_cols:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"📌 `{hidden_col}`")
            with col2:
                if st.button(f"Вернуть", key=f"hostel_restore_{hidden_col}"):
                    if hidden_col in st.session_state.hostel_hidden_cols:
                        st.session_state.hostel_hidden_cols.remove(hidden_col)
                        st.rerun()
            with col3:
                if st.button(f"🔄", key=f"hostel_restore_icon_{hidden_col}", help="Вернуть столбец"):
                    if hidden_col in st.session_state.hostel_hidden_cols:
                        st.session_state.hostel_hidden_cols.remove(hidden_col)
                        st.rerun()
        
        if st.button("🔄 Вернуть все скрытые столбцы", use_container_width=True, key="hostel_restore_all"):
            st.session_state.hostel_hidden_cols = []
            st.rerun()
    
    visible_cols = [col for col in all_cols if col not in st.session_state.hostel_hidden_cols]
    return visible_cols

# ============================================================
# ОСНОВНАЯ ФУНКЦИЯ
# ============================================================

def main():
    """Главная функция модуля Общежитие АТОМ"""
    
    st.markdown("""
    <div class="hostel-header">
        <h1>
            🏠 Общежитие АТОМ
            <span class="badge-hostel">Студенческое общежитие</span>
        </h1>
        <p>Учет рабочего времени в студенческом общежитии ТИ НИЯУ МИФИ</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📖 Инструкция по формату файла", expanded=True):
        st.markdown("""
        <div class="hostel-gradient-section">
        <b>📋 Поддерживаемый формат файла:</b><br>
        <br>
        <b>Горизонтальный формат:</b><br>
        - Строка с заголовками: "Таб. № | Сотрудник | ... | ДД.ММ.ГГГГ День[Вход] | ... | Всего"<br>
        - Для каждого дня есть три колонки: [Вход], [Выход], [Присутствие]<br>
        - Данные: Сотрудник | ... | время входа | время выхода | время присутствия<br>
        <br>
        <b>Результат преобразования:</b><br>
        - Данные преобразуются из горизонтального формата в вертикальный<br>
        - Каждая запись содержит: Сотрудник, Дата, Вход, Выход, Присутствие, Часы<br>
        - Автоматический расчет часов за день и за месяц<br>
        - Все данные сохраняются в оригинальном виде (без изменений)
        </div>
        """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "📂 Выберите Excel файл (Общежитие АТОМ)",
        type=['xlsx', 'xls'],
        key="hostel_uploader"
    )
    
    if uploaded_file is not None:
        with st.spinner('⏳ Преобразование файла...'):
            df_vertical, df_summary, blocks_info, debug_info = convert_horizontal_to_vertical(uploaded_file)
        
        if df_vertical is None or df_summary is None:
            with st.expander("🔍 Отладочная информация"):
                for line in debug_info:
                    st.text(line)
            return
        
        with st.expander("🔍 Отладочная информация"):
            for line in debug_info:
                st.text(line)
        
        st.success(f"✅ Данные преобразованы! Всего записей: {len(df_vertical)}, сотрудников: {len(df_summary)}")
        
        # ============================================================
        # ВКЛАДКИ
        # ============================================================
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Плоская таблица",
            "📅 По дням",
            "👥 По сотрудникам",
            "📈 Статистика",
            "📥 Экспорт"
        ])
        
        with tab1:
            st.subheader("📋 Все данные в одной таблице")
            
            visible_cols = render_column_controls(df_vertical, prefix="hostel_flat_")
            
            search = st.text_input("🔍 Поиск", key="hostel_flat_search")
            
            if search:
                mask = (
                    df_vertical['Сотрудник'].str.contains(search, case=False, na=False) |
                    df_vertical['Дата'].str.contains(search, case=False, na=False)
                )
                df_filtered = df_vertical[mask]
            else:
                df_filtered = df_vertical
            
            display_cols = [col for col in visible_cols if col in df_filtered.columns]
            if not display_cols:
                display_cols = ['Дата', 'Сотрудник', 'Вход', 'Выход', 'Часы (ЧЧ:ММ)']
            
            st.dataframe(
                df_filtered[display_cols],
                use_container_width=True,
                height=500,
                hide_index=True
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📋 Всего записей", len(df_filtered))
            with col2:
                st.metric("👥 Сотрудников", len(df_filtered['Сотрудник'].unique()))
            with col3:
                total_hours = df_filtered['Часы (float)'].sum()
                st.metric("⏱ Всего часов", format_hours_to_time(total_hours))
        
        with tab2:
            st.subheader("📅 Данные по дням (блоки друг под другом)")
            st.info("Каждый день отображается отдельным блоком в одном листе")
            
            if blocks_info and len(blocks_info) > 0:
                for block_idx, block in enumerate(blocks_info):
                    header = block['header']
                    day_header = " | ".join([str(h) for h in header if str(h).strip()])
                    
                    with st.expander(f"📅 {day_header}", expanded=block_idx < 2):
                        day_data = []
                        for row in block['data']:
                            if len(row) >= 4:
                                in_time = row[1] if len(row) > 1 else ''
                                out_time = row[2] if len(row) > 2 else ''
                                hours = calculate_time_diff(in_time, out_time)
                                
                                day_data.append({
                                    'Сотрудник': row[0],
                                    'Вход': row[1],
                                    'Выход': row[2],
                                    'Присутствие': row[3],
                                    'Часов': format_hours_to_time(hours)
                                })
                        
                        if day_data:
                            day_df = pd.DataFrame(day_data)
                            st.dataframe(day_df, use_container_width=True, hide_index=True)
                            
                            filled = day_df[(day_df['Вход'] != '') | (day_df['Выход'] != '') | (day_df['Присутствие'] != '')]
                            day_hours = day_df['Часов'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])).sum()
                            st.caption(f"Всего: {len(day_df)}, с данными: {len(filled)}, часов за день: {format_hours_to_time(day_hours / 60)}")
            else:
                st.warning("Нет данных")
        
        with tab3:
            st.subheader("👥 Данные по сотруднику")
            
            employees = sorted(df_vertical['Сотрудник'].unique())
            if len(employees) > 0:
                selected = st.selectbox("Выберите сотрудника", employees, key="hostel_employee")
                
                if selected:
                    filtered = df_vertical[df_vertical['Сотрудник'] == selected]
                    
                    display_cols = ['Дата', 'Вход', 'Выход', 'Часы (ЧЧ:ММ)']
                    st.dataframe(
                        filtered[display_cols],
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    total_hours = filtered['Часы (float)'].sum()
                    days = len(filtered)
                    avg = total_hours / days if days > 0 else 0
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📋 Записей", days)
                    with col2:
                        st.metric("📅 Дней", len(filtered['Дата'].unique()))
                    with col3:
                        st.metric("⏱ Всего часов", format_hours_to_time(total_hours))
                    with col4:
                        st.metric("📊 Среднее за день", format_hours_to_time(avg))
            else:
                st.warning("Нет данных")
        
        with tab4:
            st.subheader("📈 Статистика")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Топ-10 по часам")
                top_employees = df_summary.head(10)
                st.dataframe(
                    top_employees[['Сотрудник', 'Всего часов', 'Кол-во дней']],
                    use_container_width=True,
                    hide_index=True
                )
            
            with col2:
                st.markdown("#### Распределение по дням")
                days_count = df_vertical['Дата'].value_counts().reset_index()
                days_count.columns = ['Дата', 'Количество']
                days_count = days_count.sort_values('Дата')
                
                if not days_count.empty:
                    fig = px.bar(
                        days_count,
                        x='Дата',
                        y='Количество',
                        title='Количество записей по дням',
                        height=400
                    )
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Нет данных")
            
            st.markdown("---")
            st.markdown("#### 📊 Распределение сотрудников по часам")
            
            hist_data = df_summary['Всего часов (float)']
            if not hist_data.empty:
                fig_hist = px.histogram(
                    hist_data,
                    nbins=20,
                    title='Распределение сотрудников по часам',
                    labels={'value': 'Часы', 'count': 'Количество сотрудников'},
                    height=400
                )
                st.plotly_chart(fig_hist, use_container_width=True)
        
        with tab5:
            st.subheader("📥 Экспорт")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 📊 Excel с форматированием")
                
                excel_data = export_to_excel_formatted(df_vertical, df_summary, blocks_info)
                
                st.download_button(
                    label="📥 Скачать Excel",
                    data=excel_data,
                    file_name=f"Общежитие_вертикальный_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col2:
                st.markdown("#### 📄 CSV")
                
                csv = df_vertical.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 Скачать CSV",
                    data=csv,
                    file_name=f"Общежитие_вертикальный_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col3:
                st.markdown("#### 📄 PDF")
                
                if st.button("📄 Создать PDF детальный", use_container_width=True):
                    with st.spinner("⏳ Создание PDF..."):
                        pdf_data = export_to_pdf(df_vertical, "Общежитие АТОМ", ['Дата', 'Сотрудник', 'Вход', 'Выход', 'Часы (ЧЧ:ММ)'])
                        if pdf_data:
                            st.download_button(
                                label="📥 Скачать PDF",
                                data=pdf_data,
                                file_name=f"Общежитие_детальный_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                
                if st.button("📄 Создать PDF сводку", use_container_width=True):
                    with st.spinner("⏳ Создание PDF..."):
                        pdf_data = export_summary_to_pdf(df_summary, "Сводка по сотрудникам", ['№', 'Сотрудник', 'Всего часов', 'Кол-во дней'])
                        if pdf_data:
                            st.download_button(
                                label="📥 Скачать сводку PDF",
                                data=pdf_data,
                                file_name=f"Общежитие_сводка_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
            
            st.markdown("---")
            st.info("📄 Все данные сохраняются в оригинальном виде")

if __name__ == "__main__":
    main()