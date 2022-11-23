from flask import Blueprint, render_template, request, session, current_app, url_for
from werkzeug.utils import redirect
from sql_provider import SQLProvider
import os
from access import login_permission_required

from usedatabase import work_with_db, update_db

basket_app = Blueprint('basket', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(
    os.path.dirname(__file__), 'sql'))


@basket_app.route('/', methods=['GET', 'POST'])
@login_permission_required
def cart_init():
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        sql = provider.get('patient_list.sql')
        items = work_with_db(db_config, sql)
        print(items)
        return render_template('cart_init.html', items=items)
    else:
        session['patient_id'] = request.form['patient_id']
        print(session['patient_id'])
        if not session['patient_id']:
            return 'No valid patient ID'
        return redirect(url_for('basket.cart_speciality'))


@basket_app.route('/speciality', methods=['GET', 'POST'])
@login_permission_required
def cart_speciality():
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        sql = provider.get('speciality_list.sql')
        items = work_with_db(db_config, sql)
        print(items)
        return render_template('cart_speciality.html', items=items)
    else:
        speciality = request.form['Speciality']
        session['speciality'] = speciality
        if not session['speciality']:
            return 'No valid speciality'
        else:
            print(session['speciality'])
            return redirect(url_for('basket.cart_doctor'))


@basket_app.route('/doctor', methods=['GET', 'POST'])
@login_permission_required
def cart_doctor():
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        sql = provider.get('doctor_list.sql', speciality=session['speciality'])
        items = work_with_db(db_config, sql)
        print(items)
        return render_template('cart_doctor.html', items=items)
    else:
        doctor_id = request.form['doctor_id']
        session['doctor_id'] = doctor_id
        if not session['doctor_id']:
            return 'No valid doctor ID'
        print(session['doctor_id'])
        return redirect(url_for('basket.cart_timetable'))


@basket_app.route('/timetable', methods=['GET', 'POST'])
@login_permission_required
def cart_timetable():
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        sql = provider.get('timetable_list.sql', id_d=session['doctor_id'])
        items = work_with_db(db_config, sql)
        print(items)
        return render_template('cart_timetable.html', items=items)
    else:
        date_zap = request.form['date_zap']
        time_zap = request.form['time_zap']
        session['date_zap'] = date_zap
        session['time_zap'] = time_zap
        print(session['date_zap'])
        print(session['time_zap'])
        return redirect(url_for('basket.cart_confirm'))


@basket_app.route('/confirm', methods=['GET', 'POST'])
@login_permission_required
def cart_confirm():
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        sql = provider.get('confirm_data.sql', id_p=session['patient_id'], id_d=session['doctor_id'])
        items = work_with_db(db_config, sql)
        return render_template('cart_confirm.html', items=items)
    else:
        sql_insert = provider.get('data_insert.sql', date_zap=session['date_zap'],
                                  time_zap=session['time_zap'],
                                  patient_id=session['patient_id'],
                                  doctor_id=session['doctor_id'])
        update_db(db_config, sql_insert)
        print('SQL: ' + str(sql_insert))
        sql_update = provider.get('data_update.sql', date_zap=session['date_zap'],
                                  time_zap=session['time_zap'],
                                  doctor_id=session['doctor_id'])
        update_db(db_config, sql_update)
        print('SQL: ' + str(sql_update))
        return render_template('cart_confirm_end.html')
