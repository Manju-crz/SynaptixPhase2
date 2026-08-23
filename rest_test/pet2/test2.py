"""
Generated Test File
Generated on: 2026-08-23 03:21:12
Base URL: https://petstore.swagger.io/v2
Excel Source: OpenAPI_Data_2026_08_04_01_15.xlsx
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
    client = RestApiClient(base_url="https://petstore.swagger.io/v2")
    yield client
    client.close()

@allure.suite('Generated API Tests')
class TestComponent02TestFile01:
    """
    Auto-generated test class based on natural language queries
    """

    def test_01_create_a_new_pet_in_pest_store_ai_11(self, api_client):
        """
        Combined test executing 3 API operations
        """

        # Step 1: Create a new pet in pest store
        allure.dynamic.parameter("Step_1_Sl_No", 2)
        allure.dynamic.parameter("Step_1_Method", "POST")
        allure.dynamic.parameter("Step_1_Endpoint", "/pet")

        step1_endpoint = "/pet"
        unique_pet_name = f"Pet_{uuid.uuid4().hex}"  # Generate a unique pet name

        payload = {
            "name": unique_pet_name,
            "status": "available"
        }

        with allure.step("Step 1: POST /pet"):
            logger.info(f"🚀 Step 1: {'POST'} {step1_endpoint} with payload: {payload}")
            response1 = api_client.post(
                endpoint=step1_endpoint,
                json_payload=payload  # Use json_payload for application/json
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

            # Extract pet_id from response for use in subsequent steps
            if response1.json_data and 'pet_id' in response1.json_data:
                extracted_pet_id = response1.json_data['pet_id']
                logger.info(f"📌 Extracted pet_id: {extracted_pet_id}")
                allure.dynamic.parameter("Extracted_pet_id", extracted_pet_id)
            else:
                logger.warning("⚠️  'pet_id' not found in response, using default value")
                extracted_pet_id = "default_value"  # Default value if pet_id not found


        # Step 2: Update pet information
        allure.dynamic.parameter("Step_2_Sl_No", 3)
        allure.dynamic.parameter("Step_2_Method", "PUT")
        allure.dynamic.parameter("Step_2_Endpoint", "/pet")

        step2_endpoint = "/pet"
        updated_unique_pet_name = f"UpdatedPet_{uuid.uuid4().hex}"  # Generate a new unique pet name

        update_payload = {
            "pet_id": extracted_pet_id,  # Use pet_id from previous response
            "name": updated_unique_pet_name,
            "status": "available"
        }

        with allure.step("Step 2: PUT /pet"):
            logger.info(f"🚀 Step 2: {'PUT'} {step2_endpoint} with payload: {update_payload}")
            response2 = api_client.put(
                endpoint=step2_endpoint,
                json_payload=update_payload  # Use json_payload for application/json
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

            # Extract id from response for use in subsequent steps
            if response2.json_data and 'id' in response2.json_data:
                extracted_id = response2.json_data['id']
                logger.info(f"📌 Extracted id: {extracted_id}")
                allure.dynamic.parameter("Extracted_id", extracted_id)
            else:
                logger.warning("⚠️  'id' not found in response, using default value")
                extracted_id = "default_value"  # Default value if id not found


        # Step 3: Delete a pet
        allure.dynamic.parameter("Step_3_Sl_No", 8)
        allure.dynamic.parameter("Step_3_Method", "DELETE")
        allure.dynamic.parameter("Step_3_Endpoint", "/pet/{petId}")

        step3_endpoint = f"/pet/{extracted_pet_id}"  # Use pet_id from previous response

        with allure.step("Step 3: DELETE /pet/{petId}"):
            logger.info(f"🚀 Step 3: {'DELETE'} {step3_endpoint}")
            response3 = api_client.delete(
                endpoint=step3_endpoint
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


