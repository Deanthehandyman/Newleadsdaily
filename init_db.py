#!/usr/bin/env python3
"""
Initialize the database and create the first "Dean" user.
Run this ONCE when you first download the project.
"""

from app import app, db, User
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created!")
        
        # Check if Dean user already exists
        dean = User.query.filter_by(email='dean@deanshandymanservice.me').first()
        if dean:
            print("✓ Dean user already exists.")
            return
        
        # Create Dean user with default location (Pittsburg, TX)
        print("Creating Dean user...")
        dean = User(
            name='Dean',
            email='dean@deanshandymanservice.me',
            password_hash=generate_password_hash('changeme'),  # Change this password!
            home_lat=32.9954,
            home_lng=-94.9652,
            is_handyman=True,
            is_starlink=True,
            is_smarthome=True,
            max_radius_km=100
        )
        db.session.add(dean)
        db.session.commit()
        print("✓ Dean user created!")
        print("\nDEFAULT LOGIN:")
        print("  Email: dean@deanshandymanservice.me")
        print("  Password: changeme")
        print("\n⚠️  IMPORTANT: Change your password in /settings after first login!")

if __name__ == '__main__':
    init_database()
    print("\n✅ Database initialization complete!")
    print("\nNow run: python app.py")
    print("Then open: http://localhost:5000/login")
