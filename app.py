import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newleadsdaily.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ============ MODELS ============

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    home_lat = db.Column(db.Float, default=32.9954)
    home_lng = db.Column(db.Float, default=-94.9652)
    is_handyman = db.Column(db.Boolean, default=True)
    is_starlink = db.Column(db.Boolean, default=True)
    is_smarthome = db.Column(db.Boolean, default=True)
    max_radius_km = db.Column(db.Integer, default=50)
    user_leads = db.relationship('UserLead', backref='user', lazy=True)

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), default='manual')
    external_id = db.Column(db.String(100))
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(255))
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    is_handyman = db.Column(db.Boolean, default=False)
    is_starlink = db.Column(db.Boolean, default=False)
    is_smarthome = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_leads = db.relationship('UserLead', backref='lead', lazy=True)

class UserLead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=False)
    status = db.Column(db.String(50), default='new')  # new, contacted, not_interested, won, lost
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============ HELPERS ============

def haversine(lat1, lng1, lat2, lng2):
    """Calculate distance in km between two lat/lng points."""
    R = 6371  # Earth's radius in km
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def get_leads_for_user(user, count=10):
    """Get the next unseen leads for a user, ordered by distance."""
    # Get all lead IDs already seen by this user
    seen_lead_ids = db.session.query(UserLead.lead_id).filter_by(user_id=user.id).all()
    seen_lead_ids = [x[0] for x in seen_lead_ids]
    
    # Get all unseen leads
    unseen_leads = Lead.query.filter(
        Lead.id.notin_(seen_lead_ids)
    ).all()
    
    # Filter by service type
    filtered_leads = []
    for lead in unseen_leads:
        if (user.is_handyman and lead.is_handyman) or \
           (user.is_starlink and lead.is_starlink) or \
           (user.is_smarthome and lead.is_smarthome):
            filtered_leads.append(lead)
    
    # Calculate distance and sort
    leads_with_distance = []
    for lead in filtered_leads:
        dist = haversine(user.home_lat, user.home_lng, lead.lat, lead.lng)
        if dist <= user.max_radius_km:
            leads_with_distance.append((lead, dist))
    
    # Sort by distance, then by created_at (newest first)
    leads_with_distance.sort(key=lambda x: (x[1], -x[0].created_at.timestamp()))
    
    # Return top 'count' leads and mark them as seen
    result = []
    for lead, dist in leads_with_distance[:count]:
        user_lead = UserLead(user_id=user.id, lead_id=lead.id)
        db.session.add(user_lead)
        result.append((lead, dist))
    
    db.session.commit()
    return result

# ============ ROUTES ============

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    leads_with_dist = get_leads_for_user(current_user, count=10)
    return render_template('dashboard.html', leads=leads_with_dist)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        current_user.max_radius_km = int(request.form.get('max_radius_km', 50))
        current_user.is_handyman = 'is_handyman' in request.form
        current_user.is_starlink = 'is_starlink' in request.form
        current_user.is_smarthome = 'is_smarthome' in request.form
        db.session.commit()
        return redirect(url_for('settings'))
    return render_template('settings.html', user=current_user)

@app.route('/admin/add-lead', methods=['GET', 'POST'])
@login_required
def add_lead():
    if request.method == 'POST':
        lead = Lead(
            name=request.form.get('name'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            address=request.form.get('address'),
            lat=float(request.form.get('lat')),
            lng=float(request.form.get('lng')),
            is_handyman='is_handyman' in request.form,
            is_starlink='is_starlink' in request.form,
            is_smarthome='is_smarthome' in request.form,
            source='manual'
        )
        db.session.add(lead)
        db.session.commit()
        return redirect(url_for('add_lead'))
    return render_template('add_lead.html')

@app.route('/lead/<int:lead_id>/status', methods=['POST'])
@login_required
def update_lead_status(lead_id):
    status = request.form.get('status')
    user_lead = UserLead.query.filter_by(user_id=current_user.id, lead_id=lead_id).first()
    if user_lead:
        user_lead.status = status
        db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
