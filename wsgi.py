import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash

application = Flask(__name__)
app = application
app.secret_key = 'gys_secure_system_key_2026'

# --- EMAIL CONFIGURATION ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'grayouthsupporters@gmail.com'
app.config['MAIL_PASSWORD'] = '001122GRA'
app.config['MAIL_DEFAULT_SENDER'] = ('GYS Platform', 'grayouthsupporters@gmail.com')
mail = Mail(app)

# --- DATABASE CONFIGURATION ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'gys_registry.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Comprehensive Database Models
class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_type = db.Column(db.String(50), nullable=False) 
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    
    area_name = db.Column(db.String(100), nullable=True)
    house_number = db.Column(db.String(50), nullable=True)
    
    ward = db.Column(db.String(100), nullable=True)
    pvc_number = db.Column(db.String(50), unique=True, nullable=True)
    address = db.Column(db.Text, nullable=True)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.String(100), nullable=False)
    sender_role = db.Column(db.String(20), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# --- SECURITY GATEKEEPER MIDDLEWARE ---
@app.before_request
def check_security_clearance():
    allowed_routes = ['gate', 'register_tr', 'register_general', 'citizen_login', 'trustee_login', 'static']
    if request.endpoint not in allowed_routes and 'user_name' not in session:
        return redirect(url_for('gate'))

@app.route('/gate')
def gate():
    if 'user_name' in session:
        return redirect(url_for('home'))
    return render_template('gate.html')

@app.route('/')
def home():
    if session.get('role') == 'citizen' and not session.get('approved'):
        flash('Your registration profile is currently pending review. Access will be authorized once a Trustee verifies your credentials.')
        session.clear()
        return redirect(url_for('gate'))
        
    all_citizens = []
    if session.get('role') == 'trustee':
        try:
            all_citizens = Citizen.query.all()
        except Exception:
            all_citizens = []
            
    return render_template('index.html', citizens=all_citizens)

@app.route('/register/tr', methods=['POST'])
def register_tr():
    full_name = request.form.get('full_name')
    area_name = request.form.get('area_name')
    house_number = request.form.get('house_number')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')

    if Citizen.query.filter((Citizen.phone == phone) | (Citizen.email == email)).first():
        flash('Registration Error: Phone number or Email already exists.')
        return redirect(url_for('gate'))

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_tr = Citizen(
        reg_type='TR_Citizen', full_name=full_name, area_name=area_name,
        house_number=house_number, phone=phone, email=email,
        password=hashed_password, approved=False
    )
    db.session.add(new_tr)
    db.session.commit()
    
    flash('Profile Saved! Your TR Citizen account is pending executive validation.')
    return redirect(url_for('gate'))

@app.route('/register/general', methods=['POST'])
def register_general():
    full_name = request.form.get('full_name')
    address = request.form.get('address')
    ward = request.form.get('ward')
    pvc_number = request.form.get('pvc_number')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')

    if Citizen.query.filter((Citizen.phone == phone) | (Citizen.email == email) | (Citizen.pvc_number == pvc_number)).first():
        flash('Registration Error: Phone, Email, or PVC Number already exists.')
        return redirect(url_for('gate'))

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_general = Citizen(
        reg_type='General_Mobilization', full_name=full_name, address=address,
        ward=ward, pvc_number=pvc_number, phone=phone, email=email,
        password=hashed_password, approved=False
    )
    db.session.add(new_general)
    db.session.commit()

    flash('Campaign Profile Registered! Access pending verification.')
    return redirect(url_for('gate'))

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
    trustee_username = request.form.get('trustee_username')
    authentication_number = request.form.get('authentication_number')

    if trustee_username == "GYS-BOT-77" and authentication_number == "Bauchi2026":
        session['user_name'] = "Board Trustee Member"
        session['role'] = 'trustee'
        return redirect(url_for('home'))
    
    flash('Access Denied: Invalid Username or Authentication Key.')
    return redirect(url_for('gate'))

@app.route('/admin/approve/<int:citizen_id>')
def approve_citizen(citizen_id):
    if session.get('role') != 'trustee':
        return redirect(url_for('gate'))
    citizen = Citizen.query.get_or_404(citizen_id)
    citizen.approved = True
    db.session.commit()
    flash(f"Profile for {citizen.full_name} has been activated.")
    return redirect(url_for('home'))

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
    return render_template('history.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('gate'))

if __name__ == '__main__':
    app.run(debug=True)