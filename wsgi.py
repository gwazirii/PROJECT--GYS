import os
import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

# 1. Load environment variables
load_dotenv()

# 2. Application setup (supports Render)
application = Flask(__name__)
app = application  # Dual alias mapping for local vs Render configurations
os.makedirs(app.instance_path, exist_ok=True)

# 3. Assign configurations
app.secret_key = os.getenv('SECRET_KEY', 'gys_secure_system_key_2026')
database_url = os.getenv('DATABASE_URL', 'sqlite:///gys_registry.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 4. Initialize DB
db = SQLAlchemy(app)

# 5. Unified Citizen ledger model
class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_type = db.Column(db.String(50), nullable=False)  # 'TR_Citizen' or 'General_Campaign'
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(150), nullable=True)
    password = db.Column(db.String(150), nullable=False)
    
    # GRA Resident Specific Attributes
    area_name = db.Column(db.String(150), nullable=True)
    house_number = db.Column(db.String(50), nullable=True)
    
    # General Campaign Specific Attributes
    ward = db.Column(db.String(100), nullable=True)
    pvc_number = db.Column(db.String(100), nullable=True)
    
    # Authorization state
    approved = db.Column(db.Boolean, default=False)

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

# Initialize tables after all models are registered.
with app.app_context():
    db.create_all()

# --- SECURITY GATEKEEPER MIDDLEWARE ---
@app.before_request
def check_security_clearance():
    allowed_routes = ['gate', 'register_tr', 'register_general', 'citizen_login', 'trustee_login', 'sync_processing_gate', 'admin_dashboard', 'approve_citizen', 'logout', 'static']
    if request.endpoint not in allowed_routes and 'user_name' not in session:
        return redirect(url_for('gate'))
@app.route('/')
def gate():
    return render_template('gate.html')


@app.route('/home')
def home():
    if session.get('role') == 'citizen' and not session.get('approved'):
        flash('Your registration profile is currently pending review. Access will be authorized once a Trustee verifies your credentials.')
        session.clear()
        return redirect(url_for('gate'))
    return render_template('index.html')

# 1. Stream A Form: GRA Resident Submission Handler
@app.route('/register/tr', methods=['POST'])
def register_tr():
    try:
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        email = request.form.get('email') or ''
        ward_or_area = request.form.get('ward') or request.form.get('area_name')
        password = request.form.get('password')

        # Prevent duplicates
        existing = Citizen.query.filter_by(phone=phone).first()
        if existing:
            flash('Registration failed. Phone line already logged in database system.')
            return redirect(url_for('gate'))

        hashed = generate_password_hash(password, method='pbkdf2:sha256') if password else ''
        new_resident = Citizen(
            reg_type='TR_Citizen',
            full_name=full_name,
            phone=phone,
            email=email,
            area_name=ward_or_area,
            password=hashed,
            approved=False
        )
        db.session.add(new_resident)
        db.session.commit()

        flash('GRA Resident identity file created successfully! Awaiting board verification.')
        return redirect(url_for('gate'))
    except Exception as e:
        flash(f'System Entry Error: {str(e)}')
        return redirect(url_for('gate'))

# 2. Stream B Form: General Campaign Registration Handler
@app.route('/register/general', methods=['POST'])
def register_general():
    try:
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        email = request.form.get('email') or ''
        ward = request.form.get('ward')
        pvc_number = request.form.get('pvc_number')
        password = request.form.get('password')

        existing = Citizen.query.filter_by(phone=phone).first()
        if existing:
            flash('Registration failed. Profile parameters already exist.')
            return redirect(url_for('gate'))

        hashed = generate_password_hash(password, method='pbkdf2:sha256') if password else ''
        new_campaigner = Citizen(
            reg_type='General_Campaign',
            full_name=full_name,
            phone=phone,
            email=email,
            ward=ward,
            pvc_number=pvc_number,
            password=hashed,
            approved=False
        )
        db.session.add(new_campaigner)
        db.session.commit()

        flash('Campaign Profile registered! Profile pending administrative authorization.')
        return redirect(url_for('gate'))
    except Exception as e:
        flash(f'System Registry Error: {str(e)}')
        return redirect(url_for('gate'))

# LOGIN & TERMINAL OPERATIONS
@app.route('/citizen/login', methods=['POST'])
def citizen_login():
    phone = request.form.get('phone')
    password = request.form.get('password')

    user = Citizen.query.filter_by(phone=phone).first()
    if user and check_password_hash(user.password, password):
        if not user.approved:
            flash('Access Blocked: Your profile verification is still pending.')
            return redirect(url_for('gate'))

        session['user_name'] = user.full_name
        session['role'] = 'citizen'
        session['approved'] = True
        return redirect(url_for('home'))

    flash('Invalid verification credentials.')
    return redirect(url_for('gate'))

@app.route('/trustee/login', methods=['POST'])
def trustee_login():
    trustee_code = request.form.get('trustee_code') or request.form.get('trustee_username')
    password = request.form.get('password') or request.form.get('authentication_number')

    # Absolute core verification safety handshake logic
    if trustee_code == "GYS-BOT-77" and password == "Bauchi2026":
        session['is_admin'] = True
        session['trustee_node'] = trustee_code
        session['user_name'] = "Board Trustee Member"
        session['role'] = 'trustee'

        # Send them directly to the Synchronization Processing view first!
        return redirect(url_for('sync_processing_gate'))
    else:
        flash("ACCESS DENIED: Invalid Administrative Terminal Clearance String.")
        return redirect(url_for('gate'))

@app.route('/dashboard')
def dashboard():
    if session.get('role') != 'trustee':
        return redirect(url_for('gate'))
    all_citizens = Citizen.query.all()
    return render_template('dashboard.html', citizens=all_citizens)


# 2. Intermediate Security Synchronization Interface View
@app.route('/admin/sync-verification')
def sync_processing_gate():
    if not session.get('is_admin'):
        flash("Authentication token missing. Please access the portal terminal gate.")
        return redirect(url_for('gate'))
    return render_template('sync.html')


# 3. Clean Command Central Dashboard Endpoint
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        flash("Restricted administrative entry path. Authorization required.")
        return redirect(url_for('gate'))
        
    # Read all citizen records directly out of our database to map onto the clear table layout
    all_citizens = Citizen.query.all()
    return render_template('dashboard.html', citizens=all_citizens)

@app.route('/admin/approve/<int:citizen_id>')
def approve_citizen(citizen_id):
    if not session.get('is_admin'):
        return redirect(url_for('gate'))
        
    target_profile = Citizen.query.get_or_404(citizen_id)
    target_profile.approved = True
    db.session.commit()
    
    flash(f"Success: Verified tracking file for record ID #00{citizen_id} has been activated.")
    return redirect(url_for('admin_dashboard'))

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
            return redirect(url_for('chat'))
    messages = ChatMessage.query.order_by(ChatMessage.timestamp.asc()).all()
    return render_template('chat.html', messages=messages)

@app.route('/history')
def history():
    logs = LogEvent.query.order_by(LogEvent.timestamp.desc()).all()
    return render_template('history.html', logs=logs)

@app.route('/logout')
def logout():
    session.clear()
    flash("Session connection closed cleanly. Secure node detached.")
    return redirect(url_for('gate'))

application = app

if __name__ == '__main__':
    # Used for local development execution parameters
    app.run(port=8000, debug=True)
