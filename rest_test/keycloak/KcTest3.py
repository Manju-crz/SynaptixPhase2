"""
Generated Test File
Generated on: 2026-08-22 15:19:45
Base URL: http://localhost:8080
Excel Source: OpenAPI_Data_2026_08_22_00_39.xlsx
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

@allure.suite('Generated API Tests')
class TestGeneratedAPIs:
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

        step1_endpoint = "/realms/synaptix-technologies/protocol/openid-connect/token"
    
        # Create payload for the POST request
        payload = {
            "client_id": "synaptix-portal",
            "username": "john.employee",
            "grant_type": "password",
            "password": "employee123"
        }

        with allure.step("Step 1: POST /realms/synaptix-technologies/protocol/openid-connect/token"):
            logger.info(f"🚀 Step 1: {'POST'} {step1_endpoint}")
            response1 = api_client.post(
                endpoint=step1_endpoint,
                data=payload  # Using data parameter for application/x-www-form-urlencoded
            )

            logger.info(f"📥 Step 1 Response Status: {response1.status_code}")
            logger.info(f"📥 Step 1 Response Body: {json.dumps(response1.json_data, indent=2) if response1.json_data else response1.text}")
        
            allure.attach(
                json.dumps(response1.json_data, indent=2) if response1.json_data else response1.text,
                name="Step 1 Response",
                attachment_type=allure.attachment_type.JSON if response1.json_data else allure.attachment_type.TEXT
            )

            assert response1.is_success(), f"Step 1 failed with status {response1.status_code}"
            logger.info(f"✅ Step 1 passed - Status: {response1.status_code}")

            # Extract access token from response for use in subsequent steps
            if response1.json_data and 'access_token' in response1.json_data:
                bearerToken = response1.json_data['access_token']
                logger.info(f"📌 Extracted bearerToken: {bearerToken}")
                allure.dynamic.parameter("Extracted_bearerToken", bearerToken)
            else:
                logger.error("⚠️  'access_token' not found in response")
                assert False, "Access token not found in response"

        # Step 2: Get the existing list of Get group hierarchy
        allure.dynamic.parameter("Step_2_Sl_No", 234)
        allure.dynamic.parameter("Step_2_Method", "GET")
        allure.dynamic.parameter("Step_2_Endpoint", "/admin/realms/synaptix-technologies/groups")

        step2_endpoint = "/admin/realms/synaptix-technologies/groups"

        with allure.step("Step 2: GET /admin/realms/synaptix-technologies/groups"):
            logger.info(f"🚀 Step 2: {'GET'} {step2_endpoint}")
            response2 = api_client.get(
                endpoint=step2_endpoint,
                headers={"Authorization": f"Bearer {bearerToken}"}  # Using the extracted bearer token for authorization
            )

            logger.info(f"📥 Step 2 Response Status: {response2.status_code}")
            logger.info(f"📥 Step 2 Response Body: {json.dumps(response2.json_data, indent=2) if response2.json_data else response2.text}")
        
            allure.attach(
                json.dumps(response2.json_data, indent=2) if response2.json_data else response2.text,
                name="Step 2 Response",
                attachment_type=allure.attachment_type.JSON if response2.json_data else allure.attachment_type.TEXT
            )

            # Validate the response has 403 return code and error message
            assert response2.status_code == 403, f"Step 2 failed with status {response2.status_code}"
            assert 'error' in response2.json_data and response2.json_data['error'] == "HTTP 403 Forbidden", "Expected error message not found in response"
            logger.info(f"✅ Step 2 passed - Status: {response2.status_code}")


