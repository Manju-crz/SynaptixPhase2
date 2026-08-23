"""
Generated Test File
Generated on: 2026-08-23 03:14:13
Base URL: https://petstore.swagger.io/v2
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
    client = RestApiClient(base_url="https://petstore.swagger.io/v2")
    yield client
    client.close()

@allure.suite('Generated API Tests')
class PetT:
    """
    Auto-generated test class based on natural language queries
    """

    def test_01_create_a_new_pet_in_pest_store_ai_12(self, api_client):
        """
        Combined test executing 3 API operations
        """

        # Step 1: Create a new pet in pest store
        allure.dynamic.parameter("Step_1_Sl_No", 107)
        allure.dynamic.parameter("Step_1_Method", "POST")
        allure.dynamic.parameter("Step_1_Endpoint", "/admin/realms/{realm}/clients")

        step1_endpoint = "/admin/realms/{realm}/clients"

        with allure.step("Step 1: POST /admin/realms/{realm}/clients"):
            logger.info(f"🚀 Step 1: {'POST'} {step1_endpoint}")
            step1_payload = {
                'id': 'string_value',
                'clientId': 'string_value',
                'name': 'string_value',
                'description': 'string_value',
                'type': 'string_value',
                'rootUrl': 'string_value',
                'adminUrl': 'string_value',
                'baseUrl': 'string_value',
                'surrogateAuthRequired': True,
                'enabled': True,
                'alwaysDisplayInConsole': True,
                'clientAuthenticatorType': 'string_value',
                'secret': 'string_value',
                'registrationAccessToken': 'string_value',
                'defaultRoles': ['string_value'],
                'redirectUris': ['string_value'],
                'webOrigins': ['string_value'],
                'notBefore': 0,
                'bearerOnly': True,
                'consentRequired': True,
                'standardFlowEnabled': True,
                'implicitFlowEnabled': True,
                'directAccessGrantsEnabled': True,
                'serviceAccountsEnabled': True,
                'authorizationServicesEnabled': True,
                'directGrantsOnly': True,
                'publicClient': True,
                'frontchannelLogout': True,
                'protocol': 'string_value',
                'attributes': {},
                'authenticationFlowBindingOverrides': {},
                'fullScopeAllowed': True,
                'nodeReRegistrationTimeout': 0,
                'registeredNodes': {},
                'protocolMappers': [{
                    'config': {},
                    'consentRequired': True,
                    'consentText': 'string_value',
                    'id': 'string_value',
                    'name': 'string_value',
                    'protocol': 'string_value',
                    'protocolMapper': 'string_value'
                }],
                'clientTemplate': 'string_value',
                'useTemplateConfig': True,
                'useTemplateScope': True,
                'useTemplateMappers': True,
                'defaultClientScopes': ['string_value'],
                'optionalClientScopes': ['string_value'],
                'authorizationSettings': {
                    'id': 'string_value',
                    'clientId': 'string_value',
                    'name': 'string_value',
                    'allowRemoteResourceManagement': True,
                    'policyEnforcementMode': {'type': 'string_value'},
                    'resources': [{
                        '_id': 'string_value',
                        'name': 'string_value',
                        'uris': ['string_value'],
                        'type': 'string_value',
                        'scopes': [{
                            'id': 'string_value',
                            'name': 'string_value',
                            'iconUri': 'string_value',
                            'policies': [],
                            'resources': [],
                            'displayName': 'string_value'
                        }]
                    }]
                },
                'access': {},
                'origin': 'string_value'
            }
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
            if response1.json_data and 'clientId' in response1.json_data:
                extracted_pet_id = response1.json_data['clientId']  # Changed to clientId based on the new context
                logger.info(f"📌 Extracted pet_id: {extracted_pet_id}")
                allure.dynamic.parameter("Extracted_pet_id", extracted_pet_id)
            else:
                logger.warning("⚠️  'clientId' not found in response, using default value")
                extracted_pet_id = "default_value"

        # Step 2: Update pet information
        allure.dynamic.parameter("Step_2_Sl_No", 288)
        allure.dynamic.parameter("Step_2_Method", "PUT")
        allure.dynamic.parameter("Step_2_Endpoint", "/admin/realms/{realm}/organizations/{org-id}")

        step2_endpoint = "/admin/realms/{realm}/organizations/{org-id}"

        with allure.step("Step 2: PUT /admin/realms/{realm}/organizations/{org-id}"):
            logger.info(f"🚀 Step 2: {'PUT'} {step2_endpoint}")
            step2_payload = {
                'id': extracted_pet_id,  # Use the extracted pet_id from Step 1
                'name': 'string_value',
                'alias': 'string_value',
                'enabled': True,
                'description': 'string_value',
                'redirectUrl': 'string_value',
                'attributes': {},
                'domains': [{'name': 'string_value', 'verified': True}],
                'members': [{
                    'id': 'string_value',
                    'username': 'string_value',
                    'firstName': 'string_value',
                    'lastName': 'string_value',
                    'email': 'string_value',
                    'emailVerified': True,
                    'attributes': {},
                    'userProfileMetadata': {
                        'attributes': [{'name': 'string_value', 'displayName': 'string_value', 'required': True, 'readOnly': True}],
                        'groups': [{'name': 'string_value', 'displayHeader': 'string_value', 'displayDescription': 'string_value'}]
                    },
                    'enabled': True,
                    'self': 'string_value',
                    'origin': 'string_value',
                    'createdTimestamp': 0,
                    'totp': True,
                    'federationLink': 'string_value',
                    'serviceAccountClientId': 'string_value',
                    'credentials': [{
                        'id': 'string_value',
                        'type': 'string_value',
                        'userLabel': 'string_value',
                        'createdDate': 0,
                        'secretData': 'string_value',
                        'credentialData': 'string_value',
                        'priority': 0,
                        'value': 'string_value',
                        'temporary': True,
                        'device': 'string_value',
                        'hashedSaltedValue': 'string_value',
                        'salt': 'string_value',
                        'hashIterations': 0,
                        'counter': 0,
                        'algorithm': 'string_value',
                        'digits': 0,
                        'period': 0,
                        'config': {}
                    }],
                    'disableableCredentialTypes': ['string_value'],
                    'requiredActions': ['string_value'],
                    'federatedIdentities': [{'identityProvider': 'string_value', 'userId': 'string_value', 'userName': 'string_value'}],
                    'realmRoles': ['string_value'],
                    'clientRoles': {},
                    'clientConsents': [{'clientId': 'string_value', 'grantedClientScopes': ['string_value'], 'createdDate': 0, 'lastUpdatedDate': 0, 'grantedRealmRoles': ['string_value']}],
                    'notBefore': 0,
                    'verifiableCredentials': [{'credentialScopeName': 'string_value', 'credentialConfigurationId': 'string_value', 'revision': 'string_value', 'createdDate': 0, 'updatedDate': 0, 'userAttributes': {}}],
                    'issuedVerifiableCredentials': [{'id': 'string_value', 'userId': 'string_value', 'credentialType': 'string_value', 'issuedAt': 0, 'expiresAt': 0, 'clientId': 'string_value', 'clientName': 'string_value', 'clientBaseUrl': 'string_value', 'revision': 'string_value'}],
                    'applicationRoles': {},
                    'socialLinks': [{'socialProvider': 'string_value', 'socialUserId': 'string_value', 'socialUsername': 'string_value'}],
                    'groups': ['string_value'],
                    'access': {},
                    'membershipType': {'type': 'string_value'}
                }]
            }
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
            else:
                logger.warning("⚠️  'id' not found in response, using default value")
                extracted_id = "default_value"

        # Step 3: Delete a pet
        allure.dynamic.parameter("Step_3_Sl_No", 113)
        allure.dynamic.parameter("Step_3_Method", "DELETE")
        allure.dynamic.parameter("Step_3_Endpoint", "/admin/realms/{realm}/clients/{client-uuid}")

        step3_endpoint = "/admin/realms/{realm}/clients/{client-uuid}"

        with allure.step("Step 3: DELETE /admin/realms/{realm}/clients/{client-uuid}"):
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


