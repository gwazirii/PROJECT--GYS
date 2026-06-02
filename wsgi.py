import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'gys_secure_system_key_2026')

# --- EMAIL CONFIGURATION ---
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('1', 'true', 'yes')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = (
    os.environ.get('MAIL_SENDER_NAME', 'GYS Platform'),
    os.environ.get('MAIL_SENDER_EMAIL', os.environ.get('MAIL_USERNAME', 'no-reply@example.com'))
)
mail = Mail(app)

# --- DATABASE CONFIGURATION ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'gys_registry.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Comprehensive Database Model for All Registrants
class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_type = db.Column(db.String(50), nullable=False) # 'TR_Citizen' or 'General_Mobilization'
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    
    # TR Specific Fields
    area_name = db.Column(db.String(100), nullable=True)
    house_number = db.Column(db.String(50), nullable=True)
    
    # Campaign Mobilization Fields
    ward = db.Column(db.String(100), nullable=True)
    pvc_number = db.Column(db.String(50), unique=True, nullable=True)
    address = db.Column(db.Text, nullable=True)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.String(100), nullable=False)
    sender_role = db.Column(db.String(20), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class LogEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(60), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()


def record_log(event_type, message):
    log = LogEvent(event_type=event_type, message=message)
    db.session.add(log)
    db.session.commit()

# --- SECURITY GATEKEEPER MIDDLEWARE ---
@app.before_request
def check_security_clearance():
    allowed_routes = ['gate', 'admin_gate', 'register_tr', 'register_general', 'citizen_login', 'trustee_login', 'static']
    if request.endpoint not in allowed_routes and 'user_name' not in session:
        return redirect(url_for('gate'))

@app.route('/gate')
def gate():
    if 'user_name' in session:
        return redirect(url_for('home'))
    return render_template('gate.html')

@app.route('/admin/gate')
def admin_gate():
    if 'user_name' in session:
        return redirect(url_for('home'))
    return render_template('admin_gate.html')

@app.route('/')
def home():
    if session.get('role') == 'citizen' and not session.get('approved'):
        flash('Waiting for Trustee authorization clearance.')
        session.clear()
        return redirect(url_for('gate'))
    return render_template('index.html')

# 1. TR CITIZEN REGISTRATION ROUTE
@app.route('/register/tr', methods=['POST'])
def register_tr():
    full_name = request.form.get('full_name')
    area_name = request.form.get('area_name')
    house_number = request.form.get('house_number')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')

    if Citizen.query.filter((Citizen.phone == phone) | (Citizen.email == email)).first():
        flash('Registration Error: Phone number or Email already exists inside the GYS system.')
        return redirect(url_for('gate'))

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_tr = Citizen(
        reg_type='TR_Citizen', full_name=full_name, area_name=area_name,
        house_number=house_number, phone=phone, email=email,
        password=hashed_password, approved=False
    )
    db.session.add(new_tr)
    db.session.commit()
    record_log('registration', f'New TR registration submitted for {full_name} ({phone}).')
    
    flash('Profile Saved! Your TR Citizen account is pending executive validation.')
    return redirect(url_for('gate'))

# 2. GENERAL CAMPAIGN MOBILIZATION ROUTE (REQUIRES PVC)
@app.route('/register/general', methods=['POST'])
def register_general():
    full_name = request.form.get('full_name')
    ward = request.form.get('ward')
    pvc_number = request.form.get('pvc_number')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')

    # The PVC registry intentionally tracks only voting ward and PVC VIN identifiers.
    if Citizen.query.filter((Citizen.phone == phone) | (Citizen.email == email) | (Citizen.pvc_number == pvc_number)).first():
        flash('Registration Error: Phone, Email, or PVC Number already exists inside our mobilization directory.')
        return redirect(url_for('gate'))

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    address = request.form.get('address')
    new_general = Citizen(
        reg_type='General_Mobilization', full_name=full_name,
        ward=ward, pvc_number=pvc_number, address=address,
        phone=phone, email=email, password=hashed_password,
        approved=False
    )
    db.session.add(new_general)
    db.session.commit()
    record_log('registration', f'New PVC registration submitted for {full_name} ({phone}).')

    flash('Campaign Profile Registered! Access pending verification.')
    return redirect(url_for('gate'))

# LOGIN & TERMINAL OPERATIONS
@app.route('/citizen/login', methods=['POST'])
def citizen_login():
    phone = request.form.get('phone')
    password = request.form.get('password')

    user = Citizen.query.filter_by(phone=phone).first()
    if user and check_password_hash(user.password, password):
        if not user.approved:
            flash('Waiting for Trustee authorization clearance.')
            record_log('access_blocked', f'Pending clearance login blocked for {user.full_name} ({phone}).')
            return redirect(url_for('gate'))

        session['user_name'] = user.full_name
        session['role'] = 'citizen'
        session['approved'] = True
        record_log('login', f'Citizen {user.full_name} ({phone}) logged in.')
        return redirect(url_for('home'))
    
    flash('Invalid verification credentials.')
    return redirect(url_for('gate'))

@app.route('/trustee/login', methods=['POST'])
def trustee_login():
    trustee_username = request.form.get('trustee_username')
    authentication_number = request.form.get('authentication_number')

    if trustee_username == "GYS-BOT-77" and authentication_number == "Bauchi2026":
        session['user_name'] = "Board Trustee Member"
        session['role'] = 'trustee'
        record_log('trustee_login', 'Board Trustee authenticated and entered the dashboard.')
        return redirect(url_for('dashboard'))
    
    flash('Access Denied: Invalid Username or Authentication Key.')
    record_log('access_denied', f'Failed trustee login attempt for {trustee_username}.')
    return redirect(url_for('gate'))

@app.route('/dashboard')
def dashboard():
    if session.get('role') != 'trustee':
        return redirect(url_for('gate'))
    all_citizens = Citizen.query.all()
    return render_template('admin_dashboard.html', citizens=all_citizens)

@app.route('/admin/approve/<int:citizen_id>')
def approve_citizen(citizen_id):
    if session.get('role') != 'trustee':
        return redirect(url_for('gate'))
    citizen = Citizen.query.get_or_404(citizen_id)
    citizen.approved = True
    db.session.commit()
    record_log('approval', f'Trustee approved profile for {citizen.full_name} ({citizen.phone}).')
    flash(f"Profile for {citizen.full_name} has been activated.")
    return redirect(url_for('dashboard'))

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if session.get('role') == 'citizen' and not session.get('approved'):
        return redirect(url_for('gate'))
    if request.method == 'POST':
        msg_content = request.form.get('message')
        if msg_content and msg_content.strip():
            new_msg = ChatMessage(sender_name=session.get('user_name'), sender_role=session.get('role'), message_text=msg_content.strip())
            db.session.add(new_msg)
            db.session.commit()
            record_log('chat', f'{session.get("user_name")} ({session.get("role")}) posted a message.')
            return redirect(url_for('chat'))
    messages = ChatMessage.query.order_by(ChatMessage.timestamp.asc()).all()
    return render_template('chat.html', messages=messages)

@app.route('/history')
def history():
    logs = LogEvent.query.order_by(LogEvent.timestamp.desc()).limit(100).all()
    return render_template('history.html', logs=logs)

@app.route('/logout')
def logout():
    user_name = session.get('user_name')
    role = session.get('role')
    if user_name:
        record_log('logout', f'{user_name} ({role}) signed out.')
    session.clear()
    return redirect(url_for('gate'))

if __name__ == '__main__':
    app.run(debug=True)