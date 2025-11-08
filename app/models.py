"""
Database Models for Agent-Ledger
"""

import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    is_lawyer = db.Column(db.Boolean, default=False)  # True if user is a lawyer/reviewer
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Relationships
    legal_cases = db.relationship('LegalCase', backref='user', lazy=True)

    def set_password(self, password):
        """Set hashed password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class LegalCase(db.Model):
    """Legal case model tracking the entire A-to-Z workflow"""
    __tablename__ = 'legal_cases'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.String(50), nullable=False)  # WY_DAO_LLC, DE_LLC, UCC1_FILING

    # Status tracking (Step A-J workflow)
    # PENDING_PAYMENT -> PENDING_REVIEW -> IN_PROGRESS -> PENDING_APPROVAL -> COMPLETE
    status = db.Column(db.String(50), default='PENDING_PAYMENT')

    # Form data (stored as JSON string)
    form_data = db.Column(db.Text)  # JSON string of submitted form fields

    # Wallet & Payment Info
    client_wallet_id = db.Column(db.String(100))
    total_price_usdc = db.Column(db.String(50))
    recurring_fee_usdc = db.Column(db.String(50))

    # Payment tracking
    payment_challenge_id = db.Column(db.String(100))  # Circle transfer challenge ID
    escrow_challenge_id = db.Column(db.String(100))   # Escrow to firm transfer ID

    # Document Info
    sharepoint_folder_url = db.Column(db.String(255))
    document_url = db.Column(db.String(255))
    generated_document_path = db.Column(db.String(255))  # Local file path for mock mode

    # Lawyer review
    lawyer_memo = db.Column(db.Text)  # Lawyer's notes/comments
    reviewed_at = db.Column(db.DateTime)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<LegalCase {self.id} - {self.service_id} - {self.status}>'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader"""
    return User.query.get(int(user_id))
