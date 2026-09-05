"""
Generated Test File
Generated on: 2026-09-05 13:26:31
Base URL: http://localhost:8055
Excel Source: Z5_Directus_2026_08_28_18_06.xlsx
"""

import json
import pytest
import allure
import logging
from rest_util.rest_api_client import RestApiClient
import random
import string

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="class")
def api_client():
    """Fixture to provide REST API client"""
    client = RestApiClient(base_url="http://localhost:8055")
    yield client
    client.close()

@allure.suite('DirectusTestFile03')
class DirectusTestFile03:
    """
    Auto-generated test class based on natural language queries
    """

    logger = logging.getLogger(__name__)

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
                json_payload=step1_payload
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
            try:
                extracted_access_token = response1.json_data["data"]["access_token"]  # Extracting access_token
            except (KeyError, TypeError, IndexError):
                pytest.fail("Required field 'access_token' not found in Step 1 response")
            logger.info(f"📌 Extracted access_token: {extracted_access_token}")
            allure.dynamic.parameter("Extracted_access_token", extracted_access_token)

        # Step 2: Create a new folder
        allure.dynamic.parameter("Step_2_Sl_No", 22)
        allure.dynamic.parameter("Step_2_Method", "POST")
        allure.dynamic.parameter("Step_2_Endpoint", "/folders")

        step2_endpoint = "/folders"

        with allure.step("Step 2: POST /folders"):
            logger.info(f"🚀 Step 2: {'POST'} {step2_endpoint}")
            step2_payload = {'name': '',}  # Setting blank value for folder name, parent option removed
            response2 = api_client.post(
                endpoint=step2_endpoint,
                json_payload=step2_payload,
                headers={"Authorization": f"Bearer {extracted_access_token}"}  # Using access_token as bearer token
            )

            logger.info(f"📤 Step 2 Request Payload: {json.dumps(step2_payload, indent=2)}")

            logger.info(f"📥 Step 2 Response Status: {response2.status_code}")
            logger.info(f"📥 Step 2 Response Body: {json.dumps(response2.json_data, indent=2) if response2.json_data else response2.text}")
        
            allure.attach(
                json.dumps(response2.json_data, indent=2) if response2.json_data else response2.text,
                name="Step 2 Response",
                attachment_type=allure.attachment_type.JSON if response2.json_data else allure.attachment_type.TEXT
            )

            assert response2.status_code == 400, f"Step 2 failed with status {response2.status_code}"  # Validating error response
            logger.info(f"✅ Step 2 passed - Status: {response2.status_code}")

    def test_02_authenticate_login_to_retrieve_temporary_access_token_ai(self, api_client):
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
                json_payload=step1_payload  # Using json_payload as Content-Type is application/json
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
            try:
                extracted_access_token = response1.json_data["data"]["access_token"]
            except (KeyError, TypeError, IndexError):
                pytest.fail("Required field 'access_token' not found in Step 1 response")
            logger.info(f"📌 Extracted access_token: {extracted_access_token}")
            allure.dynamic.parameter("Extracted_access_token", extracted_access_token)

        # Step 2: Retrieve a single folder by unique identifier
        allure.dynamic.parameter("Step_2_Sl_No", 25)
        allure.dynamic.parameter("Step_2_Method", "GET")
        allure.dynamic.parameter("Step_2_Endpoint", "/folders/{id}")

        # Generate a random alphabetical string for the folder ID
        random_id = ''.join(random.choices(string.ascii_lowercase, k=10))
        step2_endpoint = f"/folders/{random_id}"

        with allure.step(f"Step 2: GET {step2_endpoint}"):
            logger.info(f"🚀 Step 2: {'GET'} {step2_endpoint}")
            response2 = api_client.get(
                endpoint=step2_endpoint,
                headers={"Authorization": f"Bearer {extracted_access_token}"}  # Using the extracted access token
            )

            logger.info(f"📥 Step 2 Response Status: {response2.status_code}")
            logger.info(f"📥 Step 2 Response Body: {json.dumps(response2.json_data, indent=2) if response2.json_data else response2.text}")
        
            allure.attach(
                json.dumps(response2.json_data, indent=2) if response2.json_data else response2.text,
                name="Step 2 Response",
                attachment_type=allure.attachment_type.JSON if response2.json_data else allure.attachment_type.TEXT
            )

            # Validate that the response returns an error with status code 404
            assert response2.status_code == 404, f"Step 2 expected status 404 but got {response2.status_code}"
            logger.info(f"✅ Step 2 passed - Status: {response2.status_code}")

    def test_03_authenticate_login_to_retrieve_temporary_access_token_ai(self, api_client):
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
            step1_payload = {'email': 'admin@example.com', 'password': 'admin123'}  # Updated payload
            response1 = api_client.post(
                endpoint=step1_endpoint,
                json_payload=step1_payload
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
            try:
                extracted_access_token = response1.json_data["data"]["access_token"]
            except (KeyError, TypeError, IndexError):
                pytest.fail("Required field 'access_token' not found in Step 1 response")
            logger.info(f"📌 Extracted access_token: {extracted_access_token}")
            allure.dynamic.parameter("Extracted_access_token", extracted_access_token)

        # Step 2: Update a folder
        random_string = ''.join(random.choices(string.ascii_lowercase, k=8))  # Generate random folder name and id
        allure.dynamic.parameter("Step_2_Sl_No", 27)
        allure.dynamic.parameter("Step_2_Method", "PATCH")
        allure.dynamic.parameter("Step_2_Endpoint", f"/folders/{random_string}")

        step2_endpoint = f"/folders/{random_string}"

        with allure.step(f"Step 2: PATCH {step2_endpoint}"):
            logger.info(f"🚀 Step 2: {'PATCH'} {step2_endpoint}")
            step2_payload = {'name': random_string, 'parent': 3}  # Use random string for folder name

            logger.info(f"📤 Step 2 Request Payload: {json.dumps(step2_payload, indent=2)}")

            response2 = api_client.patch(
                endpoint=step2_endpoint,
                json_payload=step2_payload,
                headers={"Authorization": f"Bearer {extracted_access_token}"}  # Use extracted access token
            )

            logger.info(f"📥 Step 2 Response Status: {response2.status_code}")
            logger.info(f"📥 Step 2 Response Body: {json.dumps(response2.json_data, indent=2) if response2.json_data else response2.text}")
        
            allure.attach(
                json.dumps(response2.json_data, indent=2) if response2.json_data else response2.text,
                name="Step 2 Response",
                attachment_type=allure.attachment_type.JSON if response2.json_data else allure.attachment_type.TEXT
            )

            assert response2.status_code == 400, f"Step 2 expected a 400 error but got {response2.status_code}"  # Validate error response
            logger.info(f"✅ Step 2 passed - Status: {response2.status_code}")

    logger = logging.getLogger(__name__)

    def test_04_authenticate_login_to_retrieve_temporary_access_token_ai(self, api_client):
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
            try:
                extracted_access_token = response1.json_data["data"]["access_token"]  # Retrieve access_token
            except (KeyError, TypeError, IndexError):
                pytest.fail("Required field 'access_token' not found in Step 1 response")
            logger.info(f"📌 Extracted access_token: {extracted_access_token}")
            allure.dynamic.parameter("Extracted_access_token", extracted_access_token)

        # Step 2: Delete a folder using folder id
        folder_id = 'randomfolderid'  # Using a random alphabetical string as folder id
        allure.dynamic.parameter("Step_2_Sl_No", 26)
        allure.dynamic.parameter("Step_2_Method", "DELETE")
        allure.dynamic.parameter("Step_2_Endpoint", f"/folders/{folder_id}")

        step2_endpoint = f"/folders/{folder_id}"

        with allure.step(f"Step 2: DELETE {step2_endpoint}"):
            logger.info(f"🚀 Step 2: {'DELETE'} {step2_endpoint}")
            response2 = api_client.delete(
                endpoint=step2_endpoint,
                headers={"Authorization": f"Bearer {extracted_access_token}"}  # Using access_token as bearer token
            )

            logger.info(f"📥 Step 2 Response Status: {response2.status_code}")
            logger.info(f"📥 Step 2 Response Body: {json.dumps(response2.json_data, indent=2) if response2.json_data else response2.text}")
        
            allure.attach(
                json.dumps(response2.json_data, indent=2) if response2.json_data else response2.text,
                name="Step 2 Response",
                attachment_type=allure.attachment_type.JSON if response2.json_data else allure.attachment_type.TEXT
            )

            assert response2.status_code == 400, f"Step 2 expected status 400 but got {response2.status_code}"  # Validate error response
            logger.info(f"✅ Step 2 passed - Status: {response2.status_code}")














