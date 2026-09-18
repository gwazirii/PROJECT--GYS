import os
import tempfile
from pathlib import Path
from unittest import TestCase

TEST_DB_PATH = Path(tempfile.mkdtemp()) / 'gys_test.sqlite3'
os.environ['DATABASE_URL'] = f'sqlite:///{TEST_DB_PATH}'

from backend.app import app, db, Citizen


class ParticipantAuthSafeTests(TestCase):
    def setUp(self):
        self.app = app
        self.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False, SQLALCHEMY_DATABASE_URI=f'sqlite:///{TEST_DB_PATH}')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
        self.synthetic_pvcs = []

    def tearDown(self):
        with self.app.app_context():
            if self.synthetic_pvcs:
                db.session.query(Citizen).filter(Citizen.pvc_number.in_(self.synthetic_pvcs)).delete(synchronize_session=False)
                db.session.commit()

    def _synthetic_pvc(self, label):
        pvc = f'TESTPVC-{label}'
        self.synthetic_pvcs.append(pvc)
        return pvc

    def _valid_passport_bytes(self):
        return b'\x89PNG\r\n\x1a\n' + b'1234567890'

    def _register_payload(self, pvc, password='Pass1234!'):
        return {
            'fullName': 'Synthetic Test User',
            'email': f'{pvc.lower()}@example.test',
            'pvcNumber': pvc,
            'username': pvc,
            'password': password,
            'confirm_password': password,
            'passport': (self._valid_passport_bytes(), 'passport.png'),
        }

    def _seed_participant(self, pvc, password='Pass1234!', approved=True):
        user = Citizen(
            full_name='Synthetic Test User',
            phone=f'synthetic-{pvc.lower()}@test',
            username=pvc,
            reg_type='General',
            password=__import__('werkzeug.security').security.generate_password_hash(password),
            pvc_number=pvc,
            email=f'{pvc.lower()}@example.test',
            approved=approved,
        )
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
        return user

    def test_participant_registration_with_synthetic_test_pvc(self):
        pvc = self._synthetic_pvc('REG-001')
        response = self.client.post(
            '/mobilization/register',
            data=self._register_payload(pvc),
            content_type='multipart/form-data',
            follow_redirects=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn('/registration/success', response.headers.get('Location', ''))

        with self.app.app_context():
            stored = Citizen.query.filter_by(pvc_number=pvc).first()
            self.assertIsNotNone(stored)
            self.assertNotEqual(stored.password, 'Pass1234!')
            self.assertTrue(stored.password.startswith('pbkdf2:sha256'))

    def test_duplicate_pvc_registration_is_rejected(self):
        pvc = self._synthetic_pvc('DUP-002')
        payload = self._register_payload(pvc)

        first = self.client.post('/mobilization/register', data=payload, content_type='multipart/form-data', follow_redirects=False)
        second = self.client.post('/mobilization/register', data=payload, content_type='multipart/form-data', follow_redirects=False)

        self.assertEqual(first.status_code, 302)
        self.assertEqual(second.status_code, 302)

        with self.app.app_context():
            count = Citizen.query.filter_by(pvc_number=pvc).count()
            self.assertEqual(count, 1)

    def test_successful_login_with_pvc_or_username_and_password(self):
        pvc = self._synthetic_pvc('LOGIN-003')
        self._seed_participant(pvc, approved=True)

        response = self.client.post('/login', data={'username': pvc, 'password': 'Pass1234!'}, follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/participant/sync', response.headers.get('Location', ''))

        with self.client.session_transaction() as session:
            self.assertEqual(session.get('user_type'), 'campaign')
            self.assertEqual(session.get('user_id'), Citizen.query.filter_by(pvc_number=pvc).first().id)

    def test_failed_login_is_rejected(self):
        pvc = self._synthetic_pvc('LOGIN-FAIL-004')
        self._seed_participant(pvc, approved=True)

        response = self.client.post('/login', data={'username': pvc, 'password': 'WrongPassword'}, follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers.get('Location', ''))

        with self.client.session_transaction() as session:
            self.assertNotIn('user_type', session)

    def test_protected_dashboard_requires_login(self):
        response = self.client.get('/dashboard', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers.get('Location', ''))

        pvc = self._synthetic_pvc('DASH-005')
        self._seed_participant(pvc, approved=True)

        with self.client.session_transaction() as session:
            session['user_type'] = 'campaign'
            session['user_id'] = Citizen.query.filter_by(pvc_number=pvc).first().id
            session['user_name'] = 'Synthetic Test User'
            session['approved'] = True

        dashboard_response = self.client.get('/dashboard')
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertIn('My Account', dashboard_response.get_data(as_text=True))

    def test_logout_clears_session(self):
        pvc = self._synthetic_pvc('LOGOUT-006')
        self._seed_participant(pvc, approved=True)

        with self.client.session_transaction() as session:
            session['user_type'] = 'campaign'
            session['user_id'] = Citizen.query.filter_by(pvc_number=pvc).first().id
            session['user_name'] = 'Synthetic Test User'
            session['approved'] = True

        response = self.client.get('/logout', follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers.get('Location', ''))

        with self.client.session_transaction() as session:
            self.assertNotIn('user_type', session)
            self.assertNotIn('user_id', session)
