#!/usr/bin/env python3
"""
Agent-Ledger: AI-Powered Legal Services Platform
Built for the "AI Agents on Arc with USDC" Hackathon
"""

import os
from app import create_app, db
from app.models import User, LegalCase

# Create Flask application
app = create_app(os.getenv('FLASK_ENV') or 'development')

# Flask shell context
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'LegalCase': LegalCase
    }

# Initialize database
with app.app_context():
    db.create_all()
    print("✅ Database initialized successfully")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
