"""
Document Agent
Manages document storage via Microsoft Graph/SharePoint (with local file fallback)
"""

import os
import requests
from datetime import datetime


class DocumentAgent:
    """Agent for managing legal document storage"""

    def __init__(self, mock_mode=None):
        """Initialize Document Agent"""
        if mock_mode is None:
            mock_mode = os.environ.get('MOCK_MODE', 'True').lower() in ('true', '1', 'yes')

        self.mock_mode = mock_mode
        self.tenant_id = os.environ.get("MS_TENANT_ID")
        self.client_id = os.environ.get("MS_CLIENT_ID")
        self.client_secret = os.environ.get("MS_CLIENT_SECRET")
        self.site_id = os.environ.get("SHAREPOINT_SITE_ID")
        self.drive_id = os.environ.get("SHAREPOINT_DRIVE_ID")
        self.access_token = None

        # Create local storage directory for mock mode
        self.local_storage_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'document_storage'
        )
        if self.mock_mode:
            os.makedirs(self.local_storage_path, exist_ok=True)
            print(f"📁 Using local document storage: {self.local_storage_path}")

        # Initialize MS Graph if not in mock mode
        if not self.mock_mode and all([self.tenant_id, self.client_id, self.client_secret]):
            try:
                self._get_token()
                print("✅ Microsoft Graph initialized")
            except Exception as e:
                print(f"⚠️  MS Graph initialization failed: {e}")
                print("   Falling back to local storage")
                self.mock_mode = True
        else:
            if not self.mock_mode:
                print("⚠️  Missing MS Graph credentials, using local storage")
                self.mock_mode = True

    def _get_token(self):
        """Get OAuth access token for Microsoft Graph"""
        import msal

        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        scope = ["https://graph.microsoft.com/.default"]

        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=authority,
            client_credential=self.client_secret
        )

        result = app.acquire_token_for_client(scopes=scope)

        if "access_token" in result:
            self.access_token = result['access_token']
            print("✅ MS Graph token acquired")
        else:
            raise Exception("Could not acquire MS Graph token")

    def upload_document(self, document_content_str, file_name, case_id):
        """
        Upload document to client locker

        Args:
            document_content_str: Document content as string
            file_name: Name of the file
            case_id: Case ID for folder organization

        Returns:
            URL to the uploaded document or local path
        """
        if self.mock_mode:
            # Store locally
            case_folder = os.path.join(self.local_storage_path, f'Case_{case_id}_Locker')
            os.makedirs(case_folder, exist_ok=True)

            file_path = os.path.join(case_folder, file_name)
            with open(file_path, 'w') as f:
                f.write(document_content_str)

            print(f"📄 MOCK: Document saved to {file_path}")
            return file_path

        # Real SharePoint upload
        try:
            if not self.access_token:
                self._get_token()

            folder_name = f"Case_{case_id}_Locker"
            upload_url = (
                f"https://graph.microsoft.com/v1.0/sites/{self.site_id}"
                f"/drives/{self.drive_id}/items/root:/{folder_name}/{file_name}:/content"
            )

            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'text/plain'
            }

            response = requests.put(
                upload_url,
                headers=headers,
                data=document_content_str.encode('utf-8')
            )

            if response.status_code == 201:
                doc_data = response.json()
                web_url = doc_data.get('webUrl')
                print(f"✅ Document uploaded to SharePoint: {web_url}")
                return web_url
            else:
                print(f"❌ SharePoint Upload Error: {response.text}")
                # Fallback to local storage
                return self._fallback_local_upload(document_content_str, file_name, case_id)

        except Exception as e:
            print(f"❌ Error uploading to SharePoint: {e}")
            # Fallback to local storage
            return self._fallback_local_upload(document_content_str, file_name, case_id)

    def _fallback_local_upload(self, content, file_name, case_id):
        """Fallback to local storage if SharePoint fails"""
        case_folder = os.path.join(self.local_storage_path, f'Case_{case_id}_Locker')
        os.makedirs(case_folder, exist_ok=True)

        file_path = os.path.join(case_folder, file_name)
        with open(file_path, 'w') as f:
            f.write(content)

        print(f"📄 Fallback: Document saved locally to {file_path}")
        return file_path

    def create_client_folder(self, case_id):
        """Create a folder for a case"""
        folder_name = f"Case_{case_id}_Locker"

        if self.mock_mode:
            folder_path = os.path.join(self.local_storage_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            print(f"📁 MOCK: Created folder {folder_path}")
            return folder_path

        # TODO: Implement SharePoint folder creation
        return None

    def get_document_url(self, case_id, file_name):
        """Get URL/path to a document"""
        if self.mock_mode:
            return os.path.join(
                self.local_storage_path,
                f'Case_{case_id}_Locker',
                file_name
            )

        # TODO: Implement SharePoint URL retrieval
        return None
