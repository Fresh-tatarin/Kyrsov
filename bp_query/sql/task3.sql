Select id_zap, Complaints, Diagnosis, date_visit, time_visit, FIO_doctor
From karta
join reception using (id_zap)
join patient on reception.id_p = patient.id_p
join doctor on reception.id_d = doctor.id_d
where FIO_patient = '$FIO_patient'