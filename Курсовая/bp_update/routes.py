from flask import Blueprint, request, render_template, current_app, redirect
from access import login_permission_required
from sql_provider import SQLProvider
from usedatabase import work_with_db, update_db

update_app = Blueprint('update', __name__, template_folder='templates')

provider = SQLProvider('bp_update/sql')


@update_app.route('/', methods=['GET', 'POST'])
@login_permission_required
def get_bp_index():
    if request.method == 'GET':
        items = work_with_db(
            current_app.config['DB_CONFIG'], provider.get('doctorlist.sql'))
        print(items)
        return render_template('start_list.html', items=items, heads=['Фамилия Имя Отчество', 'Специальность',
                                                                      'Номер кабинета', 'Дата начала работы','Удалить'])
    else: 
        id_d = request.form.get('id_d')
        print('id_d = ', id_d)
        sql = provider.get('delete_doctor.sql', id_d=id_d)
        print('sql = ', sql)
        result = update_db(current_app.config['DB_CONFIG'], sql)
        print(result)
        return redirect('/update')


@update_app.route('/add', methods=['GET', 'POST'])
@login_permission_required
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        fio_doctor = request.form.get('FIO_doctor')
        speciality = request.form.get('Speciality')
        numb_kab = request.form.get('numb_kab')
        date_begin = request.form.get('date_begin')
        if fio_doctor and speciality and date_begin and numb_kab:
            sql = provider.get('insert_doctor.sql',
                               FIO_doctor=fio_doctor, Speciality=speciality, numb_kab=numb_kab, date_begin=date_begin)
            update_db(current_app.config['DB_CONFIG'], sql)
            return redirect('/update')
        return 'Error'
