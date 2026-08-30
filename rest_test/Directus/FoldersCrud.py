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
from rest_util.rest_api_client import RestApiClient
import random
import string

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
                extracted_access_token = response1.json_data["data"]["access_token"]  # Retrieve access_token
            except (KeyError, TypeError, IndexError):
                pytest.fail("Required field 'access_token' not found in Step 1 response")
            logger.info(f"📌 Extracted access_token: {extracted_access_token}")
            allure.dynamic.parameter("Extracted_access_token", extracted_access_token)


        # Step 2: Create a new folder
        allure.dynamic.parameter("Step_2_Sl_No", 22)
        allure.dynamic.parameter("Step_2_Method", "POST")
        allure.dynamic.parameter("Step_2_Endpoint", "/folders")

        step2_endpoint = "/folders"

        folder_name = ''.join(random.choices(string.ascii_letters, k=10))  # Generate random folder name

        with allure.step("Step 2: POST /folders"):
            logger.info(f"🚀 Step 2: {'POST'} {step2_endpoint}")
            step2_payload = {'name': folder_name}  # Updated payload
            response2 = api_client.post(
                endpoint=step2_endpoint,
                json_payload=step2_payload,
                headers={"Authorization": f"Bearer {extracted_access_token}"}  # Use access_token as bearer token
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
                extracted_id = response2.json_data["data"]["id"]  # Retrieve ID
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
                headers={"Authorization": f"Bearer {extracted_access_token}"}  # Use access_token as bearer token
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
            folder_found = any(folder['id'] == extracted_id and folder['name'] == folder_name for folder in response3.json_data['data'])
            assert folder_found, f"Folder with ID {extracted_id} and name {folder_name} not found in the response."


        # Step 4: Delete a folder using folder id
        allure.dynamic.parameter("Step_4_Sl_No", 26)
        allure.dynamic.parameter("Step_4_Method", "DELETE")
        allure.dynamic.parameter("Step_4_Endpoint", f"/folders/{extracted_id}")

        step4_endpoint = f"/folders/{extracted_id}"

        with allure.step("Step 4: DELETE /folders/{id}"):
            logger.info(f"🚀 Step 4: {'DELETE'} {step4_endpoint}")
            response4 = api_client.delete(
                endpoint=step4_endpoint,
                headers={"Authorization": f"Bearer {extracted_access_token}"}  # Use access_token as bearer token
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
                headers={"Authorization": f"Bearer {extracted_access_token}"}  # Use access_token as bearer token
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

            # Validate that the response does NOT contain the deleted folder
            folder_deleted = not any(folder['id'] == extracted_id and folder['name'] == folder_name for folder in response5.json_data['data'])
            assert folder_deleted, f"Folder with ID {extracted_id} and name {folder_name} still exists in the response."

    def test_03_authenticate_login_to_retrieve_temporary_access_token_ai(self, api_client):
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


        # Step 2: Create a new folder
        allure.dynamic.parameter("Step_2_Sl_No", 22)
        allure.dynamic.parameter("Step_2_Method", "POST")
        allure.dynamic.parameter("Step_2_Endpoint", "/folders")

        step2_endpoint = "/folders"

        with allure.step("Step 2: POST /folders"):
            logger.info(f"🚀 Step 2: {'POST'} {step2_endpoint}")
            folder_name = ''.join(random.choices(string.ascii_lowercase, k=10))  # Random folder name
            step2_payload = {'name': folder_name}  # Updated payload without parent
            response2 = api_client.post(
                endpoint=step2_endpoint,
                json_payload=step2_payload,
                headers={'Authorization': f'Bearer {extracted_access_token}'}  # Added Bearer token
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


        # Step 3: Update a folder
        allure.dynamic.parameter("Step_3_Sl_No", 27)
        allure.dynamic.parameter("Step_3_Method", "PATCH")
        allure.dynamic.parameter("Step_3_Endpoint", f"/folders/{extracted_id}")

        step3_endpoint = f"/folders/{extracted_id}"

        with allure.step("Step 3: PATCH /folders/{id}"):
            logger.info(f"🚀 Step 3: {'PATCH'} {step3_endpoint}")
            updated_folder_name = ''.join(random.choices(string.ascii_lowercase, k=10))  # Random updated folder name
            step3_payload = {'name': updated_folder_name}  # Updated payload without parent

            logger.info(f"📤 Step 3 Request Payload: {json.dumps(step3_payload, indent=2)}")
            response3 = api_client.patch(
                endpoint=step3_endpoint,
                json_payload=step3_payload,
                headers={'Authorization': f'Bearer {extracted_access_token}'}  # Added Bearer token
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

            # Validate that the response has ID and updated folder name
            try:
                assert response3.json_data["data"]["id"] == extracted_id, "ID does not match the updated folder ID"
                assert response3.json_data["data"]["name"] == updated_folder_name, "Folder name was not updated correctly"
            except (KeyError, TypeError):
                pytest.fail("Required fields not found in Step 3 response")


        # Step 4: Delete a folder using folder id
        allure.dynamic.parameter("Step_4_Sl_No", 26)
        allure.dynamic.parameter("Step_4_Method", "DELETE")
        allure.dynamic.parameter("Step_4_Endpoint", f"/folders/{extracted_id}")

        step4_endpoint = f"/folders/{extracted_id}"

        with allure.step("Step 4: DELETE /folders/{id}"):
            logger.info(f"🚀 Step 4: {'DELETE'} {step4_endpoint}")
            response4 = api_client.delete(
                endpoint=step4_endpoint,
                headers={'Authorization': f'Bearer {extracted_access_token}'}  # Added Bearer token
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
                headers={'Authorization': f'Bearer {extracted_access_token}'}  # Added Bearer token
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

            # Validate that the response does NOT include the deleted folder
            folder_exists = any(folder['id'] == extracted_id and folder['name'] == updated_folder_name for folder in response5.json_data["data"])
            assert not folder_exists, "The deleted folder still exists in the list of folders!"

    def test_04_authenticate_login_to_retrieve_temporary_access_token_ai(self, api_client):
        """
        Combined test executing 8 API operations
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

            # Extract access_token from response
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

        folder_name_step2 = ''.join(random.choices(string.ascii_lowercase, k=10))  # Random folder name

        with allure.step("Step 2: POST /folders"):
            logger.info(f"🚀 Step 2: {'POST'} {step2_endpoint}")
            step2_payload = {'name': folder_name_step2}  # Updated payload
            response2 = api_client.post(
                endpoint=step2_endpoint,
                json_payload=step2_payload,
                headers={"Authorization": f"Bearer {extracted_access_token}"}
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

            # Extract id from response
            try:
                extracted_id = response2.json_data["data"]["id"]
            except (KeyError, TypeError, IndexError):
                pytest.fail("Required field 'id' not found in Step 2 response")
            logger.info(f"📌 Extracted id: {extracted_id}")
            allure.dynamic.parameter("Extracted_id", extracted_id)

        # Step 3: Create a new folder
        allure.dynamic.parameter("Step_3_Sl_No", 22)
        allure.dynamic.parameter("Step_3_Method", "POST")
        allure.dynamic.parameter("Step_3_Endpoint", "/folders")

        step3_endpoint = "/folders"

        folder_name_step3 = ''.join(random.choices(string.ascii_lowercase, k=10))  # Random folder name

        with allure.step("Step 3: POST /folders"):
            logger.info(f"🚀 Step 3: {'POST'} {step3_endpoint}")
            step3_payload = {'name': folder_name_step3, 'parent': extracted_id}  # Updated payload
            response3 = api_client.post(
                endpoint=step3_endpoint,
                json_payload=step3_payload,
                headers={"Authorization": f"Bearer {extracted_access_token}"}
            )

            logger.info(f"📤 Step 3 Request Payload: {json.dumps(step3_payload, indent=2)}")

            logger.info(f"📥 Step 3 Response Status: {response3.status_code}")
            logger.info(f"📥 Step 3 Response Body: {json.dumps(response3.json_data, indent=2) if response3.json_data else response3.text}")

            allure.attach(
                json.dumps(response3.json_data, indent=2) if response3.json_data else response3.text,
                name="Step 3 Response",
                attachment_type=allure.attachment_type.JSON if response3.json_data else allure.attachment_type.TEXT
            )

            assert response3.is_success(), f"Step 3 failed with status {response3.status_code}"
            logger.info(f"✅ Step 3 passed - Status: {response3.status_code}")

            # Extract newly generated ID from response
            try:
                extracted_newly = response3.json_data["data"]["id"]
            except (KeyError, TypeError, IndexError):
                pytest.fail("Required field 'newly' not found in Step 3 response")
            logger.info(f"📌 Extracted newly: {extracted_newly}")
            allure.dynamic.parameter("Extracted_newly", extracted_newly)

        # Step 4: Update a folder
        allure.dynamic.parameter("Step_4_Sl_No", 27)
        allure.dynamic.parameter("Step_4_Method", "PATCH")
        allure.dynamic.parameter("Step_4_Endpoint", "/folders/{id}")

        step4_endpoint = f"/folders/{extracted_newly}"

        folder_name_step4 = ''.join(random.choices(string.ascii_lowercase, k=10))  # Random folder name

        with allure.step("Step 4: PATCH /folders/{id}"):
            logger.info(f"🚀 Step 4: {'PATCH'} {step4_endpoint}")
            step4_payload = {'name': folder_name_step4, 'parent': extracted_id}  # Updated payload

            logger.info(f"📤 Step 4 Request Payload: {json.dumps(step4_payload, indent=2)}")

            response4 = api_client.patch(
                endpoint=step4_endpoint,
                json_payload=step4_payload,
                headers={"Authorization": f"Bearer {extracted_access_token}"}
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

            # Validate response
            try:
                assert response4.json_data["data"]["id"] == extracted_newly, "ID in response does not match the updated ID"
                assert response4.json_data["data"]["parent"] == extracted_id, "Parent ID in response does not match the expected parent ID"
                assert response4.json_data["data"]["name"] == folder_name_step4, "Folder name in response does not match the updated name"
            except (KeyError, TypeError):
                pytest.fail("Validation of response fields failed")

        # Step 5: Get the list of folder names
        allure.dynamic.parameter("Step_5_Sl_No", 21)
        allure.dynamic.parameter("Step_5_Method", "GET")
        allure.dynamic.parameter("Step_5_Endpoint", "/folders")

        step5_endpoint = "/folders"

        with allure.step("Step 5: GET /folders"):
            logger.info(f"🚀 Step 5: {'GET'} {step5_endpoint}")
            response5 = api_client.get(
                endpoint=step5_endpoint,
                headers={"Authorization": f"Bearer {extracted_access_token}"}
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

            # Validate response contains the folder created in Step 3
            folders = response5.json_data.get("data", [])
            folder_ids = [folder["id"] for folder in folders]
            assert extracted_newly in folder_ids, f"Folder with ID {extracted_newly} not found in the response"
            assert folder_name_step4 in [folder["name"] for folder in folders], f"Folder name '{folder_name_step4}' not found in the response"

        # Step 6: Delete a folder using folder id
        allure.dynamic.parameter("Step_6_Sl_No", 26)
        allure.dynamic.parameter("Step_6_Method", "DELETE")
        allure.dynamic.parameter("Step_6_Endpoint", "/folders/{id}")

        step6_endpoint = f"/folders/{extracted_id}"

        with allure.step("Step 6: DELETE /folders/{id}"):
            logger.info(f"🚀 Step 6: {'DELETE'} {step6_endpoint}")
            response6 = api_client.delete(
                endpoint=step6_endpoint,
                headers={"Authorization": f"Bearer {extracted_access_token}"}
            )

            logger.info(f"📥 Step 6 Response Status: {response6.status_code}")
            logger.info(f"📥 Step 6 Response Body: {json.dumps(response6.json_data, indent=2) if response6.json_data else response6.text}")

            allure.attach(
                json.dumps(response6.json_data, indent=2) if response6.json_data else response6.text,
                name="Step 6 Response",
                attachment_type=allure.attachment_type.JSON if response6.json_data else allure.attachment_type.TEXT
            )

            assert response6.is_success(), f"Step 6 failed with status {response6.status_code}"
            logger.info(f"✅ Step 6 passed - Status: {response6.status_code}")

        # Step 7: Delete a folder using folder id
        allure.dynamic.parameter("Step_7_Sl_No", 26)
        allure.dynamic.parameter("Step_7_Method", "DELETE")
        allure.dynamic.parameter("Step_7_Endpoint", "/folders/{id}")

        step7_endpoint = f"/folders/{extracted_newly}"

        with allure.step("Step 7: DELETE /folders/{id}"):
            logger.info(f"🚀 Step 7: {'DELETE'} {step7_endpoint}")
            response7 = api_client.delete(
                endpoint=step7_endpoint,
                headers={"Authorization": f"Bearer {extracted_access_token}"}
            )

            logger.info(f"📥 Step 7 Response Status: {response7.status_code}")
            logger.info(f"📥 Step 7 Response Body: {json.dumps(response7.json_data, indent=2) if response7.json_data else response7.text}")

            allure.attach(
                json.dumps(response7.json_data, indent=2) if response7.json_data else response7.text,
                name="Step 7 Response",
                attachment_type=allure.attachment_type.JSON if response7.json_data else allure.attachment_type.TEXT
            )

            assert response7.is_success(), f"Step 7 failed with status {response7.status_code}"
            logger.info(f"✅ Step 7 passed - Status: {response7.status_code}")

        # Step 8: Get the list of folder names
        allure.dynamic.parameter("Step_8_Sl_No", 21)
        allure.dynamic.parameter("Step_8_Method", "GET")
        allure.dynamic.parameter("Step_8_Endpoint", "/folders")

        step8_endpoint = "/folders"

        with allure.step("Step 8: GET /folders"):
            logger.info(f"🚀 Step 8: {'GET'} {step8_endpoint}")
            response8 = api_client.get(
                endpoint=step8_endpoint,
                headers={"Authorization": f"Bearer {extracted_access_token}"}
            )

            logger.info(f"📥 Step 8 Response Status: {response8.status_code}")
            logger.info(f"📥 Step 8 Response Body: {json.dumps(response8.json_data, indent=2) if response8.json_data else response8.text}")

            allure.attach(
                json.dumps(response8.json_data, indent=2) if response8.json_data else response8.text,
                name="Step 8 Response",
                attachment_type=allure.attachment_type.JSON if response8.json_data else allure.attachment_type.TEXT
            )

            assert response8.is_success(), f"Step 8 failed with status {response8.status_code}"
            logger.info(f"✅ Step 8 passed - Status: {response8.status_code}")

            # Validate that the deleted folders are not present in the response
            folders_after_deletion = response8.json_data.get("data", [])
            folder_ids_after_deletion = [folder["id"] for folder in folders_after_deletion]
            assert extracted_id not in folder_ids_after_deletion, f"Folder with ID {extracted_id} should not exist after deletion"
            assert extracted_newly not in folder_ids_after_deletion, f"Folder with ID {extracted_newly} should not exist after deletion"


































