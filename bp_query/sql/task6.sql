Select FIO_patient,  FIO_doctor, time_visit
From patient
right join reception using (id_p)
join doctor using (id_d)
where otmetka = '$otmetka' and date_visit = '$date_visit'