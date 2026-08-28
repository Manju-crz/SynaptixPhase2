"""
Generated Test File
Generated on: 2026-08-28 18:40:55
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

@allure.suite('TestComponent01TestFile01')
class TestComponent01TestFile01:
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
            "client_id": "synaptix-portal",  # Updated client_id
            "username": "admin.synaptix",  # Updated username
            "password": "admin123",  # Updated password
            "grant_type": "password",  # Updated grant_type
        }

        step1_endpoint = "/realms/synaptix-technologies/protocol/openid-connect/token"

        with allure.step("Step 1: POST /realms/synaptix-technologies/protocol/openid-connect/token"):
            logger.info(f"🚀 Step 1: {'POST'} {step1_endpoint}")
            response1 = api_client.post(
                endpoint=step1_endpoint,
                data=step1_form_data  # Using data for application/x-www-form-urlencoded
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

            # Extract bearer token from response for use in subsequent steps
            if response1.json_data and 'access_token' in response1.json_data:
                bearer_token = response1.json_data['access_token']
                logger.info(f"📌 Extracted bearer token: {bearer_token}")
                allure.dynamic.parameter("Bearer_Token", bearer_token)
            else:
                logger.error("⚠️  'access_token' not found in response")
                pytest.fail("Step 1 failed: access_token not found in response")

        # Step 2: Get the list of Get group hierarchy
        allure.dynamic.parameter("Step_2_Sl_No", 234)
        allure.dynamic.parameter("Step_2_Method", "GET")
        allure.dynamic.parameter("Step_2_Endpoint", "/admin/realms/synaptix-technologies/groups")

        step2_endpoint = "/admin/realms/synaptix-technologies/groups"

        with allure.step("Step 2: GET /admin/realms/synaptix-technologies/groups"):
            logger.info(f"🚀 Step 2: {'GET'} {step2_endpoint}")
            response2 = api_client.get(
                endpoint=step2_endpoint,
                headers={"Authorization": f"Bearer {bearer_token}"}  # Using bearer token for authorization
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
            actual_group_names = {group['name'] for group in response2.json_data} if response2.json_data else set()

            logger.info(f"📌 Actual group names: {actual_group_names}")
            assert expected_group_names.issubset(actual_group_names), f"Expected group names {expected_group_names} not found in actual group names {actual_group_names}"


