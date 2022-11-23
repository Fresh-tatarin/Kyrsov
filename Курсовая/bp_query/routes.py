from flask import Blueprint, request, render_template, current_app

from sql_provider import SQLProvider
from usedatabase import work_with_db
from access import login_permission_required

request_app = Blueprint('request', __name__, template_folder='templates')

provider = SQLProvider('bp_query/sql')


@request_app.route('/')
@login_permission_required
def get_bp_index():
    return render_template('request_menu.html')


@request_app.route('/task1')
@login_permission_required
def task1():
    Speciality = request.args.get('Speciality')
    if Speciality is None:
        return render_template('query_task1.html')
    print(Speciality)
    sql = provider.get('task1.sql', Speciality=Speciality)
    print(sql)
    db_config = current_app.config['DB_CONFIG']
    result = work_with_db(db_config, sql)

    context = {'schema': ['Фамилия Имя Отчество', 'Специальность'], 'data': result}

    return render_template('query_result.html', context=context)


@request_app.route('/task2')
@login_permission_required
def task2():
    FIO_doctor = request.args.get('FIO_doctor')
    date_visit = request.args.get('date_visit')
    if FIO_doctor is None or date_visit is None:
        return render_template('query_task2.html')
    sql = provider.get('task2.sql', FIO_doctor=FIO_doctor, date_visit=date_visit)
    db_config = current_app.config['DB_CONFIG']
    result = work_with_db(db_config, sql)

    context = {'schema': ['Фамилия Имя Отчество', 'Время посещения'], 'data': result}

    return render_template('query_result.html', context=context)


@request_app.route('/task3')
@login_permission_required
def task3():
    FIO_patient = request.args.get('FIO_patient')
    if FIO_patient is None:
        return render_template('query_task3.html')
    sql = provider.get('task3.sql', FIO_patient=FIO_patient)
    print(sql)
    db_config = current_app.config['DB_CONFIG']
    result = work_with_db(db_config, sql)

    context = {'schema': [
        '№ рецепта', 'Жалобы',  'Диагноз', 'Дата', 'Время', 'ФИО врача'], 'data': result}

    return render_template('query_result.html', context=context)


@request_app.route('/task4')
@login_permission_required
def task4():
    Diagnosis = request.args.get('Diagnosis')
    if Diagnosis is None:
        return render_template('query_task4.html')
    sql = provider.get('task4.sql', Diagnosis=Diagnosis)
    db_config = current_app.config['DB_CONFIG']
    result = work_with_db(db_config, sql)

    context = {'schema': ['Фамилия Имя Отчество', 'Диагноз'], 'data': result}

    return render_template('query_result.html', context=context)


@request_app.route('/task5')
@login_permission_required
def task5():
    birthday = request.args.get('birthday')
    if birthday is None:
        return render_template('query_task5.html')
    sql = provider.get('task5.sql', birthday=birthday)
    db_config = current_app.config['DB_CONFIG']
    result = work_with_db(db_config, sql)

    context = {'schema': ['Фамилия Имя Отчество', 'Дата рождения', 'Адрес'], 'data': result}

    return render_template('query_result.html', context=context)


@request_app.route('/task6')
@login_permission_required
def task6():
    otmetka = request.args.get('otmetka')
    date_visit = request.args.get('date_visit')
    if otmetka is None or date_visit is None:
        return render_template('query_task6.html')
    sql = provider.get('task6.sql', otmetka=otmetka, date_visit=date_visit)
    db_config = current_app.config['DB_CONFIG']
    result = work_with_db(db_config, sql)

    context = {'schema': ['ФИО пациента', 'ФИО врача', 'Время посещения'], 'data': result}

    return render_template('query_result.html', context=context)