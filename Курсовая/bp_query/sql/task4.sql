Select FIO_patient, Diagnosis
From patient
join reception on patient.id_p=reception.id_p
join karta on reception.id_zap=karta.id_zap
where Diagnosis = '$Diagnosis'
