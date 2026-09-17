"""
app.py — GYS Session-Based Dynamic Role Router
================================================
Architecture overview
─────────────────────
  /                       → gate.html          (public landing)
  /mobilization/register  → campaign registration
  /mobilization/login     → campaign login     → session user_type: 'campaign'
  /trustee/login          → board login        → session user_type: 'trustee'
  /home                   → index.html         (authenticated portal view)
  /admin/sync-verification → sync.html         (trustee pre-dashboard)
  /admin/dashboard        → admin_dashboard.html (trustee command central)
  /admin/approve/<id>     → approval action
  /chat                   → chat.html
  /history                → history.html
  /logout                 → clears session

session keys written on login
──────────────────────────────
  session['user_type']   →  'campaign' | 'trustee'
  session['user_name']   →  display name
  session['user_id']     →  DB record id
  session['approved']    →  bool
  session['is_admin']    →  True (trustee only)
"""

import os
import re
import secrets
import uuid
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import (Flask, abort, flash, redirect, render_template,
                   request, send_from_directory, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, inspect, or_, text
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

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
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024

PASSPORT_UPLOAD_DIR = Path(app.instance_path) / 'uploads' / 'passports'
MAX_PASSPORT_BYTES = 5 * 1024 * 1024
ALLOWED_IMAGE_SIGNATURES = {
    '.jpg': ('image/jpeg', lambda data: data.startswith(b'\xff\xd8\xff')),
    '.jpeg': ('image/jpeg', lambda data: data.startswith(b'\xff\xd8\xff')),
    '.png': ('image/png', lambda data: data.startswith(b'\x89PNG\r\n\x1a\n')),
    '.webp': ('image/webp', lambda data: data.startswith(b'RIFF') and data[8:12] == b'WEBP'),
}

db = SQLAlchemy(app)

# ─────────────────────────────────────────────
# 2.  Models
# ─────────────────────────────────────────────

class Citizen(db.Model):
    """Legacy registry table reused for campaign registrations."""
    id           = db.Column(db.Integer, primary_key=True)
    full_name    = db.Column(db.String(150), nullable=False)
    phone        = db.Column(db.String(50),  unique=True, nullable=False)
    username     = db.Column(db.String(80), nullable=True)
    reg_type     = db.Column(db.String(50),  nullable=False)   # General for campaign registrations
    password     = db.Column(db.String(256), nullable=False)
    ward         = db.Column(db.String(100), nullable=True)
    pvc_number   = db.Column(db.String(100), nullable=True)
    email        = db.Column(db.String(150), nullable=True)
    area_name    = db.Column(db.String(150), nullable=True)
    house_number = db.Column(db.String(50),  nullable=True)
    passport_image = db.Column(db.String(255), nullable=True)
    approved     = db.Column(db.Boolean,     default=False)
    created_at   = db.Column(db.DateTime,    default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime,    default=datetime.utcnow, onupdate=datetime.utcnow)


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


def _ensure_schema_columns() -> None:
    """Add minimal columns needed by the simplified campaign registration flow."""
    inspector = inspect(db.engine)
    columns = {column['name'] for column in inspector.get_columns('citizen')}
    dialect = db.engine.dialect.name

    if dialect == 'postgresql':
        statements = {
            'passport_image': 'ALTER TABLE citizen ADD COLUMN IF NOT EXISTS passport_image VARCHAR(255)',
            'created_at': 'ALTER TABLE citizen ADD COLUMN IF NOT EXISTS created_at TIMESTAMP',
            'updated_at': 'ALTER TABLE citizen ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP',
            'username': 'ALTER TABLE citizen ADD COLUMN IF NOT EXISTS username VARCHAR(80)',
        }
    else:
        statements = {
            'passport_image': 'ALTER TABLE citizen ADD COLUMN passport_image VARCHAR(255)',
            'created_at': 'ALTER TABLE citizen ADD COLUMN created_at DATETIME',
            'updated_at': 'ALTER TABLE citizen ADD COLUMN updated_at DATETIME',
            'username': 'ALTER TABLE citizen ADD COLUMN username VARCHAR(80)',
        }

    for column_name, statement in statements.items():
        if column_name not in columns:
            db.session.execute(text(statement))

    db.session.commit()


def _normalize_email(value: str) -> str:
    return (value or '').strip().lower()


def _normalize_name(value: str) -> str:
    return re.sub(r'\s+', ' ', (value or '').strip())


def _normalize_pvc_number(value: str) -> str:
    return (value or '').strip().upper()


def _is_valid_email(value: str) -> bool:
    return bool(re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', value or ''))


def _is_valid_pvc_number(value: str) -> bool:
    return bool(re.fullmatch(r'[A-Z0-9/-]{5,50}', value or ''))


def _validate_passport_upload(file_storage):
    if not file_storage or not file_storage.filename:
        return False, 'Passport photograph is required.'

    original_name = secure_filename(file_storage.filename)
    extension = Path(original_name).suffix.lower()
    if extension not in ALLOWED_IMAGE_SIGNATURES:
        return False, 'Passport photograph must be a JPG, JPEG, PNG, or WebP image.'

    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)
    if size <= 0:
        return False, 'Passport photograph is empty.'
    if size > MAX_PASSPORT_BYTES:
        return False, 'Passport photograph must not exceed 5 MB.'

    header = file_storage.stream.read(16)
    file_storage.stream.seek(0)
    if not ALLOWED_IMAGE_SIGNATURES[extension][1](header):
        return False, 'Passport photograph is not a valid image file.'

    safe_filename = f'{uuid.uuid4().hex}{extension}'
    PASSPORT_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_storage.save(PASSPORT_UPLOAD_DIR / safe_filename)
    return True, safe_filename


with app.app_context():
    db.create_all()
    _ensure_schema_columns()


# ─────────────────────────────────────────────
# 4.  Security middleware
# ─────────────────────────────────────────────

# Routes that are open to unauthenticated visitors
_PUBLIC_ENDPOINTS = {
    'gate',
    'mobilization_register',
    'mobilization_login',
    'login',
    'registration_success',
    'admin_login',
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
        # If the user is trying to access the dashboard, send them to the participant login
        if request.endpoint == 'dashboard' or request.path.startswith('/dashboard'):
            flash('Please log in to continue.')
            return redirect(url_for('login'))
        flash('Please log in to continue.')
        return redirect(url_for('gate'))


@app.errorhandler(413)
def request_entity_too_large(_error):
    flash('Passport photograph must not exceed 5 MB.')
    return redirect(url_for('gate')), 413


# ─────────────────────────────────────────────
# 5.  Public landing
# ─────────────────────────────────────────────

@app.route('/')
def gate():
    """Public entry point for campaign registration and trustee access."""
    return render_template(
        'gate.html',
        section='gate',
        session=session,
    )


# ─────────────────────────────────────────────
# 6.  Campaign registration  →  /mobilization/register
# ─────────────────────────────────────────────

@app.route('/mobilization/register', methods=['POST'])
def mobilization_register():
    """Campaign registration accepting only fullName/email/pvcNumber/passport."""
    full_name = _normalize_name(request.form.get('fullName') or request.form.get('full_name'))
    email = _normalize_email(request.form.get('email'))
    pvc_number = _normalize_pvc_number(request.form.get('pvcNumber') or request.form.get('pvc_number'))
    passport = request.files.get('passport')
    username = (request.form.get('username') or '').strip()
    password = request.form.get('password', '')
    confirm = request.form.get('confirm_password', '')

    if len(full_name) < 3:
        flash('Full Name is required and must be at least 3 characters.')
        return redirect(url_for('gate'))
    if not _is_valid_email(email):
        flash('Please enter a valid Email Address.')
        return redirect(url_for('gate'))
    if not _is_valid_pvc_number(pvc_number):
        flash('PVC / Voter Identification Number is required and must use only letters, numbers, hyphens, or slashes.')
        return redirect(url_for('gate'))

    if not password or not confirm:
        flash('Password and Confirm Password are required.')
        return redirect(url_for('gate'))

    if password != confirm:
        flash('Passwords do not match. Please check and try again.')
        return redirect(url_for('gate'))

    if len(password) < 8:
        flash('Password must be at least 8 characters long.')
        return redirect(url_for('gate'))

    if not username or len(username) < 3:
        flash('Username is required and must be at least 3 characters.')
        return redirect(url_for('gate'))

    # Check for duplicate username or email
    existing_user = Citizen.query.filter(or_(func.lower(Citizen.email) == email, func.lower(Citizen.username) == username.lower())).first()
    if existing_user:
        # Determine which field conflicts and show a safe message
        if existing_user.username and existing_user.username.lower() == username.lower():
            flash('This username is already in use. Please choose another username.')
        else:
            flash('This email address is already registered. If this is your account, try signing in or use password recovery.')
        try:
            (PASSPORT_UPLOAD_DIR / passport_result).unlink(missing_ok=True)
        except Exception:
            pass
        return redirect(url_for('gate'))

    is_valid_passport, passport_result = _validate_passport_upload(passport)
    if not is_valid_passport:
        flash(passport_result)
        return redirect(url_for('gate'))

    duplicate = Citizen.query.filter(Citizen.reg_type == 'General').filter(
        or_(func.lower(Citizen.email) == email, Citizen.pvc_number == pvc_number)
    ).first()
    if duplicate:
        try:
            (PASSPORT_UPLOAD_DIR / passport_result).unlink(missing_ok=True)
        except OSError:
            pass
        flash('This information has already been registered.')
        return redirect(url_for('gate'))

    now = datetime.utcnow()
    mobilizer = Citizen(
        reg_type='General',
        full_name=full_name,
        email=email,
        username=username,
        pvc_number=pvc_number,
        passport_image=passport_result,
        phone=f'campaign:{secrets.token_hex(12)}',
        password=_hash(password),
        approved=False,
        created_at=now,
        updated_at=now,
    )
    db.session.add(mobilizer)
    db.session.commit()
    _log('REGISTER', f'Campaign registration submitted: {full_name} (id={mobilizer.id})')

    flash('Registration Successful|Your campaign registration and account have been created successfully.')
    return redirect(url_for('registration_success'))


@app.route('/registration/success')
def registration_success():
    return render_template('registration_success.html')


# ─────────────────────────────────────────────
# 7.  Mobilization login  →  /mobilization/login
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Campaign participant login using PVC / Voter Identification Number."""
    if request.method == 'GET':
        return render_template('login.html', session=session)

    username = (request.form.get('username') or '').strip()
    password = request.form.get('password', '')

    if not username or not password:
        flash('Please provide your username and password.')
        return redirect(url_for('login'))

    user = Citizen.query.filter(func.lower(Citizen.username) == username.lower(), Citizen.reg_type == 'General').first()
    if not user or not _verify(user.password, password):
        flash('Invalid username or password.')
        return redirect(url_for('login'))

    if not user.approved:
        flash('Campaign profile pending approval. Contact your board trustee.')
        return redirect(url_for('login'))

    session.clear()
    session['user_type'] = 'campaign'
    session['user_name'] = user.full_name
    session['user_id'] = user.id
    session['approved'] = bool(user.approved)

    _log('LOGIN', f'Campaign login: {user.full_name} (id={user.id})')
    # After successful participant authentication, show a short synchronization
    # screen before landing on the participant dashboard to match the GYS flow.
    return redirect(url_for('participant_sync'))



@app.route('/participant/sync')
def participant_sync():
    """Short synchronization screen shown to authenticated participants
    prior to landing on the full participant dashboard."""
    if session.get('user_type') != 'campaign' or not session.get('user_id'):
        flash('Please log in to continue.')
        return redirect(url_for('login'))

    return render_template(
        'participant_sync.html',
        section='sync',
        session=session,
    )



@app.route('/admin/login', methods=['GET'])
def admin_login():
    """Render the board member/admin login terminal page."""
    return render_template('admin_login.html', session=session)


# ─────────────────────────────────────────────
# 8.  Trustee login  →  /trustee/login
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
# 9.  Authenticated views
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
        return redirect(url_for('admin_login'))

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
        return redirect(url_for('admin_login'))

    citizens = Citizen.query.filter_by(reg_type='General').order_by(Citizen.created_at.desc(), Citizen.id.desc()).all()
    return render_template(
        'admin_dashboard.html',
        section='admin_dashboard',
        session=session,
        citizens=citizens,
    )


# Legacy alias kept so existing nav links (/dashboard) still resolve
@app.route('/dashboard')
def dashboard():
    # Route acts as role-aware dashboard landing.
    if session.get('user_type') == 'trustee':
        return redirect(url_for('admin_dashboard'))

    if session.get('user_type') == 'campaign':
        user = None
        if session.get('user_id'):
            user = Citizen.query.get(session.get('user_id'))
        return render_template(
            'participant_dashboard.html',
            session=session,
            user=user,
        )

    # Default for unauthenticated: send to login
    flash('Please log in to continue.')
    return redirect(url_for('login'))


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


@app.route('/admin/passports/<path:filename>')
def admin_passport(filename):
    if session.get('user_type') != 'trustee':
        abort(404)

    safe_name = secure_filename(filename)
    if safe_name != filename:
        abort(404)

    return send_from_directory(PASSPORT_UPLOAD_DIR, safe_name, as_attachment=False)


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
    prev_type = session.get('user_type')
    session.clear()
    flash('Session closed. Secure node detached.')
    if prev_type == 'campaign':
        return redirect(url_for('login'))
    return redirect(url_for('gate'))


@app.after_request
def set_response_headers(response):
    # Prevent caching of authenticated pages so back-button cannot expose data
    try:
        if session.get('user_type'):
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
    except Exception:
        pass
    return response


# ─────────────────────────────────────────────
# 10.  WSGI entry points
# ─────────────────────────────────────────────

application = app   # Render / gunicorn expects `application`

if __name__ == '__main__':
    app.run(port=8000, debug=True)
