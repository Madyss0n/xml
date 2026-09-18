-- ============================================================
-- ЗАПРОС ДЛЯ ТАБЕЛЯ (Firebird)
-- Параметры: :start_date, :end_date, :tabel_id (опционально)
-- ============================================================

with gr as (
    select
        reg_events.staff_id,
        reg_events.date_ev,
        min(case reg_events.areas_id 
            when 6613 then time_ev 
            else null 
        end) as time_in,          -- Вход (зона 6613)
        max(case reg_events.areas_id 
            when 1 then time_ev 
            else null 
        end) as time_out          -- Выход (зона 1)
    from reg_events
    where reg_events.date_ev between :start_date and :end_date
    group by
        reg_events.staff_id,
        reg_events.date_ev
    -- order by date_ev desc
),
hours_per_day as (
    select
        gr.staff_id,
        gr.date_ev,
        gr.time_in,
        gr.time_out,
        -- Точный расчет часов (без округления)
        datediff(minute from gr.time_in to gr.time_out) / 60.0 as hours,
        -- Флаг: есть ли полные данные
        case 
            when gr.time_in is not null and gr.time_out is not null 
            then 1 
            else 0 
        end as has_full_data
    from gr
    -- Оставляем все записи, даже с NULL
    -- where gr.time_in is not null and gr.time_out is not null
)
select
    hours_per_day.staff_id,
    staff.last_name,
    staff.first_name,
    staff.middle_name,
    hours_per_day.date_ev,
    hours_per_day.time_in,
    hours_per_day.time_out,
    hours_per_day.hours,
    hours_per_day.has_full_data
from hours_per_day
inner join staff on staff.id_staff = hours_per_day.staff_id
-- Фильтр по табельному номеру (если передан)
where (:tabel_id is null or TRIM(staff.TABEL_ID) = :tabel_id)
order by 
    hours_per_day.staff_id,
    hours_per_day.date_ev desc