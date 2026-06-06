"""
app.py — GYS Session-Based Dynamic Role Router
================================================
Architecture overview
─────────────────────
  /                       → gate.html          (public landing)
  /citizen/register       → register citizens  (TR stream & General stream)
  /citizen/login          → citizen login      → session user_type: 'citizen'
  /mobilization/login     → campaign login     → session user_type: 'campaign'
  /trustee/login          → board login        → session user_type: 'trustee'
  /home                   → index.html         (citizen view)
  /admin/sync-verification → sync.html         (trustee pre-dashboard)
  /admin/dashboard        → admin_dashboard.html (trustee command central)
  /admin/approve/<id>     → approval action
  /chat                   → chat.html
  /history                → history.html
  /logout                 → clears session

session keys written on login
──────────────────────────────
  session['user_type']   →  'citizen' | 'campaign' | 'trustee'
  session['user_name']   →  display name
  session['user_id']     →  DB record id (citizens only)
  session['approved']    →  bool (citizens only)
  session['is_admin']    →  True (trustee only)
"""

import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import (Flask, flash, redirect, render_template,
                   request, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

# ─────────────────────────────────────────────
# 1.  Bootstrap
# ─────────────────────────────────────────────
load_dotenv()

app = Flask(__name__)
os.makedirs(app.instance_path, exist_ok=True)

app.secret_key = os.getenv('SECRET_KEY', 'gys_secure_system_key_2026')

_db_url = os.getenv('DATABASE_URL', f"sqlite:///{Path(app.instance_path) / 'gys_registry.db'}")
if _db_url.startswith('postgres://'):
    _db_url = _db_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = _db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ─────────────────────────────────────────────
# 2.  Models
# ─────────────────────────────────────────────

class Citizen(db.Model):
    """Covers both GRA residents (TR_Citizen) and general mobilizers (General)."""
    id           = db.Column(db.Integer, primary_key=True)
    full_name    = db.Column(db.String(150), nullable=False)
    phone        = db.Column(db.String(50),  unique=True, nullable=False)
    reg_type     = db.Column(db.String(50),  nullable=False)   # TR_Citizen | General
    password     = db.Column(db.String(256), nullable=False)
    ward         = db.Column(db.String(100), nullable=True)
    pvc_number   = db.Column(db.String(100), nullable=True)
    email        = db.Column(db.String(150), nullable=True)
    area_name    = db.Column(db.String(150), nullable=True)
    house_number = db.Column(db.String(50),  nullable=True)
    approved     = db.Column(db.Boolean,     default=False)


class ChatMessage(db.Model):
    id           = db.Column(db.Integer,  primary_key=True)
    sender_name  = db.Column(db.String(100), nullable=False)
    sender_role  = db.Column(db.String(20),  nullable=False)
    message_text = db.Column(db.Text,        nullable=False)
    timestamp    = db.Column(db.DateTime,    default=datetime.utcnow)


class LogEvent(db.Model):
    id         = db.Column(db.Integer,  primary_key=True)
    event_type = db.Column(db.String(60), nullable=False)
    message    = db.Column(db.Text,       nullable=False)
    timestamp  = db.Column(db.DateTime,   default=datetime.utcnow)


with app.app_context():
    db.create_all()

# ─────────────────────────────────────────────
# 3.  Helpers
# ─────────────────────────────────────────────

def _hash(password: str) -> str:
    return generate_password_hash(password, method='pbkdf2:sha256')


def _verify(stored: str, provided: str) -> bool:
    return check_password_hash(stored, provided)


def _log(event_type: str, message: str) -> None:
    """Persist an audit log entry; silently swallows errors so it never
    interrupts a user-facing request."""
    try:
        db.session.add(LogEvent(event_type=event_type, message=message))
        db.session.commit()
    except Exception:
        db.session.rollback()


# ─────────────────────────────────────────────
# 4.  Security middleware
# ─────────────────────────────────────────────

# Routes that are open to unauthenticated visitors
_PUBLIC_ENDPOINTS = {
    'gate',
    'citizen_register_tr',
    'citizen_register',
    'citizen_register_general',
    'mobilization_register',
    'citizen_login',
    'mobilization_login',
    'trustee_login',
    'static',
}


@app.before_request
def require_authentication():
    """Redirect unauthenticated requests to the gate,
    except for public endpoints."""
    if request.endpoint in _PUBLIC_ENDPOINTS:
        return  # allow through
    if 'user_type' not in session:
        flash('Please log in to continue.')
        return redirect(url_for('gate'))


# ─────────────────────────────────────────────
# 5.  Public landing
# ─────────────────────────────────────────────

@app.route('/')
def gate():
    """Public entry point — shows the gate template with citizen login /
    register tabs and the trustee terminal panel."""
    return render_template(
        'gate.html',
        section='gate',
        session=session,
    )


# ─────────────────────────────────────────────
# 6.  Citizen registration  →  /citizen/register
# ─────────────────────────────────────────────

@app.route('/citizen/register/tr', methods=['POST'])
def citizen_register_tr():
    """Stream A — GRA Resident (TR_Citizen) registration."""
    full_name    = request.form.get('full_name', '').strip()
    phone        = request.form.get('phone', '').strip()
    email        = request.form.get('email', '').strip()
    ward_or_area = (request.form.get('ward') or request.form.get('area_name') or '').strip()
    password     = request.form.get('password', '')

    if not all([full_name, phone, password]):
        flash('Please fill in all required fields.')
        return redirect(url_for('gate'))

    if Citizen.query.filter_by(phone=phone).first():
        flash('Registration failed — this phone number is already on record.')
        return redirect(url_for('gate'))

    resident = Citizen(
        reg_type    = 'TR_Citizen',
        full_name   = full_name,
        phone       = phone,
        email       = email,
        ward        = ward_or_area,
        area_name   = ward_or_area,
        password    = _hash(password),
        approved    = False,
    )
    db.session.add(resident)
    db.session.commit()
    _log('REGISTER', f'TR Citizen registered: {full_name} ({phone})')

    flash('GRA Resident profile created. Awaiting board verification.')
    return redirect(url_for('gate'))


@app.route('/citizen/register/general', methods=['POST'])
def citizen_register_general():
    """Legacy path — kept so any old bookmarks still work."""
    # Reuse the mobilization_register logic by reposting internally
    full_name  = request.form.get('full_name', '').strip()
    phone      = request.form.get('phone', '').strip()
    email      = request.form.get('email', '').strip()
    ward       = request.form.get('ward', '').strip()
    pvc_number = request.form.get('pvc_number', '').strip()
    password   = request.form.get('password', '')

    if not all([full_name, phone, ward, pvc_number, password]):
        flash('Please fill in all required fields.')
        return redirect(url_for('gate'))

    if Citizen.query.filter_by(phone=phone).first():
        flash('Registration failed — profile parameters already exist.')
        return redirect(url_for('gate'))

    mobilizer = Citizen(
        reg_type   = 'General',
        full_name  = full_name,
        phone      = phone,
        email      = email,
        ward       = ward,
        pvc_number = pvc_number,
        password   = _hash(password),
        approved   = False,
    )
    db.session.add(mobilizer)
    db.session.commit()
    _log('REGISTER', f'General mobilizer registered: {full_name} ({phone})')

    flash('Campaign profile submitted. Awaiting administrative authorization.')
    return redirect(url_for('gate'))


@app.route('/citizen/register', methods=['GET', 'POST'])
def citizen_register():
    """Form A — GRA Citizen Registry.
    Accepts full_name, house_number, phone, email, id_document (file), password."""
    if request.method == 'GET':
        return redirect(url_for('gate') + '?tab=citizen')

    full_name    = request.form.get('full_name', '').strip()
    house_number = request.form.get('house_number', '').strip()
    phone        = request.form.get('phone', '').strip()
    email        = request.form.get('email', '').strip()
    password     = request.form.get('password', '')

    if not all([full_name, house_number, phone, password]):
        flash('Please fill in all required fields.')
        return redirect(url_for('gate') + '?tab=citizen')

    if Citizen.query.filter_by(phone=phone).first():
        flash('Registration failed — this phone number is already on record.')
        return redirect(url_for('gate') + '?tab=citizen')

    resident = Citizen(
        reg_type     = 'TR_Citizen',
        full_name    = full_name,
        phone        = phone,
        email        = email,
        house_number = house_number,
        area_name    = house_number,   # mirrors into area_name for existing views
        password     = _hash(password),
        approved     = False,
    )
    db.session.add(resident)
    db.session.commit()
    _log('REGISTER', f'GRA Citizen registered: {full_name} ({phone})')

    flash('GRA Citizen profile created. Awaiting board verification.')
    return redirect(url_for('gate'))


@app.route('/mobilization/register', methods=['POST'])
def mobilization_register():
    """Form B — Campaign Mobilization Enrollment.
    Accepts full_name, lga, ward, pvc_number, phone, password."""
    full_name  = request.form.get('full_name', '').strip()
    lga        = request.form.get('lga', '').strip()
    ward       = request.form.get('ward', '').strip()
    pvc_number = request.form.get('pvc_number', '').strip()
    phone      = request.form.get('phone', '').strip()
    password   = request.form.get('password', '')

    if not all([full_name, lga, ward, pvc_number, phone, password]):
        flash('Please fill in all required fields.')
        return redirect(url_for('gate') + '?tab=campaign')

    if Citizen.query.filter_by(phone=phone).first():
        flash('Enrollment failed — this phone number is already registered.')
        return redirect(url_for('gate') + '?tab=campaign')

    mobilizer = Citizen(
        reg_type   = 'General',
        full_name  = full_name,
        phone      = phone,
        ward       = f'{lga} / {ward}',   # LGA + ward stored together
        pvc_number = pvc_number,
        password   = _hash(password),
        approved   = False,
    )
    db.session.add(mobilizer)
    db.session.commit()
    _log('REGISTER', f'Campaign mobilizer enrolled: {full_name} ({phone}), LGA: {lga}, Ward: {ward}')

    flash('Campaign enrollment submitted. Awaiting administrative authorization.')
    return redirect(url_for('gate'))


# ─────────────────────────────────────────────
# 7.  Citizen login  →  /citizen/login
#     Sets user_type: 'citizen'
# ─────────────────────────────────────────────

@app.route('/citizen/login', methods=['POST'])
def citizen_login():
    phone    = request.form.get('phone', '').strip()
    password = request.form.get('password', '')

    user = Citizen.query.filter_by(phone=phone).first()

    if not user or not _verify(user.password, password):
        flash('Invalid credentials. Please check your phone number and password.')
        return redirect(url_for('gate'))

    if not user.approved:
        flash('Access blocked — your profile is still pending board verification.')
        return redirect(url_for('gate'))

    # ── Write session ──────────────────────────────────────────────────────
    session.clear()
    session['user_type'] = 'citizen'        # role discriminator
    session['user_name'] = user.full_name
    session['user_id']   = user.id
    session['approved']  = True
    # ───────────────────────────────────────────────────────────────────────

    _log('LOGIN', f'Citizen login: {user.full_name} (id={user.id})')
    return redirect(url_for('home'))


# ─────────────────────────────────────────────
# 8.  Mobilization login  →  /mobilization/login
#     Sets user_type: 'campaign'
# ─────────────────────────────────────────────

@app.route('/mobilization/login', methods=['GET', 'POST'])
def mobilization_login():
    """Login endpoint for campaign / mobilization officers.
    These are General-stream citizens whose role is explicitly 'campaign'
    rather than 'citizen' once they authenticate."""

    if request.method == 'GET':
        # Render the gate with the mobilization panel pre-selected
        return render_template(
            'gate.html',
            section='mobilization',
            session=session,
        )

    phone    = request.form.get('phone', '').strip()
    password = request.form.get('password', '')

    user = Citizen.query.filter_by(phone=phone, reg_type='General').first()

    if not user or not _verify(user.password, password):
        flash('Mobilization credentials not recognised.')
        return redirect(url_for('mobilization_login'))

    if not user.approved:
        flash('Campaign profile pending approval. Contact your board trustee.')
        return redirect(url_for('mobilization_login'))

    # ── Write session ──────────────────────────────────────────────────────
    session.clear()
    session['user_type'] = 'campaign'       # role discriminator
    session['user_name'] = user.full_name
    session['user_id']   = user.id
    session['approved']  = True
    # ───────────────────────────────────────────────────────────────────────

    _log('LOGIN', f'Campaign login: {user.full_name} (id={user.id})')
    return redirect(url_for('home'))


# ─────────────────────────────────────────────
# 9.  Trustee login  →  /trustee/login
#     Sets user_type: 'trustee'
# ─────────────────────────────────────────────

@app.route('/trustee/login', methods=['POST'])
def trustee_login():
    """Board trustee authentication. Accepts the code from both
    gate.html (trustee_code) and admin_gate.html (trustee_username)."""

    trustee_code = (
        request.form.get('trustee_code')
        or request.form.get('trustee_username')
        or ''
    ).strip()

    password = (
        request.form.get('password')
        or request.form.get('authentication_number')
        or ''
    )

    # Hard-coded board credentials (replace with a DB-backed trustee model
    # or environment variables for production use).
    VALID_CODE = os.getenv('TRUSTEE_CODE', 'GYS-BOT-77')
    VALID_PASS = os.getenv('TRUSTEE_PASS', 'Bauchi2026')

    if trustee_code == VALID_CODE and password == VALID_PASS:
        # ── Write session ──────────────────────────────────────────────────
        session.clear()
        session['user_type']     = 'trustee'    # role discriminator
        session['user_name']     = 'Board Trustee Member'
        session['is_admin']      = True
        session['trustee_node']  = trustee_code
        # ──────────────────────────────────────────────────────────────────

        _log('LOGIN', f'Trustee authenticated: {trustee_code}')
        return redirect(url_for('sync_processing_gate'))

    flash('ACCESS DENIED — Invalid administrative terminal clearance string.')
    return redirect(url_for('gate'))


# ─────────────────────────────────────────────
# 10.  Authenticated views
# ─────────────────────────────────────────────

@app.route('/home')
def home():
    """Main citizen / campaign portal view.
    Passes section='home' and the live session so the template can branch
    on session.user_type or session.role."""
    citizens = []
    if session.get('user_type') == 'trustee':
        citizens = Citizen.query.all()

    return render_template(
        'index.html',
        section='home',
        session=session,
        citizens=citizens,
    )


@app.route('/admin/sync-verification')
def sync_processing_gate():
    """Intermediate synchronisation screen shown to trustees before the
    command central dashboard loads."""
    if not session.get('is_admin'):
        flash('Authentication token missing. Please use the terminal gate.')
        return redirect(url_for('gate'))

    return render_template(
        'sync.html',
        section='sync',
        session=session,
    )


@app.route('/admin/dashboard')
def admin_dashboard():
    """Board command central — trustee-only view."""
    if session.get('user_type') != 'trustee':
        flash('Restricted path. Board trustee authorisation required.')
        return redirect(url_for('gate'))

    citizens = Citizen.query.all()
    return render_template(
        'admin_dashboard.html',
        section='admin_dashboard',
        session=session,
        citizens=citizens,
    )


# Legacy alias kept so existing nav links (/dashboard) still resolve
@app.route('/dashboard')
def dashboard():
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/approve/<int:citizen_id>')
def approve_citizen(citizen_id):
    if session.get('user_type') != 'trustee':
        return redirect(url_for('gate'))

    profile = Citizen.query.get_or_404(citizen_id)
    profile.approved = True
    db.session.commit()
    _log('APPROVE', f'Profile approved: {profile.full_name} (id={citizen_id})')

    flash(f'Profile #00{citizen_id} — {profile.full_name} — has been authorised.')
    return redirect(url_for('admin_dashboard'))


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        content = (request.form.get('message') or '').strip()
        if content:
            db.session.add(ChatMessage(
                sender_name = session.get('user_name', 'Anonymous'),
                sender_role = session.get('user_type', 'unknown'),
                message_text = content,
            ))
            db.session.commit()
            return redirect(url_for('chat'))

    messages = ChatMessage.query.order_by(ChatMessage.timestamp.asc()).all()
    return render_template(
        'chat.html',
        section='chat',
        session=session,
        messages=messages,
    )


@app.route('/history')
def history():
    logs = LogEvent.query.order_by(LogEvent.timestamp.desc()).all()
    return render_template(
        'history.html',
        section='history',
        session=session,
        logs=logs,
    )


@app.route('/logout')
def logout():
    session.clear()
    flash('Session closed. Secure node detached.')
    return redirect(url_for('gate'))


# ─────────────────────────────────────────────
# 11.  WSGI entry points
# ─────────────────────────────────────────────

application = app   # Render / gunicorn expects `application`

if __name__ == '__main__':
    app.run(port=8000, debug=True)
