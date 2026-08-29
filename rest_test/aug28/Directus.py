"""
Generated Test File
Generated on: 2026-08-28 18:28:22
Base URL: http://localhost:8080
Excel Source: Z4_KeyClock_2026_08_28_18_05.xlsx
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
    client = RestApiClient(base_url="http://localhost:8080")
    yield client
    client.close()

@allure.suite('DirectusTests')
class DirectusTests:
    """
    Auto-generated test class based on natural language queries
    """

    def test_01_obtain_the_openid_access_token_ai(self, api_client):
        """
        Combined test executing 2 API operations
        """

        # Step 1: Obtain the openid access token
        allure.dynamic.parameter("Step_1_Sl_No", 1)
        allure.dynamic.parameter("Step_1_Method", "POST")
        allure.dynamic.parameter("Step_1_Endpoint", "/realms/synaptix-technologies/protocol/openid-connect/token")

        # Step 1 - Form data
        step1_form_data = {
            "client_id": "synaptix-portal",  # Updated value
            "username": "admin.synaptix",     # Updated value
            "password": "admin123",           # Updated value
            "grant_type": "password",          # Updated value
        }

        step1_endpoint = "/realms/synaptix-technologies/protocol/openid-connect/token"

        with allure.step("Step 1: POST /realms/synaptix-technologies/protocol/openid-connect/token"):
            logger.info(f"🚀 Step 1: {'POST'} {step1_endpoint}")
            response1 = api_client.post(
                endpoint=step1_endpoint,
                data=step1_form_data  # Using data parameter for form-urlencoded
            )

            logger.info(f"📤 Step 1 Form Data: {step1_form_data}")

            logger.info(f"📥 Step 1 Response Status: {response1.status_code}")
            logger.info(f"📥 Step 1 Response Body: {json.dumps(response1.json_data, indent=2) if response1.json_data else response1.text}")

            allure.attach(
                json.dumps(response1.json_data, indent=2) if response1.json_data else response1.text,
                name="Step 1 Response",
                attachment_type=allure.attachment_type.JSON if response1.json_data else allure.attachment_type.TEXT
            )

            assert response1.is_success(), f"Step 1 failed with status {response1.status_code}"
            logger.info(f"✅ Step 1 passed - Status: {response1.status_code}")

            # Extract access token as bearerToken
            if response1.json_data and 'access_token' in response1.json_data:
                bearerToken = response1.json_data['access_token']
                logger.info(f"📌 Extracted bearerToken: {bearerToken}")
                allure.dynamic.parameter("Extracted_bearerToken", bearerToken)
            else:
                logger.warning("⚠️  'access_token' not found in response")
                pytest.fail("Access token not found in response")

        # Step 2: Get the list of Get group hierarchy
        allure.dynamic.parameter("Step_2_Sl_No", 234)
        allure.dynamic.parameter("Step_2_Method", "GET")
        allure.dynamic.parameter("Step_2_Endpoint", "/admin/realms/synaptix-technologies/groups")

        step2_endpoint = "/admin/realms/synaptix-technologies/groups"

        with allure.step("Step 2: GET /admin/realms/synaptix-technologies/groups"):
            logger.info(f"🚀 Step 2: {'GET'} {step2_endpoint}")
            response2 = api_client.get(
                endpoint=step2_endpoint,
                headers={"Authorization": f"Bearer {bearerToken}"}  # Using bearer token for authorization
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

            # Validate the group names in the response
            expected_group_names = {"Employees", "IT", "Finance", "HR", "Management"}
            if response2.json_data and isinstance(response2.json_data, list):
                actual_group_names = {group['name'] for group in response2.json_data if 'name' in group}
                logger.info(f"📌 Actual group names: {actual_group_names}")
                assert expected_group_names.issubset(actual_group_names), f"Expected groups {expected_group_names} not found in the response"
            else:
                logger.warning("⚠️  Response data is not a list or is empty")
                pytest.fail("Response data is not valid")

    def test_02_retrieve_a_temporary_access_token_ai(self, api_client):
        """
        Combined test executing 2 API operations
        """

        # Step 1: Retrieve a temporary access token
        allure.dynamic.parameter("Step_1_Sl_No", 3)
        allure.dynamic.parameter("Step_1_Method", "POST")
        allure.dynamic.parameter("Step_1_Endpoint", "/auth/refresh")

        step1_endpoint = "/auth/refresh"

        with allure.step("Step 1: POST /auth/refresh"):
            logger.info(f"🚀 Step 1: {'POST'} {step1_endpoint}")
            step1_payload = {
                'email': 'admin@example.com',
                'password': 'admin123'
            }
            response1 = api_client.post(
                endpoint=step1_endpoint,
                json_payload=step1_payload  # Using json_payload as the Content-Type is application/json
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
                extracted_access_token = "default_value"  # This should not happen as we expect the token

        # Step 2: Get the list of folders
        allure.dynamic.parameter("Step_2_Sl_No", 21)
        allure.dynamic.parameter("Step_2_Method", "GET")
        allure.dynamic.parameter("Step_2_Endpoint", "/folders")

        step2_endpoint = "/folders"

        with allure.step("Step 2: GET /folders"):
            logger.info(f"🚀 Step 2: {'GET'} {step2_endpoint}")
            headers = {
                'Authorization': f'Bearer {extracted_access_token}'  # Using the extracted access token
            }
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

            # Validate the response contains the folder with name "aug28"
            folder_names = [folder['name'] for folder in response2.json_data['data']] if response2.json_data and 'data' in response2.json_data else []
            assert "aug28" in folder_names, "Folder with name 'aug28' not found in the response."







