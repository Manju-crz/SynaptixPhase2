"""
Generated Test File
Generated on: 2026-08-29 11:12:43
Base URL: http://localhost:8055/
Excel Source: Z5_Directus_2026_08_28_18_06.xlsx
"""

import json
import pytest
import allure
import logging
from rest_util.rest_api_client import RestApiClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="class")
def api_client():
    """Fixture to provide REST API client"""
    client = RestApiClient(base_url="http://localhost:8055/")
    yield client
    client.close()

@allure.suite('Ag29TestFile03')
class Ag29TestFile03:
    """
    Auto-generated test class based on natural language queries
    """

    def test_01_authenticate_login_to_retrieve_temporary_access_token_ai(self, api_client):
        """
        Combined test executing 2 API operations
        """

        # Step 1: Authenticate Login to retrieve temporary access_token
        allure.dynamic.parameter("Step_1_Sl_No", 2)
        allure.dynamic.parameter("Step_1_Method", "POST")
        allure.dynamic.parameter("Step_1_Endpoint", "/auth/login")

        step1_endpoint = "/auth/login"

        with allure.step("Step 1: POST /auth/login"):
            logger.info(f"🚀 Step 1: {'POST'} {step1_endpoint}")
            step1_payload = {'email': 'admin@example.com', 'password': 'admin123'}  # Modified payload
            response1 = api_client.post(
                endpoint=step1_endpoint,
                json_payload=step1_payload  # Using json_payload for application/json
            )

            logger.info(f"📤 Step 1 Request Payload: {json.dumps(step1_payload, indent=2)}")

            logger.info(f"📥 Step 1 Response Status: {response1.status_code}")
            logger.info(f"📥 Step 1 Response Body: {json.dumps(response1.json_data, indent=2) if response1.json_data else response1.text}")
        
            allure.attach(
                json.dumps(response1.json_data, indent=2) if response1.json_data else response1.text,
                name="Step 1 Response",
                attachment_type=allure.attachment_type.JSON if response1.json_data else allure.attachment_type.TEXT
            )

            assert response1.is_success(), f"Step 1 failed with status {response1.status_code}"
            logger.info(f"✅ Step 1 passed - Status: {response1.status_code}")

            # Extract fields from response for use in subsequent steps
            if response1.json_data and 'access_token' in response1.json_data:
                extracted_access_token = response1.json_data['access_token']
                logger.info(f"📌 Extracted access_token: {extracted_access_token}")
                allure.dynamic.parameter("Extracted_access_token", extracted_access_token)
            else:
                logger.warning("⚠️  'access_token' not found in response, using default value")
                extracted_access_token = "default_value"  # Fallback if not found

        # Step 2: Get the list of folders
        allure.dynamic.parameter("Step_2_Sl_No", 21)
        allure.dynamic.parameter("Step_2_Method", "GET")
        allure.dynamic.parameter("Step_2_Endpoint", "/folders")

        step2_endpoint = "/folders"

        with allure.step("Step 2: GET /folders"):
            logger.info(f"🚀 Step 2: {'GET'} {step2_endpoint}")
            headers = {"Authorization": f"Bearer {extracted_access_token}"}  # Using the extracted access token
            response2 = api_client.get(
                endpoint=step2_endpoint,
                headers=headers  # Adding the Authorization header
            )

            logger.info(f"📥 Step 2 Response Status: {response2.status_code}")
            logger.info(f"📥 Step 2 Response Body: {json.dumps(response2.json_data, indent=2) if response2.json_data else response2.text}")
        
            allure.attach(
                json.dumps(response2.json_data, indent=2) if response2.json_data else response2.text,
                name="Step 2 Response",
                attachment_type=allure.attachment_type.JSON if response2.json_data else allure.attachment_type.TEXT
            )

            assert response2.is_success(), f"Step 2 failed with status {response2.status_code}"
            logger.info(f"✅ Step 2 passed - Status: {response2.status_code}")

            # Validate that the response contains a folder with the name "aug28"
            folder_names = [folder['name'] for folder in response2.json_data.get('data', []) if 'name' in folder]
            assert "aug28" in folder_names, "Folder with name 'aug28' not found in the response."  # Validation check


