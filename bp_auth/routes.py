from flask import Blueprint, session, render_template, request, current_app
from sql_provider import SQLProvider
from usedatabase import work_with_db, update_db
from access import login_permission_required

auth_app = Blueprint('auth', __name__, template_folder='templates')

provider = SQLProvider('bp_auth/sql')


@auth_app.route('/login', methods=['GET', 'POST'])
@login_permission_required
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')

        sql = provider.get('user.sql', login=login, password=password)

        result = work_with_db(current_app.config['DB_CONFIG'], sql)

        if len(result) > 0:
            session['group_name'] = result[0]['group_user']
            return render_template('success.html')

        return render_template('fail.html')


@auth_app.route('/register', methods=['GET', 'POST'])
@login_permission_required
def register_page():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')

        sql = provider.get('external_user.sql', login=login, password=password)
        print(sql)
        update_db(current_app.config['DB_CONFIG'], sql)
        return render_template('success_register.html')
