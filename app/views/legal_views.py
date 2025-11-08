"""
Legal Views Blueprint
Implements the full A-to-Z legal service workflow (Steps A-J)
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app import db
from app.models import LegalCase
from app.agents.circle_wallet_agent import CircleWalletAgent
from app.agents.ai_intent_agent import AiIntentAgent
from app.agents.document_agent import DocumentAgent
from app.agents.scheduling_agent import SchedulingAgent
from app.services.legal_factory import LegalFactory
import json
import os
from datetime import datetime

legal_blueprint = Blueprint('legal', __name__)

# Initialize agents (singleton pattern for the demo)
wallet_agent = None
intent_agent = None
doc_agent = None
schedule_agent = None
factory = None


def get_agents():
    """Lazy initialization of agents"""
    global wallet_agent, intent_agent, doc_agent, schedule_agent, factory

    if wallet_agent is None:
        wallet_agent = CircleWalletAgent()
    if intent_agent is None:
        intent_agent = AiIntentAgent()
    if doc_agent is None:
        doc_agent = DocumentAgent()
    if schedule_agent is None:
        schedule_agent = SchedulingAgent(wallet_agent=wallet_agent)
    if factory is None:
        factory = LegalFactory()

    return wallet_agent, intent_agent, doc_agent, schedule_agent, factory


# ============================================================================
# STEP A/B: Order Form & Submission
# ============================================================================

@legal_blueprint.route('/order', methods=['GET'])
@login_required
def order_form():
    """
    Step A/B: Show the order form
    Displays available legal services
    """
    _, _, _, _, factory = get_agents()
    services = list(factory.get_all_services())
    return render_template('legal/order_form.html', services=services)


@legal_blueprint.route('/order', methods=['POST'])
@login_required
def submit_order_form():
    """
    Step A/B: Handle form submission
    Creates a new legal case
    """
    _, _, _, _, factory = get_agents()

    data = request.form.to_dict()
    service_id = data.get('service_id')

    service = factory.get_service(service_id)
    if not service:
        flash("Invalid service selected.", "danger")
        return redirect(url_for('legal.order_form'))

    try:
        # Validate required fields
        factory.validate_fields(service_id, data)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for('legal.order_form'))

    # Step C: Create case and prepare for payment
    # For demo, simulate client wallet creation
    client_wallet_id = f"client_wallet_{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    new_case = LegalCase(
        user_id=current_user.id,
        service_id=service_id,
        status='PENDING_PAYMENT',
        form_data=json.dumps(data),
        client_wallet_id=client_wallet_id,
        total_price_usdc=service['price_usdc'],
        recurring_fee_usdc=service['recurring_fee_usdc']
    )

    db.session.add(new_case)
    db.session.commit()

    flash(f"Order created! Case ID: {new_case.id}. Proceeding to payment...", "success")
    return redirect(url_for('legal.handle_payment', case_id=new_case.id))


@legal_blueprint.route('/order/voice', methods=['POST'])
@login_required
def submit_order_voice():
    """
    Step A/B (Alternative): Handle "Vibe Coder" voice submission
    Uses ElevenLabs + Gemini to extract intent from audio
    """
    wallet_agent, intent_agent, _, _, factory = get_agents()

    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({"error": "No audio file provided"}), 400

    # Extract intent from voice
    form_data = intent_agent.get_intent_from_voice_order(audio_file.read())
    if not form_data:
        return jsonify({"error": "Could not understand audio"}), 400

    service_id = form_data.get('service_id')
    service = factory.get_service(service_id)

    if not service:
        return jsonify({"error": "Invalid service in voice command"}), 400

    try:
        factory.validate_fields(service_id, form_data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Create case
    client_wallet_id = f"client_wallet_{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    new_case = LegalCase(
        user_id=current_user.id,
        service_id=service_id,
        status='PENDING_PAYMENT',
        form_data=json.dumps(form_data),
        client_wallet_id=client_wallet_id,
        total_price_usdc=service['price_usdc'],
        recurring_fee_usdc=service['recurring_fee_usdc']
    )

    db.session.add(new_case)
    db.session.commit()

    return jsonify({
        "success": True,
        "case_id": new_case.id,
        "message": f"Voice order processed! Case {new_case.id} created.",
        "redirect_url": url_for('legal.handle_payment', case_id=new_case.id)
    })


# ============================================================================
# STEP C: Payment & Escrow
# ============================================================================

@legal_blueprint.route('/case/<int:case_id>/pay', methods=['GET', 'POST'])
@login_required
def handle_payment(case_id):
    """
    Step C: Simulate payment and move funds to escrow
    In production, this would integrate with Circle Paymaster
    """
    wallet_agent, _, _, _, _ = get_agents()
    case = LegalCase.query.get_or_404(case_id)

    # Security check
    if case.user_id != current_user.id:
        flash("Unauthorized access", "danger")
        return redirect(url_for('main.index'))

    if request.method == 'GET':
        # Show payment page
        return render_template('legal/payment.html', case=case)

    # POST: Process payment
    # Simulate: Transfer from client wallet to escrow wallet
    escrow_wallet_id = os.environ.get("LAW_FIRM_ESCROW_WALLET_ID", "escrow_wallet_demo")

    challenge_id = wallet_agent.initiate_gasless_transfer(
        from_wallet_id=case.client_wallet_id,
        to_address=escrow_wallet_id,
        amount_usdc=case.total_price_usdc
    )

    if challenge_id:
        case.status = 'PENDING_REVIEW'  # Step D
        case.payment_challenge_id = challenge_id
        db.session.commit()

        flash(f"Payment successful! Case {case.id} is pending lawyer review.", "success")
        return redirect(url_for('legal.lawyer_review_page', case_id=case.id))
    else:
        flash("Payment transfer failed. Please try again.", "danger")
        return redirect(url_for('legal.handle_payment', case_id=case.id))


# ============================================================================
# STEP D/E/F: Lawyer Review & Document Generation
# ============================================================================

@legal_blueprint.route('/review/<int:case_id>', methods=['GET'])
@login_required
def lawyer_review_page(case_id):
    """
    Step D/E/F: Show lawyer the review page
    Lawyer can approve/reject with voice or form
    """
    case = LegalCase.query.get_or_404(case_id)
    form_data = json.loads(case.form_data)

    # In production, add role check: if not current_user.is_lawyer
    return render_template('legal/lawyer_review.html', case=case, form_data=form_data)


@legal_blueprint.route('/review/<int:case_id>/approve', methods=['POST'])
@login_required
def lawyer_approve_case(case_id):
    """
    Step E/F: Lawyer approves case (form-based approval)
    Generates document and uploads to client locker
    """
    _, _, doc_agent, _, factory = get_agents()
    case = LegalCase.query.get_or_404(case_id)

    # Get lawyer's memo
    lawyer_memo = request.form.get('memo', '')

    # Step E: Generate the document
    form_data = json.loads(case.form_data)
    form_data['case_id'] = case.id  # Add case_id for template

    try:
        doc_content, doc_filename = factory.generate_document(case.service_id, form_data)
    except Exception as e:
        flash(f"Error generating document: {e}", "danger")
        return redirect(url_for('legal.lawyer_review_page', case_id=case.id))

    # Step F: Upload to client locker
    doc_url = doc_agent.upload_document(doc_content, doc_filename, case.id)

    if doc_url:
        case.status = 'PENDING_APPROVAL'  # Step G
        case.document_url = doc_url
        case.generated_document_path = doc_url
        case.lawyer_memo = lawyer_memo
        case.reviewed_at = datetime.utcnow()
        db.session.commit()

        flash(f"Case {case.id} approved! Document uploaded. Client notified.", "success")
        return redirect(url_for('legal.client_approval_page', case_id=case.id))
    else:
        flash("Document upload failed.", "danger")
        return redirect(url_for('legal.lawyer_review_page', case_id=case.id))


@legal_blueprint.route('/review/voice', methods=['POST'])
@login_required
def lawyer_submit_review_voice():
    """
    Step D/E/F (Alternative): Handle lawyer's voice approval
    Uses AI to extract "approve/reject" intent
    """
    _, intent_agent, doc_agent, _, factory = get_agents()

    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({"error": "No audio file provided"}), 400

    review_data = intent_agent.get_intent_from_voice_review(audio_file.read())
    if not review_data:
        return jsonify({"error": "Could not understand audio"}), 400

    case_id = review_data.get('case_id')
    case = LegalCase.query.get_or_404(case_id)

    if review_data.get('action') == 'approve':
        # Generate document
        form_data = json.loads(case.form_data)
        form_data['case_id'] = case.id

        doc_content, doc_filename = factory.generate_document(case.service_id, form_data)
        doc_url = doc_agent.upload_document(doc_content, doc_filename, case.id)

        if doc_url:
            case.status = 'PENDING_APPROVAL'
            case.document_url = doc_url
            case.generated_document_path = doc_url
            case.lawyer_memo = review_data.get('memo', '')
            case.reviewed_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                "success": True,
                "message": "Case approved via voice, document uploaded.",
                "redirect_url": url_for('legal.client_approval_page', case_id=case.id)
            })
        else:
            return jsonify({"error": "Document upload failed"}), 500

    elif review_data.get('action') == 'reject':
        case.status = 'REJECTED'
        case.lawyer_memo = review_data.get('memo', 'Rejected by lawyer')
        db.session.commit()
        return jsonify({"success": True, "message": "Case rejected."})

    else:
        return jsonify({"error": "Unknown action"}), 400


# ============================================================================
# STEP G/H: Client Final Approval & Fund Release
# ============================================================================

@legal_blueprint.route('/approve/<int:case_id>', methods=['GET'])
@login_required
def client_approval_page(case_id):
    """
    Step G: Show client the final approval page
    Client reviews the generated document
    """
    case = LegalCase.query.get_or_404(case_id)

    # Security check
    if case.user_id != current_user.id:
        flash("Unauthorized access", "danger")
        return redirect(url_for('main.index'))

    return render_template('legal/client_approval.html', case=case)


@legal_blueprint.route('/approve/<int:case_id>', methods=['POST'])
@login_required
def client_submit_approval(case_id):
    """
    Step H/I/J: Handle client's final approval
    - Release funds from escrow to law firm
    - Schedule recurring fees if applicable
    - Finalize case
    """
    wallet_agent, _, _, schedule_agent, _ = get_agents()
    case = LegalCase.query.get_or_404(case_id)

    # Security check
    if case.user_id != current_user.id:
        flash("Unauthorized access", "danger")
        return redirect(url_for('main.index'))

    # Step H: Release funds from escrow to law firm main wallet
    escrow_wallet_id = os.environ.get("LAW_FIRM_ESCROW_WALLET_ID", "escrow_wallet_demo")
    main_wallet_id = os.environ.get("LAW_FIRM_MAIN_WALLET_ID", "main_wallet_demo")

    challenge_id = wallet_agent.initiate_gasless_transfer(
        from_wallet_id=escrow_wallet_id,
        to_address=main_wallet_id,
        amount_usdc=case.total_price_usdc
    )

    if not challenge_id:
        flash("Fund release failed. Please contact support.", "danger")
        return redirect(url_for('legal.client_approval_page', case_id=case.id))

    case.escrow_challenge_id = challenge_id

    # Step I: Schedule recurring fee if applicable
    if float(case.recurring_fee_usdc) > 0:
        fee_wallet_id = os.environ.get("LAW_FIRM_FEE_WALLET_ID", case.client_wallet_id)
        schedule_agent.schedule_annual_payment(
            case_id=case.id,
            client_fee_wallet_id=fee_wallet_id,
            amount=case.recurring_fee_usdc
        )
        flash(f"Recurring fee of ${case.recurring_fee_usdc} USDC scheduled annually.", "info")

    # Step J: Finalize case
    case.status = 'COMPLETE'
    case.updated_at = datetime.utcnow()
    db.session.commit()

    flash(f"Case {case.id} complete! Funds released and document is yours.", "success")
    return redirect(url_for('legal.case_detail', case_id=case.id))


# ============================================================================
# Additional Routes
# ============================================================================

@legal_blueprint.route('/cases')
@login_required
def my_cases():
    """List all cases for current user"""
    if current_user.is_lawyer:
        # Lawyers see all cases
        cases = LegalCase.query.order_by(LegalCase.created_at.desc()).all()
    else:
        # Clients see only their cases
        cases = LegalCase.query.filter_by(user_id=current_user.id)\
            .order_by(LegalCase.created_at.desc()).all()

    return render_template('legal/cases.html', cases=cases)


@legal_blueprint.route('/case/<int:case_id>')
@login_required
def case_detail(case_id):
    """View case details"""
    case = LegalCase.query.get_or_404(case_id)

    # Security check
    if not current_user.is_lawyer and case.user_id != current_user.id:
        flash("Unauthorized access", "danger")
        return redirect(url_for('main.index'))

    form_data = json.loads(case.form_data) if case.form_data else {}
    return render_template('legal/case_detail.html', case=case, form_data=form_data)


@legal_blueprint.route('/api/status')
def api_status():
    """API status endpoint for demo/testing"""
    wallet_agent, intent_agent, doc_agent, schedule_agent, factory = get_agents()

    return jsonify({
        "status": "operational",
        "agents": {
            "wallet": "initialized" if wallet_agent else "not initialized",
            "intent": "initialized" if intent_agent else "not initialized",
            "document": "initialized" if doc_agent else "not initialized",
            "scheduler": "initialized" if schedule_agent else "not initialized"
        },
        "services": len(factory.services) if factory else 0,
        "mock_mode": os.environ.get('MOCK_MODE', 'True')
    })
