"""
Generated Test File
Generated on: 2026-08-29 12:21:19
Base URL: http://localhost:8055/
Excel Source: Z5_Directus_2026_08_28_18_06.xlsx
"""

import json
import pytest
import allure
import logging
import random
import string
from rest_util.rest_api_client import RestApiClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="class")
def api_client():
    """Fixture to provide REST API client"""
    client = RestApiClient(base_url="http://localhost:8055/")
    yield client
    client.close()

@allure.suite('DirectusFoldersCrud')
class DirectusFoldersCrud:
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
                extracted_access_token = response1.json_data["data"]["access_token"]  # Retrieve access_token
            except (KeyError, TypeError, IndexError):
                pytest.fail("Required field 'access_token' not found in Step 1 response")
            logger.info(f"📌 Extracted access_token: {extracted_access_token}")
            allure.dynamic.parameter("Extracted_access_token", extracted_access_token)

        # Step 2: Get the list of folders
        allure.dynamic.parameter("Step_2_Sl_No", 21)
        allure.dynamic.parameter("Step_2_Method", "GET")
        allure.dynamic.parameter("Step_2_Endpoint", "/folders")

        step2_endpoint = "/folders"

        with allure.step("Step 2: GET /folders"):
            logger.info(f"🚀 Step 2: {'GET'} {step2_endpoint}")
            response2 = api_client.get(
                endpoint=step2_endpoint,
                headers={"Authorization": f"Bearer {extracted_access_token}"}  # Use access_token as bearer token
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

            # Validate that the response contains the folder name "aug28"
            folder_names = [folder['name'] for folder in response2.json_data.get("data", [])]  # Extract folder names
            assert "aug28" in folder_names, "Folder name 'aug28' not found in the response"  # Fail if not found
            logger.info("Folder name 'aug28' found in the response.")

    def test_02_authenticate_login_to_retrieve_temporary_access_token_ai(self, api_client):
        """
        Combined test executing 5 API operations
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
                extracted_access_token = response1.json_data["data"]["access_token"]
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
            folder_name = ''.join(random.choices(string.ascii_lowercase, k=10))  # Random alphabetical string
            step2_payload = {'name': folder_name}  # Modified payload
            response2 = api_client.post(
                endpoint=step2_endpoint,
                json_payload=step2_payload,
                headers={'Authorization': f'Bearer {extracted_access_token}'}  # Added bearer token
            )

            logger.info(f"📤 Step 2 Request Payload: {json.dumps(step2_payload, indent=2)}")

            logger.info(f"📥 Step 2 Response Status: {response2.status_code}")
            logger.info(f"📥 Step 2 Response Body: {json.dumps(response2.json_data, indent=2) if response2.json_data else response2.text}")
        
            allure.attach(
                json.dumps(response2.json_data, indent=2) if response2.json_data else response2.text,
                name="Step 2 Response",
                attachment_type=allure.attachment_type.JSON if response2.json_data else allure.attachment_type.TEXT
            )

            assert response2.is_success(), f"Step 2 failed with status {response2.status_code}"
            logger.info(f"✅ Step 2 passed - Status: {response2.status_code}")

            # Extract fields from response for use in subsequent steps
            try:
                extracted_id = response2.json_data["data"]["id"]
            except (KeyError, TypeError, IndexError):
                pytest.fail("Required field 'id' not found in Step 2 response")
            logger.info(f"📌 Extracted id: {extracted_id}")
            allure.dynamic.parameter("Extracted_id", extracted_id)

        # Step 3: Get the list of folder names
        allure.dynamic.parameter("Step_3_Sl_No", 21)
        allure.dynamic.parameter("Step_3_Method", "GET")
        allure.dynamic.parameter("Step_3_Endpoint", "/folders")

        step3_endpoint = "/folders"

        with allure.step("Step 3: GET /folders"):
            logger.info(f"🚀 Step 3: {'GET'} {step3_endpoint}")
            response3 = api_client.get(
                endpoint=step3_endpoint,
                headers={'Authorization': f'Bearer {extracted_access_token}'}  # Added bearer token
            )

            logger.info(f"📥 Step 3 Response Status: {response3.status_code}")
            logger.info(f"📥 Step 3 Response Body: {json.dumps(response3.json_data, indent=2) if response3.json_data else response3.text}")
        
            allure.attach(
                json.dumps(response3.json_data, indent=2) if response3.json_data else response3.text,
                name="Step 3 Response",
                attachment_type=allure.attachment_type.JSON if response3.json_data else allure.attachment_type.TEXT
            )

            assert response3.is_success(), f"Step 3 failed with status {response3.status_code}"
            logger.info(f"✅ Step 3 passed - Status: {response3.status_code}")

            # Validate that the response contains the created folder
            folder_exists = any(folder['id'] == extracted_id and folder['name'] == folder_name for folder in response3.json_data['data'])
            assert folder_exists, "The created folder does not exist in the folder list."

        # Step 4: Delete a folder using folder id
        allure.dynamic.parameter("Step_4_Sl_No", 26)
        allure.dynamic.parameter("Step_4_Method", "DELETE")
        allure.dynamic.parameter("Step_4_Endpoint", "/folders/{id}")

        step4_endpoint = f"/folders/{extracted_id}"  # Use the extracted ID

        with allure.step("Step 4: DELETE /folders/{id}"):
            logger.info(f"🚀 Step 4: {'DELETE'} {step4_endpoint}")
            response4 = api_client.delete(
                endpoint=step4_endpoint,
                headers={'Authorization': f'Bearer {extracted_access_token}'}  # Added bearer token
            )

            logger.info(f"📥 Step 4 Response Status: {response4.status_code}")
            logger.info(f"📥 Step 4 Response Body: {json.dumps(response4.json_data, indent=2) if response4.json_data else response4.text}")
        
            allure.attach(
                json.dumps(response4.json_data, indent=2) if response4.json_data else response4.text,
                name="Step 4 Response",
                attachment_type=allure.attachment_type.JSON if response4.json_data else allure.attachment_type.TEXT
            )

            assert response4.is_success(), f"Step 4 failed with status {response4.status_code}"
            logger.info(f"✅ Step 4 passed - Status: {response4.status_code}")

        # Step 5: Get the list of folder names
        allure.dynamic.parameter("Step_5_Sl_No", 21)
        allure.dynamic.parameter("Step_5_Method", "GET")
        allure.dynamic.parameter("Step_5_Endpoint", "/folders")

        step5_endpoint = "/folders"

        with allure.step("Step 5: GET /folders"):
            logger.info(f"🚀 Step 5: {'GET'} {step5_endpoint}")
            response5 = api_client.get(
                endpoint=step5_endpoint,
                headers={'Authorization': f'Bearer {extracted_access_token}'}  # Added bearer token
            )

            logger.info(f"📥 Step 5 Response Status: {response5.status_code}")
            logger.info(f"📥 Step 5 Response Body: {json.dumps(response5.json_data, indent=2) if response5.json_data else response5.text}")
        
            allure.attach(
                json.dumps(response5.json_data, indent=2) if response5.json_data else response5.text,
                name="Step 5 Response",
                attachment_type=allure.attachment_type.JSON if response5.json_data else allure.attachment_type.TEXT
            )

            assert response5.is_success(), f"Step 5 failed with status {response5.status_code}"
            logger.info(f"✅ Step 5 passed - Status: {response5.status_code}")

            # Validate that the deleted folder does not exist in the folder list
            folder_exists_after_deletion = any(folder['id'] == extracted_id and folder['name'] == folder_name for folder in response5.json_data['data'])
            assert not folder_exists_after_deletion, "The deleted folder still exists in the folder list."


















