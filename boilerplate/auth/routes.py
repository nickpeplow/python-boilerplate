from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from .models import User
from boilerplate.database import db
from .forms import AccountForm, RegistrationForm

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    current_app.logger.info("Login route accessed")
    if request.method == 'POST':
        current_app.logger.info("Login POST request")
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            current_app.logger.info("Login failed: Invalid credentials")
            flash('Invalid email or password', 'error')
            return render_template('auth/login.html')
        
        next_page = request.args.get('next')
        login_user(user)
        
        if next_page and next_page != '/':
            return redirect(next_page)
        return redirect(url_for('sites.list'))
        
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Check if user already exists
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered', 'error')
                return render_template('auth/register.html', form=form)
            
            # Create new user
            user = User(
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            user.set_password(form.password.data)
            
            # Add to database
            db.session.add(user)
            db.session.commit()
            
            # Log the user in
            login_user(user)
            flash('Registration successful! Welcome!', 'success')
            
            # Redirect to sites list
            return redirect(url_for('sites.list'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration error: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'error')
    
    # If form validation failed, show errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'error')
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm(obj=current_user)
    
    if request.method == 'POST':
        if request.form.get('action') == 'update_profile':
            # Check if email is being changed
            if form.email.data != current_user.email:
                if User.query.filter_by(email=form.email.data).first():
                    flash('Email already exists', 'error')
                    return render_template('auth/account.html', form=form)

            # Update user details
            current_user.email = form.email.data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            db.session.commit()
            flash('Profile updated successfully', 'success')
                    
        elif request.form.get('action') == 'change_password':
            if form.new_password.data:
                if not current_user.check_password(form.current_password.data):
                    flash('Current password is incorrect', 'error')
                else:
                    current_user.set_password(form.new_password.data)
                    db.session.commit()
                    flash('Password changed successfully', 'success')
                    
    return render_template('auth/account.html', form=form) 