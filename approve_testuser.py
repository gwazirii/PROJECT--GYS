from backend.app import app, db, Citizen

with app.app_context():
    user = Citizen.query.filter_by(username='testuser').first()
    if user:
        user.approved = True
        db.session.commit()
        print('Approved', user.id)
    else:
        print('User not found')
