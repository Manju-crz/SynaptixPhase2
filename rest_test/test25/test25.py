"""
Generated Test File
Generated on: 2026-08-02 18:40:14
Base URL: https://petstore.swagger.io/v2
Excel Source: OpenAPI_Data_2026_07_30_02_28.xlsx
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
class TestGeneratedAPIs:
    """
    Auto-generated test class based on natural language queries
    """

    @allure.feature('API Testing')
    @allure.story('Combined API Test')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('Combined Test: 3 API Operations')
    @allure.description("""
        This test executes 3 API operations sequentially:
        1. Create a new pet in pest store
        2. Update pet information
        3. Delete a pet
    """)
    def test_01_create_a_new_pet_in_pest_store(self, api_client):
        """
        Combined test executing 3 API operations
        """

        # Step 1: Create a new pet in pest store
        allure.dynamic.parameter("Step_1_Sl_No", 2)
        allure.dynamic.parameter("Step_1_Method", "POST")
        allure.dynamic.parameter("Step_1_Endpoint", "/pet")

        step1_endpoint = "/pet"

        with allure.step("Step 1: POST /pet"):
            logger.info(f"🚀 Step 1: {'POST'} {step1_endpoint}")
            step1_payload = {   'category': {'id': 0, 'name': 'string_value'},
                'id': 0,
                'name': 'doggie',
                'photoUrls': ['string_value'],
                'status': 'available',
                'tags': [{'id': 0, 'name': 'string_value'}]}
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
            if response1.json_data and 'pet_id' in response1.json_data:
                extracted_pet_id = response1.json_data['pet_id']
                logger.info(f"📌 Extracted pet_id: {extracted_pet_id}")
                allure.dynamic.parameter("Extracted_pet_id", extracted_pet_id)
                extracted_petId = extracted_pet_id  # Alias
            else:
                logger.warning("⚠️  'pet_id' not found in response, using default value")
                extracted_pet_id = 1 if 'pet_id' in ['id', 'pet_id', 'user_id', 'order_id'] else "default_value"


        # Step 2: Update pet information
        allure.dynamic.parameter("Step_2_Sl_No", 3)
        allure.dynamic.parameter("Step_2_Method", "PUT")
        allure.dynamic.parameter("Step_2_Endpoint", "/pet")

        step2_endpoint = "/pet"

        with allure.step("Step 2: PUT /pet"):
            logger.info(f"🚀 Step 2: {'PUT'} {step2_endpoint}")
            step2_payload = {   'category': {'id': 0, 'name': 'string_value'},
                'id': 0,
                'name': 'doggie',
                'photoUrls': ['string_value'],
                'status': 'available',
                'tags': [{'id': 0, 'name': 'string_value'}]}
            response2 = api_client.put(
                endpoint=step2_endpoint,
                json_payload=step2_payload
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
            if response2.json_data and 'id' in response2.json_data:
                extracted_id = response2.json_data['id']
                logger.info(f"📌 Extracted id: {extracted_id}")
                allure.dynamic.parameter("Extracted_id", extracted_id)
                # Aliases for common ID patterns
                extracted_petId = extracted_id
                extracted_userId = extracted_id
                extracted_orderId = extracted_id
            else:
                logger.warning("⚠️  'id' not found in response, using default value")
                extracted_id = 1 if 'id' in ['id', 'pet_id', 'user_id', 'order_id'] else "default_value"
                extracted_petId = extracted_id
                extracted_userId = extracted_id
                extracted_orderId = extracted_id


        # Step 3: Delete a pet
        allure.dynamic.parameter("Step_3_Sl_No", 8)
        allure.dynamic.parameter("Step_3_Method", "DELETE")
        allure.dynamic.parameter("Step_3_Endpoint", "/pet/{petId}")

        step3_endpoint = "/pet/{petId}"

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


    def test_01_create_a_new_pet_in_pest_store_ai(self, api_client):
        """
        Combined test executing 3 API operations
        """

        # Step 1: Create a new pet in pest store
        allure.dynamic.parameter("Step_1_Sl_No", 2)
        allure.dynamic.parameter("Step_1_Method", "POST")
        allure.dynamic.parameter("Step_1_Endpoint", "/pet")

        step1_endpoint = "/pet"

        with allure.step("Step 1: POST /pet"):
            logger.info(f"🚀 Step 1: {'POST'} {step1_endpoint}")
            step1_payload = {   'category': {'id': 0, 'name': 'string_value'},
                'id': 0,
                'name': 'doggie',
                'photoUrls': ['string_value'],
                'status': 'available',
                'tags': [{'id': 0, 'name': 'string_value'}]}
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
            if response1.json_data and 'id' in response1.json_data:
                # Modification: Retrieve the pet_id from the response
                extracted_pet_id = response1.json_data['id']
                logger.info(f"📌 Extracted pet_id: {extracted_pet_id}")
                allure.dynamic.parameter("Extracted_pet_id", extracted_pet_id)
            else:
                logger.warning("⚠️  'id' not found in response, using default value")
                extracted_pet_id = 1


        # Step 2: Update pet information
        allure.dynamic.parameter("Step_2_Sl_No", 3)
        allure.dynamic.parameter("Step_2_Method", "PUT")
        allure.dynamic.parameter("Step_2_Endpoint", "/pet")

        step2_endpoint = "/pet"

        with allure.step("Step 2: PUT /pet"):
            logger.info(f"🚀 Step 2: {'PUT'} {step2_endpoint}")
            # Modification: Use the pet_id from previous response
            step2_payload = {   'id': extracted_pet_id,
                'category': {'id': 0, 'name': 'string_value'},
                'name': 'doggie',
                'photoUrls': ['string_value'],
                'status': 'available',
                'tags': [{'id': 0, 'name': 'string_value'}]}
            response2 = api_client.put(
                endpoint=step2_endpoint,
                json_payload=step2_payload
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


        # Step 3: Delete a pet
        allure.dynamic.parameter("Step_3_Sl_No", 8)
        allure.dynamic.parameter("Step_3_Method", "DELETE")
        allure.dynamic.parameter("Step_3_Endpoint", "/pet/{petId}")

        # Modification: Use the pet_id from previous response
        step3_endpoint = f"/pet/{extracted_pet_id}"

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


