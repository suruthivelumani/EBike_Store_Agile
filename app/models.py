from flask_login import UserMixin
from app import db
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    
    test_rides = relationship('TestRide', back_populates='user')
    services = relationship('Service', back_populates='user')
    feedbacks = relationship('Feedback', back_populates='user')
    
class TestRide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bike_model = db.Column(db.String(50), nullable=False)
    preferred_date = db.Column(db.Date, nullable=False)
    preferred_time = db.Column(db.Time, nullable=False)
    additional_comments = db.Column(db.Text)

    # Define a relationship to the User model
    user = relationship('User', back_populates='test_rides')

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bike_model = db.Column(db.String(50), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    scheduled_date = db.Column(db.Date, nullable=False)
    scheduled_time = db.Column(db.Time, nullable=False)
    additional_complaints = db.Column(db.Text)

    # Define a relationship to the User model
    user = relationship('User', back_populates='services')
    
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Define a relationship to the User model
    user = relationship('User', back_populates='feedbacks')

    



