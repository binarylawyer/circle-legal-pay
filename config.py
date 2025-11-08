import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database - SQLAlchemy will auto-detect SQLite vs Postgres
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///agent_ledger.db'

    # Handle Supabase/Render postgres:// vs postgresql://
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Circle WaaS
    CIRCLE_API_KEY = os.environ.get('CIRCLE_API_KEY')
    CIRCLE_ENTITY_SECRET = os.environ.get('CIRCLE_ENTITY_SECRET')

    # Arc Network
    ARC_RPC_URL = os.environ.get('ARC_RPC_URL', 'https://rpc.testnet.arc.network')
    ARC_CHAIN_ID = os.environ.get('ARC_CHAIN_ID', '5042002')

    # AI Services
    ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

    # MS Graph (Optional)
    MS_TENANT_ID = os.environ.get('MS_TENANT_ID')
    MS_CLIENT_ID = os.environ.get('MS_CLIENT_ID')
    MS_CLIENT_SECRET = os.environ.get('MS_CLIENT_SECRET')
    SHAREPOINT_SITE_ID = os.environ.get('SHAREPOINT_SITE_ID')
    SHAREPOINT_DRIVE_ID = os.environ.get('SHAREPOINT_DRIVE_ID')

    # Law Firm Wallets
    LAW_FIRM_ESCROW_WALLET_ID = os.environ.get('LAW_FIRM_ESCROW_WALLET_ID')
    LAW_FIRM_MAIN_WALLET_ID = os.environ.get('LAW_FIRM_MAIN_WALLET_ID')
    LAW_FIRM_FEE_WALLET_ID = os.environ.get('LAW_FIRM_FEE_WALLET_ID')

    # Mock Mode (for development without real API keys)
    MOCK_MODE = os.environ.get('MOCK_MODE', 'True').lower() in ('true', '1', 'yes')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    MOCK_MODE = False


# Config dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
