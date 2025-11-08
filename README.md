# Agent-Ledger: AI-Powered Legal Services Platform

**Built for the "AI Agents on Arc with USDC" Hackathon**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Arc](https://img.shields.io/badge/Arc-Testnet-purple.svg)](https://docs.arc.network/)
[![Circle](https://img.shields.io/badge/Circle-WaaS-orange.svg)](https://developers.circle.com/)

---

## 🎯 Executive Summary

**Agent-Ledger** is the first AI-powered, ethically-compliant legal services platform built on USDC-native blockchain infrastructure. We solve a $1 trillion problem: **the legal industry is locked out of Web3 because cryptocurrency payments trigger complex ethical rules due to volatility**.

### The Innovation

By using **Arc's USDC-native gas** + **Circle Paymaster** + **AI agents**, we eliminate volatility from the *entire* payment stack, creating the first compliant on-chain payment rail for legal services.

### Core Features

- 🤖 **AI-Powered Document Generation** (ElevenLabs + Google Gemini)
- 💰 **Gasless USDC Payments** (Circle Paymaster on Arc Testnet)
- 📄 **Deterministic Legal Templates** (Wyoming DAO LLC, Delaware LLC, UCC-1)
- 🔒 **Secure Document Storage** (Local/SharePoint integration)
- 📅 **Automated Recurring Payments** (APScheduler for annual fees)
- 🎙️ **Voice Interface** ("Vibe Coder" - order via speech)

---

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │ (Web UI or Voice)
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│         Flask Application (Python)           │
│  ┌───────────────────────────────────────┐  │
│  │  AI Agents Layer                      │  │
│  │  • Circle Wallet Agent (WaaS)         │  │
│  │  • AI Intent Agent (Gemini)           │  │
│  │  • Document Agent (SharePoint/Local)  │  │
│  │  • Scheduling Agent (APScheduler)     │  │
│  └───────────────────────────────────────┘  │
│  ┌───────────────────────────────────────┐  │
│  │  Legal Service Factory                │  │
│  │  • services.json (Config)             │  │
│  │  • Templates (WY DAO, DE LLC, UCC-1)  │  │
│  └───────────────────────────────────────┘  │
│  ┌───────────────────────────────────────┐  │
│  │  Database (SQLAlchemy)                │  │
│  │  • Users                              │  │
│  │  • Legal Cases (Workflow tracking)    │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│  Blockchain Layer (Arc Testnet)             │
│  • Native USDC Gas                          │
│  • Circle Developer-Controlled Wallets      │
│  • Gasless Transactions (Paymaster)         │
└─────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Git
- (Optional) API keys for Circle, Gemini, ElevenLabs

### Installation

```bash
# 1. Clone the repository
cd circle-legal-pay

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your API keys (or leave MOCK_MODE=True for demo)

# 5. Initialize database
python run.py  # This will auto-create the database

# 6. Run the application
python run.py
```

The app will be available at **http://localhost:5000**

---

## 🔑 API Keys Setup

### Required for Full Functionality

1. **Circle API Keys** (https://console.circle.com/)
   - `CIRCLE_API_KEY`
   - `CIRCLE_ENTITY_SECRET`
   - Create wallets via Circle Dashboard and add IDs to `.env`

2. **Google Gemini API** (https://ai.google.dev/)
   - `GEMINI_API_KEY`

3. **ElevenLabs API** (https://elevenlabs.io/)
   - `ELEVENLABS_API_KEY`

### Optional (Will use mock/local storage)

4. **Microsoft Graph (SharePoint)**
   - `MS_TENANT_ID`, `MS_CLIENT_ID`, `MS_CLIENT_SECRET`
   - `SHAREPOINT_SITE_ID`, `SHAREPOINT_DRIVE_ID`

### Demo Mode

To run without API keys, set `MOCK_MODE=True` in `.env`. The app will use simulated responses.

---

## 📖 User Guide

### The A-to-Z Legal Services Flow

#### **For Clients:**

1. **Register/Login** → Create an account
2. **Order Service** → Choose Wyoming DAO LLC, Delaware LLC, or UCC-1
3. **Submit Form** → Fill in required fields (or use voice input)
4. **Pay in USDC** → Gasless payment via Circle Paymaster on Arc
5. **Wait for Review** → Lawyer reviews AI-generated draft
6. **Approve Document** → Review final document and approve
7. **Complete** → Receive document, funds released, case closed

#### **For Lawyers:**

1. **Register as Lawyer** → Check "I am a lawyer" during registration
2. **View Pending Cases** → See all cases awaiting review
3. **Review Submission** → AI has pre-validated and drafted document
4. **Approve/Reject** → Use form or voice command
5. **Document Generated** → AI creates final document from template
6. **Client Notified** → Client receives notification to approve

---

## 🎤 Voice Interface ("Vibe Coder")

### Order via Voice

```javascript
// Example voice command:
"I need to form a Wyoming DAO called 'DeFi Collective DAO LLC' with smart contract at 0x1234..."

// The AI extracts:
{
  "service_id": "WY_DAO_LLC",
  "entity_name": "DeFi Collective DAO LLC",
  "smart_contract_identifier": "0x1234...",
  // ... other fields
}
```

### Lawyer Voice Approval

```javascript
// Example voice command:
"Approve case 123, looks good"

// The AI extracts:
{
  "action": "approve",
  "case_id": 123,
  "memo": "looks good"
}
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Python Flask | Web application framework |
| **Database** | SQLAlchemy (SQLite/Postgres) | ORM and data persistence |
| **Blockchain** | Arc Testnet | USDC-native gas blockchain |
| **Wallets** | Circle WaaS | Developer-controlled wallets |
| **Gas Sponsorship** | Circle Paymaster | Gasless client transactions |
| **Voice I/O** | ElevenLabs | Speech-to-Text |
| **AI Agent** | Google Gemini | Intent extraction & structuring |
| **Document Storage** | Local Files / SharePoint | Secure document lockers |
| **Scheduling** | APScheduler | Recurring fee automation |
| **Frontend** | Bootstrap 5 | Responsive UI |

---

## 📁 Project Structure

```
circle-legal-pay/
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── models.py                   # User & LegalCase models
│   ├── agents/                     # AI Agent modules
│   │   ├── circle_wallet_agent.py  # Circle WaaS integration
│   │   ├── ai_intent_agent.py      # ElevenLabs + Gemini
│   │   ├── document_agent.py       # SharePoint/local storage
│   │   └── scheduling_agent.py     # Recurring payments
│   ├── services/                   # Legal Service Factory
│   │   ├── legal_factory.py        # Document generation logic
│   │   ├── services.json           # Service definitions
│   │   └── templates/              # Legal document templates
│   │       ├── wy_dao_llc.txt
│   │       ├── de_llc.txt
│   │       └── ucc1_filing.txt
│   ├── views/                      # Flask routes/blueprints
│   │   ├── main_views.py           # Auth, home, etc.
│   │   └── legal_views.py          # Full A-to-Z workflow
│   └── templates/                  # HTML templates
│       ├── layout.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       └── legal/
│           ├── order_form.html
│           ├── payment.html
│           ├── lawyer_review.html
│           ├── client_approval.html
│           ├── cases.html
│           └── case_detail.html
├── config.py                       # Configuration
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (create from .env.example)
├── .env.example                    # Template for environment variables
├── PITCH_SCRIPT.md                 # Hackathon pitch script
└── README.md                       # This file
```

---

## 🧪 Testing the Demo

### Create Test Users

```bash
# Start Python shell
python

>>> from app import create_app, db
>>> from app.models import User
>>> app = create_app()
>>> with app.app_context():
...     # Create a client
...     client = User(username="client1", email="client@example.com", is_lawyer=False)
...     client.set_password("password123")
...     db.session.add(client)
...
...     # Create a lawyer
...     lawyer = User(username="lawyer1", email="lawyer@example.com", is_lawyer=True)
...     lawyer.set_password("password123")
...     db.session.add(lawyer)
...
...     db.session.commit()
...     print("✅ Test users created!")
```

### Test Workflow

1. Login as **client1** → Order a Wyoming DAO LLC
2. Submit payment (mock transfer happens)
3. Logout and login as **lawyer1**
4. Review and approve the case
5. Logout and login as **client1**
6. Approve the final document
7. View completed case with generated document

---

## 🌐 Arc Testnet Integration

### Network Details

| Property | Value |
|----------|-------|
| Network Name | Arc Testnet |
| Chain ID | 5042002 |
| RPC URL | https://rpc.testnet.arc.network |
| Block Explorer | https://testnet.arcscan.app |
| Native Currency | USDC |
| Faucet | https://faucet.circle.com/ |

### Get Testnet USDC

1. Visit https://faucet.circle.com/
2. Connect your wallet or enter an address
3. Request testnet USDC for Arc Testnet

---

## 🎓 Legal Services Offered

### 1. Wyoming DAO LLC ($1,000 USDC)

- Compliant with W.S. 17-31-101 (DAO Supplement)
- Smart contract integration required
- On-chain governance recognition
- Annual compliance: $300/year

### 2. Delaware LLC ($150 USDC)

- Standard Certificate of Formation
- Registered agent included
- Gold standard for US entities
- Annual franchise tax: $300/year

### 3. UCC-1 Financing Statement ($100 USDC)

- Uniform Commercial Code Article 9
- Perfects security interests
- 5-year validity
- No recurring fees

---

## 🏆 Hackathon Submission

### Judging Criteria Alignment

| Criterion | Our Solution |
|-----------|--------------|
| **Application of Technology** | Circle WaaS + Arc USDC-native gas + ElevenLabs + Gemini = complete sponsor stack integration |
| **Business Value** | Solves ethical compliance blocker for $1T legal industry |
| **Originality** | First platform to eliminate volatility from *entire* payment stack (payment + gas) |

---

## 📚 Further Reading

- [Arc Network Documentation](https://docs.arc.network/)
- [Circle Developer Docs](https://developers.circle.com/)
- [Wyoming DAO Law (W.S. 17-31-101)](https://sos.wyo.gov/Business/Docs/DAOs_FAQs.pdf)
- [NYSBA Opinion 2019-5 (Crypto Payments)](https://www.nycbar.org/reports/formal-opinion-2019-5)

---

## 📄 License

MIT License

---

## 🙏 Acknowledgments

- **Circle** for pioneering USDC-native blockchain infrastructure
- **Arc Network** for solving the volatility problem at the protocol level
- **ElevenLabs** for democratizing voice AI
- **Google Gemini** for powerful intent extraction
- **Lablab.ai** for hosting an incredible hackathon

---

**Built for the On-Chain Economy. Powered by USDC. Compliant by Design.**
