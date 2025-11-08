"""
Legal Service Factory
Generates deterministic legal documents from templates and structured data
"""

import json
import os
from datetime import datetime


class LegalFactory:
    """Factory class for legal document generation"""

    def __init__(self):
        """Load service definitions from services.json"""
        services_path = os.path.join(os.path.dirname(__file__), 'services.json')
        with open(services_path, 'r') as f:
            services_list = json.load(f)
            self.services = {s['id']: s for s in services_list}

    def get_service(self, service_id):
        """Get service definition by ID"""
        return self.services.get(service_id)

    def get_all_services(self):
        """Get all available services"""
        return self.services.values()

    def validate_fields(self, service_id, data):
        """
        Validate that all required fields are present in the data
        Raises ValueError if validation fails
        """
        service = self.get_service(service_id)
        if not service:
            raise ValueError(f"Service '{service_id}' not found")

        missing_fields = [
            field for field in service['required_fields']
            if field not in data or not data[field]
        ]

        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        return True

    def generate_document(self, service_id, data):
        """
        Generate a legal document from a template and data

        Args:
            service_id: The service ID (e.g., 'WY_DAO_LLC')
            data: Dictionary containing all required fields

        Returns:
            Tuple of (document_content, filename)
        """
        service = self.get_service(service_id)
        if not service:
            raise ValueError(f"Service '{service_id}' not found")

        # Validate required fields
        self.validate_fields(service_id, data)

        # Load template
        template_path = os.path.join(
            os.path.dirname(__file__),
            'templates',
            service['template_file']
        )

        with open(template_path, 'r') as f:
            template_content = f.read()

        # Add metadata to data
        enhanced_data = data.copy()
        enhanced_data['generation_date'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        enhanced_data['filing_date'] = datetime.utcnow().strftime('%Y-%m-%d')

        # Add default values for optional fields in UCC-1
        if service_id == 'UCC1_FILING':
            enhanced_data.setdefault('debtor_org_type', 'Corporation')
            enhanced_data.setdefault('debtor_jurisdiction', 'Delaware')
            enhanced_data.setdefault('debtor_address', 'See Debtor Name')
            enhanced_data.setdefault('secured_party_address', 'See Secured Party Name')
            enhanced_data.setdefault('filing_office', 'State Filing Office')

        # Simple template replacement
        for key, value in enhanced_data.items():
            placeholder = f"{{{{{key}}}}}"
            template_content = template_content.replace(placeholder, str(value))

        # Generate filename
        case_id = data.get('case_id', 'new')
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"{service_id}_case_{case_id}_{timestamp}.txt"

        return template_content, filename

    def calculate_total_fee(self, service_id):
        """Calculate total fee for a service"""
        service = self.get_service(service_id)
        if not service:
            raise ValueError(f"Service '{service_id}' not found")

        return float(service['price_usdc'])

    def get_recurring_fee(self, service_id):
        """Get recurring annual fee for a service"""
        service = self.get_service(service_id)
        if not service:
            raise ValueError(f"Service '{service_id}' not found")

        return float(service['recurring_fee_usdc'])
