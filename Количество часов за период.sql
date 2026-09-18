with gr as (
        select
        reg_events.staff_id,
        reg_events.date_ev,
        min(case reg_events.areas_id when 6613 then time_ev else null end) as in_,
        max(case reg_events.areas_id when 1 then time_ev else null end) as out_
        from reg_events
        where reg_events.date_ev between '30.09.2019' and '30.10.2019'
        and staff_id is not null
        group by
        reg_events.staff_id,
        reg_events.date_ev
        order by date_ev desc
    ), hours_per_day as(
        select
        gr.staff_id,
        coalesce(gr.in_, CAST('08:30:00' AS TIME)) as in_,
        coalesce(gr.out_, CAST('18:00:00' AS TIME)) as out_,
        ceil(datediff (minute from coalesce(gr.in_, CAST('08:30:00' AS TIME)) to coalesce(gr.out_, CAST('18:00:00' AS TIME)))/60.0) as hours
        from gr
        where (gr.in_ is not null) and (gr.out_ is not null)
    ), hours_all as(
        select
        hours_per_day.staff_id,
        sum(hours) as sum_hours
        from hours_per_day
        group by hours_per_day.staff_id
    )
    select
        hours_all.staff_id,
        staff.last_name,
        staff.first_name,
        staff.middle_name,
        hours_all.sum_hours
        from hours_all
        inner join staff on staff.id_staff = hours_all.staff_id
        and TRIM(TABEL_ID) = 'ворк'

        --where staff.last_name like 'Вагано%'
        order by hours_all.staff_id


