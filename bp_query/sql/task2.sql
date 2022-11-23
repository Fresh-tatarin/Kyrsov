Select FIO_patient, time_visit
From patient
join reception using (id_p)
join doctor using (id_d)
where FIO_doctor = '$FIO_doctor' and date_visit = '$date_visit'