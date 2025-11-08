"""
Scheduling Agent
Manages recurring payments using APScheduler
"""

import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime


class SchedulingAgent:
    """Agent for scheduling recurring fee payments"""

    def __init__(self, wallet_agent=None):
        """
        Initialize Scheduling Agent

        Args:
            wallet_agent: CircleWalletAgent instance for executing payments
        """
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.wallet_agent = wallet_agent
        self.law_firm_main_wallet = os.environ.get("LAW_FIRM_MAIN_WALLET_ID")

        print("✅ Scheduling Agent initialized")

    def _execute_annual_payment(self, case_id, client_fee_wallet_id, amount):
        """
        Execute a scheduled annual payment

        Args:
            case_id: The case ID
            client_fee_wallet_id: Source wallet (client's fee wallet)
            amount: Amount in USDC
        """
        print(f"⏰ Executing scheduled annual payment for Case {case_id}...")
        print(f"   Amount: ${amount} USDC")
        print(f"   From: {client_fee_wallet_id}")
        print(f"   To: {self.law_firm_main_wallet}")

        if self.wallet_agent:
            try:
                challenge_id = self.wallet_agent.initiate_gasless_transfer(
                    from_wallet_id=client_fee_wallet_id,
                    to_address=self.law_firm_main_wallet,
                    amount_usdc=amount
                )

                if challenge_id:
                    print(f"✅ Scheduled payment submitted. Challenge ID: {challenge_id}")
                else:
                    print(f"❌ Scheduled payment failed for Case {case_id}")

            except Exception as e:
                print(f"❌ Error executing scheduled payment: {e}")
        else:
            print("⚠️  No wallet agent configured, payment not executed")

    def schedule_annual_payment(self, case_id, client_fee_wallet_id, amount):
        """
        Schedule a recurring annual payment

        Args:
            case_id: The case ID
            client_fee_wallet_id: Source wallet ID
            amount: Amount in USDC

        Returns:
            Job ID
        """
        job_id = f"case_{case_id}_annual_fee"

        # Schedule job to run once per year (365 days)
        self.scheduler.add_job(
            self._execute_annual_payment,
            trigger=IntervalTrigger(days=365),
            id=job_id,
            replace_existing=True,
            args=[case_id, client_fee_wallet_id, amount],
            next_run_time=datetime.now()  # First payment happens immediately for demo
        )

        print(f"📅 Job {job_id} scheduled: ${amount} USDC annual fee")
        return job_id

    def cancel_scheduled_payment(self, case_id):
        """Cancel a scheduled payment"""
        job_id = f"case_{case_id}_annual_fee"

        try:
            self.scheduler.remove_job(job_id)
            print(f"🗑️  Cancelled scheduled payment for Case {case_id}")
            return True
        except Exception as e:
            print(f"⚠️  Could not cancel job {job_id}: {e}")
            return False

    def get_scheduled_jobs(self):
        """Get all scheduled jobs"""
        jobs = self.scheduler.get_jobs()
        return [
            {
                'id': job.id,
                'next_run': job.next_run_time,
                'trigger': str(job.trigger)
            }
            for job in jobs
        ]

    def shutdown(self):
        """Shutdown the scheduler"""
        self.scheduler.shutdown()
        print("⏹️  Scheduler shut down")
