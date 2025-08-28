from flask import Blueprint, render_template, redirect, request, session, url_for, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        email = request.form.get('email')
        password = request.form.get('password')  # you can add password validation here

        if not role or not email or not password:
            flash("Please fill out all fields")
            return render_template('login.html')

        # In real app, validate user credentials here before login

        session['role'] = role
        session['email'] = email
        flash("Logged in as " + role)

        role_to_endpoint = {
            'Job Seeker': 'dashboard_seeker',
            'Employer': 'dashboard_employer'
        }
        endpoint = role_to_endpoint.get(role)
        if endpoint:
            return redirect(url_for('auth.' + endpoint))
        else:
            flash("Invalid role")
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Add registration logic here
        flash("Registered successfully")
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/dashboard/seeker')
def dashboard_seeker():
    if session.get('role') != 'Job Seeker':
        flash("Access denied.")
        return redirect(url_for('auth.login'))
    return render_template('dashboard_seeker.html', current_user=session.get('email'))

@auth_bp.route('/dashboard/employer')
def dashboard_employer():
    if session.get('role') != 'Employer':
        flash("Access denied.")
        return redirect(url_for('auth.login'))
    return render_template('dashboard_employer.html', current_user=session.get('email'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
