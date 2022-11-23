select id_d,
    FIO_doctor,
    Speciality,
    numb_kab,
    date_begin
from doctor
where status = 'on'
order by FIO_doctor