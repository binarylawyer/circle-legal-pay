"""
Vercel Serverless Function Entry Point for Agent-Ledger
This file wraps the Flask app for deployment on Vercel
"""

import sys
import os

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from run import app

# Vercel expects the app to be named 'app' or accessible via handler
# Flask apps are WSGI apps, so we can use them directly
handler = app
