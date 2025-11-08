"""
Circle Wallet Agent
Manages Circle Developer-Controlled Wallets and gasless USDC transfers on Arc
"""

import os
import uuid
from web3 import Web3


class CircleWalletAgent:
    """Agent for managing Circle WaaS wallets and transfers"""

    def __init__(self, mock_mode=None):
        """Initialize Circle Wallet Agent"""
        if mock_mode is None:
            mock_mode = os.environ.get('MOCK_MODE', 'True').lower() in ('true', '1', 'yes')

        self.mock_mode = mock_mode
        self.api_key = os.environ.get("CIRCLE_API_KEY")
        self.entity_secret = os.environ.get("CIRCLE_ENTITY_SECRET")
        self.arc_rpc_url = os.environ.get("ARC_RPC_URL", "https://rpc.testnet.arc.network")
        self.arc_chain_id = os.environ.get("ARC_CHAIN_ID", "5042002")

        # Initialize Web3 connection to Arc
        self.w3 = Web3(Web3.HTTPProvider(self.arc_rpc_url))

        # Initialize Circle SDK client (only if not in mock mode and keys exist)
        if not self.mock_mode and self.api_key and self.entity_secret:
            try:
                from circle.web3 import utils, types
                self.client = utils.init_developer_controlled_wallets_client(
                    api_key=self.api_key,
                    entity_secret=self.entity_secret
                )
                self.types = types
                print("✅ Circle SDK initialized successfully")
            except Exception as e:
                print(f"⚠️  Circle SDK initialization failed: {e}")
                print("   Falling back to mock mode")
                self.mock_mode = True
                self.client = None
        else:
            self.client = None
            if not self.mock_mode:
                print("⚠️  Missing Circle API credentials, using mock mode")
                self.mock_mode = True

    def create_wallet(self, user_id):
        """
        Create a new wallet for a user

        Args:
            user_id: The user's ID

        Returns:
            Wallet object or mock wallet data
        """
        if self.mock_mode:
            # Return mock wallet data
            mock_wallet = {
                'id': f'mock_wallet_{user_id}_{uuid.uuid4().hex[:8]}',
                'address': f'0x{uuid.uuid4().hex[:40]}',
                'blockchain': 'ARC-TESTNET',
                'state': 'LIVE'
            }
            print(f"🔧 MOCK: Created wallet {mock_wallet['id']}")
            return [mock_wallet]

        try:
            # Create a WalletSet for the user
            wallet_set_name = f"user_{user_id}_wallet_set"
            wallet_set = self.client.create_wallet_set(name=wallet_set_name)

            # Create a wallet on the Arc Testnet
            response = self.client.create_wallets(
                wallet_set_id=wallet_set.data.wallet_set.id,
                account_type=self.types.AccountType.SCA,
                blockchains=[self.types.Blockchain.ARC_TESTNET],
                count=1
            )
            print(f"✅ Created Circle wallet for user {user_id}")
            return response.data.wallets
        except Exception as e:
            print(f"❌ Error creating Circle wallet: {e}")
            return None

    def initiate_gasless_transfer(self, from_wallet_id, to_address, amount_usdc):
        """
        Initiate a gasless (developer-sponsored) USDC transfer on Arc

        Args:
            from_wallet_id: Source wallet ID
            to_address: Destination wallet address or ID
            amount_usdc: Amount in USDC (as string)

        Returns:
            Challenge ID or None if failed
        """
        if self.mock_mode:
            # Return mock challenge ID
            mock_challenge_id = f'mock_challenge_{uuid.uuid4().hex[:16]}'
            print(f"🔧 MOCK: Transfer ${amount_usdc} USDC")
            print(f"   From: {from_wallet_id}")
            print(f"   To: {to_address}")
            print(f"   Challenge ID: {mock_challenge_id}")
            return mock_challenge_id

        # Arc's native USDC address (system contract)
        token_address = "0x3600000000000000000000000000000000000000"

        try:
            # Determine destination type (wallet ID vs address)
            dest_type = "WALLET" if to_address.startswith("0x") else "WALLET"

            response = self.client.create_transfer(
                source=self.types.WalletLocation(
                    type="WALLET",
                    id=from_wallet_id
                ),
                destination=self.types.DestinationLocation(
                    type=dest_type,
                    address=to_address if to_address.startswith("0x") else None,
                    id=to_address if not to_address.startswith("0x") else None,
                    chain=self.arc_chain_id
                ),
                amount=self.types.Money(
                    amount=str(amount_usdc),
                    currency="USD"
                ),
                fee_level=self.types.FeeLevel.MEDIUM,  # Gas is sponsored by developer
                idempotency_key=str(uuid.uuid4())
            )

            challenge_id = response.data.challenge_id
            print(f"✅ Transfer initiated: {challenge_id}")
            return challenge_id

        except Exception as e:
            print(f"❌ Error initiating Circle transfer: {e}")
            return None

    def get_wallet_balance(self, wallet_id):
        """Get wallet balance (mock for now)"""
        if self.mock_mode:
            return {
                'wallet_id': wallet_id,
                'balance': '1000.00',
                'currency': 'USDC'
            }

        # TODO: Implement real Circle balance check
        return None

    def check_arc_connection(self):
        """Check if connected to Arc network"""
        try:
            is_connected = self.w3.is_connected()
            if is_connected:
                print(f"✅ Connected to Arc Testnet: {self.arc_rpc_url}")
            return is_connected
        except Exception as e:
            print(f"❌ Arc connection error: {e}")
            return False
