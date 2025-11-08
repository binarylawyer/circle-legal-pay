"""
AI Intent Agent
Uses ElevenLabs STT and Google Gemini for structured intent extraction
"""

import os
import json
from pydantic import BaseModel, Field
from typing import Optional, Literal


# Pydantic Schemas for Intent Extraction
class OrderService(BaseModel):
    """Schema for ordering a legal service"""
    service_id: Literal["WY_DAO_LLC", "DE_LLC", "UCC1_FILING"] = Field(
        description="The ID of the legal service to order"
    )
    entity_name: Optional[str] = Field(
        default=None,
        description="The name of the company, DAO, or LLC"
    )
    smart_contract_identifier: Optional[str] = Field(
        default=None,
        description="The public smart contract address for a DAO"
    )
    registered_agent_name: Optional[str] = Field(
        default=None,
        description="Name of the registered agent"
    )
    registered_agent_address: Optional[str] = Field(
        default=None,
        description="Address of the registered agent"
    )
    management_statement: Optional[str] = Field(
        default=None,
        description="Management structure (member-managed or algorithmically managed)"
    )
    # DE LLC fields
    authorized_person_name: Optional[str] = Field(
        default=None,
        description="Name of authorized person for Delaware LLC"
    )
    # UCC-1 fields
    debtor_name: Optional[str] = Field(
        default=None,
        description="Legal name of the debtor"
    )
    secured_party_name: Optional[str] = Field(
        default=None,
        description="Name of the secured party/creditor"
    )
    collateral_description: Optional[str] = Field(
        default=None,
        description="Description of collateral"
    )


class ReviewTask(BaseModel):
    """Schema for lawyer review actions"""
    action: Literal["approve", "reject", "comment"] = Field(
        description="The action the lawyer is taking"
    )
    case_id: int = Field(
        description="The unique case ID being reviewed"
    )
    memo: Optional[str] = Field(
        default=None,
        description="The lawyer's comments or suggestions for the client"
    )


class AiIntentAgent:
    """Agent for AI-powered intent extraction from voice or text"""

    def __init__(self, mock_mode=None):
        """Initialize AI Intent Agent"""
        if mock_mode is None:
            mock_mode = os.environ.get('MOCK_MODE', 'True').lower() in ('true', '1', 'yes')

        self.mock_mode = mock_mode
        self.elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")
        self.gemini_key = os.environ.get("GEMINI_API_KEY")

        # Initialize ElevenLabs client
        if not self.mock_mode and self.elevenlabs_key:
            try:
                from elevenlabs.client import ElevenLabs
                self.eleven_client = ElevenLabs(api_key=self.elevenlabs_key)
                print("✅ ElevenLabs initialized")
            except Exception as e:
                print(f"⚠️  ElevenLabs initialization failed: {e}")
                self.mock_mode = True
                self.eleven_client = None
        else:
            self.eleven_client = None
            if not self.mock_mode:
                print("⚠️  Missing ElevenLabs API key, using mock mode")
                self.mock_mode = True

        # Initialize Gemini client
        if not self.mock_mode and self.gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_key)
                self.gemini_model = genai.GenerativeModel(
                    'gemini-1.5-pro-latest',
                    generation_config={"response_mime_type": "application/json"}
                )
                print("✅ Google Gemini initialized")
            except Exception as e:
                print(f"⚠️  Gemini initialization failed: {e}")
                self.mock_mode = True
                self.gemini_model = None
        else:
            self.gemini_model = None
            if not self.mock_mode:
                print("⚠️  Missing Gemini API key, using mock mode")
                self.mock_mode = True

    def transcribe_audio(self, audio_file_bytes):
        """
        Transcribe audio to text using ElevenLabs STT

        Args:
            audio_file_bytes: Audio file as bytes

        Returns:
            Transcribed text or None
        """
        if self.mock_mode:
            print("🔧 MOCK: Transcribing audio...")
            return "I need to form a Wyoming DAO called 'DeFi Collective DAO' with smart contract at 0x1234567890abcdef"

        try:
            response = self.eleven_client.speech_to_text.convert(audio=audio_file_bytes)
            transcript = response.text
            print(f"✅ Transcribed: {transcript}")
            return transcript
        except Exception as e:
            print(f"❌ ElevenLabs STT Error: {e}")
            return None

    def _extract_json(self, transcript, schema_description):
        """
        Extract structured JSON from transcript using Gemini

        Args:
            transcript: Text to analyze
            schema_description: Description of expected JSON schema

        Returns:
            Parsed JSON dict or None
        """
        if self.mock_mode:
            print(f"🔧 MOCK: Extracting intent from: {transcript}")
            # Return mock structured data
            if "wyoming" in transcript.lower() or "dao" in transcript.lower():
                return {
                    "service_id": "WY_DAO_LLC",
                    "entity_name": "DeFi Collective DAO LLC",
                    "smart_contract_identifier": "0x1234567890abcdef",
                    "registered_agent_name": "Wyoming Registered Agent Services",
                    "registered_agent_address": "123 Capitol Ave, Cheyenne, WY 82001",
                    "management_statement": "This DAO is algorithmically managed via smart contract governance"
                }
            return None

        try:
            prompt = f"""
Extract the user's intent from this transcript into valid JSON matching this schema:
{schema_description}

Transcript: {transcript}

Return ONLY valid JSON, no additional text.
"""

            response = self.gemini_model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )

            result = json.loads(response.text)
            print(f"✅ Extracted intent: {result}")
            return result

        except Exception as e:
            print(f"❌ Gemini Extraction Error: {e}")
            return None

    def get_intent_from_voice_order(self, audio_file_bytes):
        """
        Extract order intent from voice audio

        Args:
            audio_file_bytes: Audio file bytes

        Returns:
            Dict with extracted order data or None
        """
        # Step 1: Transcribe
        transcript = self.transcribe_audio(audio_file_bytes)
        if not transcript:
            return None

        # Step 2: Extract structured data
        schema_desc = OrderService.schema_json(indent=2)
        return self._extract_json(transcript, schema_desc)

    def get_intent_from_text_order(self, text):
        """
        Extract order intent from text (alternative to voice)

        Args:
            text: User's text input

        Returns:
            Dict with extracted order data or None
        """
        schema_desc = OrderService.schema_json(indent=2)
        return self._extract_json(text, schema_desc)

    def get_intent_from_voice_review(self, audio_file_bytes):
        """
        Extract review intent from lawyer's voice

        Args:
            audio_file_bytes: Audio file bytes

        Returns:
            Dict with review action or None
        """
        transcript = self.transcribe_audio(audio_file_bytes)
        if not transcript:
            return None

        schema_desc = ReviewTask.schema_json(indent=2)
        return self._extract_json(transcript, schema_desc)

    def get_intent_from_text_review(self, text):
        """
        Extract review intent from lawyer's text

        Args:
            text: Lawyer's text input

        Returns:
            Dict with review action or None
        """
        schema_desc = ReviewTask.schema_json(indent=2)
        return self._extract_json(text, schema_desc)
