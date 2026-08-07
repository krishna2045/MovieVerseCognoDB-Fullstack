from flask import render_template, request, flash, redirect, url_for, jsonify, make_response
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.extensions import neo4j_driver
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        # Support JSON payload or Form data
        if request.is_json:
            data = request.get_json() or {}
            username = data.get('username')
            password = data.get('password')
            remember = data.get('remember', False)
        else:
            username = request.form.get('username')
            password = request.form.get('password')
            remember = True if request.form.get('remember') else False

        driver = neo4j_driver.driver
        user = User.find_by_username(driver, username)

        if user and user.check_password(password):
            login_user(user, remember=remember)
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': True, 'redirect': url_for('main.home')})
            next_page = request.args.get('next')
            target_url = next_page if next_page else url_for('main.home')
            return render_template('auth/login.html', show_loading=True, redirect_url=target_url)
        else:
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if confirm_password and password != confirm_password:
            flash('Passwords do not match.', 'warning')
            return render_template('auth/register.html')

        driver = neo4j_driver.driver
        if User.find_by_username(driver, username) or User.find_by_username(driver, email):
            flash('Username or Email is already registered.', 'warning')
        else:
            password_hash = User.hash_password(password)
            User.create(driver, username, email, password_hash)
            flash('Account created successfully! Please sign in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    response = make_response(redirect(url_for('auth.login')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# OAuth placeholder endpoints to avoid 404s
@auth_bp.route('/google')
def google_login():
    flash('Google authentication available in production mode.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/github')
def github_login():
    flash('GitHub authentication available in production mode.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/apple')
def apple_login():
    flash('Apple authentication available in production mode.', 'info')
    return redirect(url_for('auth.login'))
