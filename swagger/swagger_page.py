"""
Swagger Page Object - Reusable page elements and actions
"""

import logging
import json
from playwright.sync_api import Page, expect

logging.basicConfig(
    level=logging.INFO,
    format='\n%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class SwaggerPage:
    """Page object for Swagger UI pages"""

    def __init__(self, page: Page):
        self.page = page
        self.swagger_ui = page.locator("#swagger-ui")

    def verify_swagger_ui_visible(self, timeout: int = 10000) -> bool:
        """
        Verify that the Swagger UI element is visible.

        Args:
            timeout: Maximum time to wait for element (ms)

        Returns:
            bool: True if visible, False otherwise
        """
        try:
            if self.swagger_ui.count() > 0:
                expect(self.swagger_ui).to_be_visible(timeout=timeout)
                logger.info("Swagger UI element is visible")
                return True
            else:
                logger.info("ℹ No Swagger UI element found (may not be a Swagger page)")
                return False
        except Exception as e:
            logger.error(f"Failed to verify Swagger UI: {str(e)}")
            return False

    def get_h3_tag_data(self) -> dict:
        """
        Find all h3 elements and retrieve data-tag and data-is-open attribute values.

        Returns:
            dict: Dictionary with data-tag as key and data-is-open as value
                  e.g., {"Funds": "true", "Users": "false"}
        """
        tag_data = {}

        try:
            # Find all h3 elements with data-tag attribute
            h3_elements = self.page.locator("h3[data-tag]")
            count = h3_elements.count()

            logger.info(f"Found {count} h3 elements with data-tag attribute")

            for i in range(count):
                element = h3_elements.nth(i)

                # Get attribute values
                data_tag = element.get_attribute("data-tag")
                data_is_open = element.get_attribute("data-is-open")

                if data_tag:
                    tag_data[data_tag] = data_is_open
                    logger.info(f"  - {data_tag}: {data_is_open}")

            logger.info(f"✅ Retrieved {len(tag_data)} tag entries")
            return tag_data

        except Exception as e:
            logger.error(f"Failed to retrieve h3 tag data: {str(e)}")
            return tag_data

    def expand_h3_tag(self, tag_name: str) -> bool:
        """
        Expand the h3 header if it is not already expanded.

        Args:
            tag_name: The value of data-tag attribute (e.g., "Activity", "Funds")

        Returns:
            bool: True if expanded successfully, False otherwise
        """
        try:
            # Find the h3 element with the specified data-tag
            h3_element = self.page.locator(f'h3[data-tag="{tag_name}"]')

            if h3_element.count() == 0:
                logger.error(f"❌ h3 element with data-tag='{tag_name}' not found")
                return False

            # Get current data-is-open value
            is_open = h3_element.get_attribute("data-is-open")
            logger.info(f"Tag '{tag_name}' current state: data-is-open={is_open}")

            # If not expanded, click to expand
            if is_open == "false":
                logger.info(f"Expanding tag '{tag_name}'...")
                h3_element.locator("a").click()

                # Wait for the element to update
                self.page.wait_for_timeout(500)

                # Verify it is now expanded
                is_open_after = h3_element.get_attribute("data-is-open")

                if is_open_after == "true":
                    logger.info(f"✅ Tag '{tag_name}' expanded successfully")
                    return True
                else:
                    logger.error(f"❌ Tag '{tag_name}' failed to expand. data-is-open={is_open_after}")
                    return False
            else:
                logger.info(f"ℹ Tag '{tag_name}' is already expanded")
                return True

        except Exception as e:
            logger.error(f"Failed to expand tag '{tag_name}': {str(e)}")
            return False

    def get_h3_small_description(self, tag_name: str) -> str:
        """
        Get the inner text of the small element inside the h3 tag.

        Args:
            tag_name: The value of data-tag attribute (e.g., "Activity", "Funds")

        Returns:
            str: The inner text of the small element, or empty string if not found
        """
        try:
            # Find the small element inside the h3 with specified data-tag
            small_element = self.page.locator(f'//h3[@data-tag="{tag_name}"]/small')

            if small_element.count() == 0:
                logger.info(f"ℹ No small element found for tag '{tag_name}'")
                return ""

            inner_text = small_element.inner_text()
            logger.info(f"Tag '{tag_name}' description: {inner_text}")
            return inner_text

        except Exception as e:
            logger.error(f"Failed to get description for tag '{tag_name}': {str(e)}")
            return ""

    def get_api_operations_basics(self, tag_name: str) -> list:
        """
        Get all API operations (method, path, summary, expansion status) for a given tag.

        Args:
            tag_name: The value of data-tag attribute (e.g., "Activity", "Funds")

        Returns:
            list: List of dictionaries containing method, path, summary, and expansion status
        """
        operations = []

        try:
            # Locate parent element for the given tag
            parent_element = self.page.locator(
                f'//div[h3[@data-tag="{tag_name}"]]//div[@class="operation-tag-content"]/span/div[not(@class="opblock opblock-deprecated")]'
            )

            count = parent_element.count()
            logger.info(f"Found {count} API operations for tag '{tag_name}'")

            for i in range(count):
                # Find all inner elements relative to parent (excluding deprecated operations)
                method_elements = parent_element.locator('xpath=.//span[@class="opblock-summary-method"]')
                path_elements = parent_element.locator('xpath=.//span[@class="opblock-summary-path"]')
                summary_elements = parent_element.locator('xpath=.//div[@class="opblock-summary-description"]')
                expansion_status_elements = parent_element.locator('xpath=.//button[@class="opblock-summary-control"]')

                operation = {
                    'method': method_elements.nth(i).inner_text(),
                    'path': path_elements.nth(i).get_attribute('data-path'),
                    'summary': summary_elements.nth(i).inner_text() if summary_elements.count() > i else '',
                    'expanded': expansion_status_elements.nth(i).get_attribute('aria-expanded')
                               if expansion_status_elements.count() > i else ''
                }
                operations.append(operation)
                logger.info(f"  - {operation['method']} {operation['path']}: {operation['summary']}")

            logger.info(f"✅ Retrieved {len(operations)} operations for tag '{tag_name}'")
            return operations

        except Exception as e:
            logger.error(f"Failed to get API operations for tag '{tag_name}': {str(e)}")
            return operations

    def get_operation_body_element(self, component: str, operation_method: str, operation_path: str):
        """
        Find and return the operation body element for a specific API operation.

        Args:
            component: The component/tag name (e.g., "Activity", "Funds")
            operation_method: The HTTP method (e.g., "GET", "POST")
            operation_path: The API path (e.g., "/rest/v1/activity")

        Returns:
            Locator: The opblock-body element for the matching operation

        Raises:
            Exception: If no matching operation is found
        """
        try:
            # Step 1: Find all operation section elements for the component
            operation_section_elements = self.page.locator(
                f'//div[h3[@data-tag="{component}"]]//div[@class="operation-tag-content"]/span/div[not(@class="opblock opblock-deprecated")]'
            )

            count = operation_section_elements.count()
            logger.info(f"Found {count} operation sections for component '{component}'")

            for i in range(count):
                section = operation_section_elements.nth(i)

                # Step 2: Find the expand button and expand if collapsed
                expand_button = section.locator('xpath=.//button[@class="opblock-summary-control"]')

                aria_expanded = expand_button.get_attribute('aria-expanded')
                if aria_expanded == 'false':
                    logger.info(f"Expanding operation section {i + 1}...")
                    expand_button.click()
                    self.page.wait_for_timeout(300)

                    # Verify expansion
                    aria_expanded_after = expand_button.get_attribute('aria-expanded')
                    if aria_expanded_after != 'true':
                        logger.warning(f"Failed to expand operation section {i + 1}")
                        continue

                # Step 3: Get method and path from the section
                method_element = section.locator('xpath=.//span[@class="opblock-summary-method"]')
                path_element = section.locator('xpath=.//span[@class="opblock-summary-path"]')

                method_text = method_element.inner_text()
                path_value = path_element.get_attribute('data-path')

                # Step 4: Check if this matches the requested operation
                if method_text == operation_method and path_value == operation_path:
                    logger.info(f"✅ Found matching operation: {operation_method} {operation_path}")

                    # Find and return the opblock-body element
                    body_element = section.locator('xpath=.//div[@class="opblock-body"]')

                    if body_element.count() > 0:
                        logger.info(f"✅ Returning operation body element")
                        return body_element
                    else:
                        raise Exception(f"Operation body element not found for {operation_method} {operation_path}")

            # Step 5: No matching operation found
            raise Exception(f"No matching operation found for {operation_method} {operation_path} in component '{component}'")

        except Exception as e:
            logger.error(f"Failed to get operation body element: {str(e)}")
            raise

    def get_operation_section_by_details(self, component_name: str, method_type: str, operation_path: str):
        """
        Find and return the operation body section element for a specific API operation
        based on component, method, and path.

        Args:
            component_name: The component/tag name matching data-tag attribute (e.g., "pet", "store")
            method_type: The HTTP method matching opblock-summary-method class (e.g., "GET", "POST", "PUT", "DELETE")
            operation_path: The API path matching data-path attribute (e.g., "/pet/{petId}/uploadImage")

        Returns:
            Locator: The opblock-body element for the matching operation section

        Raises:
            Exception: If no matching operation is found
        """
        try:
            # Step 1: Find all operation section elements for the component (excluding deprecated)
            operation_sections = self.page.locator(
                f'//div[h3[@data-tag="{component_name}"]]//div[@class="operation-tag-content"]/span/div[not(@class="opblock opblock-deprecated")]'
            )

            count = operation_sections.count()
            logger.info(f"Found {count} operation sections for component '{component_name}'")

            for i in range(count):
                section = operation_sections.nth(i)

                # Step 2: Extract method and path from the section
                method_element = section.locator('xpath=.//span[@class="opblock-summary-method"]')
                path_element = section.locator('xpath=.//span[@class="opblock-summary-path"]')

                if method_element.count() == 0 or path_element.count() == 0:
                    continue

                current_method = method_element.inner_text()
                current_path = path_element.get_attribute('data-path')

                # Step 3: Check if this section matches the requested operation
                if current_method == method_type and current_path == operation_path:
                    logger.info(f"✅ Found matching operation: {method_type} {operation_path}")

                    # Step 4: Find the expand button
                    expand_button = section.locator('xpath=.//button[@class="opblock-summary-control"]')

                    if expand_button.count() > 0:
                        aria_expanded = expand_button.get_attribute('aria-expanded')

                        # Step 5: Click only if aria-expanded="false"
                        if aria_expanded == "false":
                            logger.info(f"Expanding operation section (aria-expanded={aria_expanded})...")
                            expand_button.click()
                            self.page.wait_for_timeout(300)

                            # Verify expansion
                            aria_expanded_after = expand_button.get_attribute('aria-expanded')
                            if aria_expanded_after == "true":
                                logger.info(f"✅ Operation section expanded successfully")
                            else:
                                logger.warning(f"⚠ Operation section may not have expanded properly")
                        else:
                            logger.info(f"ℹ Operation section already expanded (aria-expanded={aria_expanded})")

                    # Step 6: Find and return the opblock-body element
                    body_element = section.locator('xpath=.//div[@class="opblock-body"]')

                    if body_element.count() > 0:
                        logger.info(f"✅ Returning operation body section element")
                        return body_element
                    else:
                        raise Exception(f"Operation body element not found for {method_type} {operation_path}")

            # Step 7: No matching operation found
            raise Exception(f"No matching operation found for {method_type} {operation_path} in component '{component_name}'")

        except Exception as e:
            logger.error(f"Failed to get operation section by details: {str(e)}")
            raise

    def get_operation_description_text(self, body_element) -> str:
        """
        Extract the description text from the operation body element.

        Args:
            body_element: The opblock-body element returned by get_operation_section_by_details

        Returns:
            str: The text within the <p> tag inside the opblock-description section, or empty string if not found
        """
        try:
            # Find the opblock-description div
            description_div = body_element.locator('xpath=.//div[@class="opblock-description"]')

            if description_div.count() == 0:
                logger.info("ℹ No opblock-description element found")
                return ""

            # Find the renderedMarkdown div inside
            markdown_div = description_div.locator('xpath=.//div[@class="renderedMarkdown"]')

            if markdown_div.count() == 0:
                logger.info("ℹ No renderedMarkdown element found")
                return ""

            # Find the p tag and get its text
            p_element = markdown_div.locator('xpath=.//p')

            if p_element.count() > 0:
                text = p_element.inner_text()
                logger.info(f"✅ Found description text: {text}")
                return text
            else:
                logger.info("ℹ No p element found inside renderedMarkdown")
                return ""

        except Exception as e:
            logger.error(f"Failed to get operation description text: {str(e)}")
            return ""

    def get_header_parameters(self, body_element) -> str:
        """
        Extract header parameters from the operation body element.

        Args:
            body_element: The opblock-body element returned by get_operation_section_by_details

        Returns:
            str: JSON string containing list of header parameter dictionaries
        """
        header_params = []

        try:
            # Find all tr elements with data-param-in="header"
            header_tr_elements = body_element.locator('xpath=.//tr[@data-param-in="header"]')
            count = header_tr_elements.count()
            logger.info(f"Found {count} header parameters")

            for i in range(count):
                tr_element = header_tr_elements.nth(i)

                # Get data-param-name value
                param_name = tr_element.get_attribute('data-param-name')
                if not param_name:
                    continue

                param_dict = {"name": param_name}

                # Check if parameter is required (class ends with "required")
                name_div = tr_element.locator('xpath=.//div[starts-with(@class, "parameter__name")]')
                if name_div.count() > 0:
                    name_class = name_div.get_attribute('class')
                    param_dict["required"] = 'required' in name_class if name_class else False
                else:
                    param_dict["required"] = False

                # Get parameter type
                type_div = tr_element.locator('xpath=.//div[@class="parameter__type"]')
                if type_div.count() > 0:
                    type_text = type_div.inner_text().strip()
                    param_dict["type"] = type_text

                # Get description if present
                desc_td = tr_element.locator('xpath=.//td[contains(@class, "parameters-col_description")]')
                if desc_td.count() > 0:
                    p_element = desc_td.locator('xpath=.//div[@class="renderedMarkdown"]/p')
                    if p_element.count() > 0:
                        desc_text = p_element.inner_text().strip()
                        if desc_text:
                            param_dict["description"] = desc_text

                header_params.append(param_dict)
                logger.info(f"  - {param_dict}")

            logger.info(f"✅ Collected {len(header_params)} header parameters")
            return json.dumps(header_params) if header_params else ""

        except Exception as e:
            logger.error(f"Failed to get header parameters: {str(e)}")
            return json.dumps(header_params) if header_params else ""

    def get_query_parameters(self, body_element) -> str:
        """
        Extract query parameters from the operation body element.

        Args:
            body_element: The opblock-body element returned by get_operation_section_by_details

        Returns:
            str: JSON string containing list of query parameter dictionaries
        """
        import json
        query_params = []

        try:
            # Find all tr elements with data-param-in="query"
            query_tr_elements = body_element.locator('xpath=.//tr[@data-param-in="query"]')
            count = query_tr_elements.count()

            logger.info(f"Found {count} query parameters")

            for i in range(count):
                tr_element = query_tr_elements.nth(i)

                # Get data-param-name value
                param_name = tr_element.get_attribute('data-param-name')
                if not param_name:
                    continue

                param_dict = {"name": param_name}

                # Check if parameter is required (class ends with "required")
                name_div = tr_element.locator('xpath=.//div[starts-with(@class, "parameter__name")]')
                if name_div.count() > 0:
                    name_class = name_div.get_attribute('class')
                    param_dict["required"] = 'required' in name_class if name_class else False
                else:
                    param_dict["required"] = False

                # Get parameter type
                type_div = tr_element.locator('xpath=.//div[@class="parameter__type"]')
                if type_div.count() > 0:
                    type_text = type_div.inner_text().strip()
                    param_dict["type"] = type_text

                # Get description if present
                desc_td = tr_element.locator('xpath=.//td[contains(@class, "parameters-col_description")]')
                if desc_td.count() > 0:
                    p_element = desc_td.locator('xpath=.//div[@class="renderedMarkdown"]/p')
                    if p_element.count() > 0:
                        desc_text = p_element.inner_text().strip()
                        if desc_text:
                            param_dict["description"] = desc_text

                query_params.append(param_dict)
                logger.info(f"  - {param_dict}")

            logger.info(f"✅ Collected {len(query_params)} query parameters")
            return json.dumps(query_params) if query_params else ""

        except Exception as e:
            logger.error(f"Failed to get query parameters: {str(e)}")
            return json.dumps(query_params) if query_params else ""

    def get_path_parameters(self, body_element) -> str:
        """
        Extract path parameters from the operation body element.

        Args:
            body_element: The opblock-body element returned by get_operation_section_by_details

        Returns:
            str: JSON string containing list of path parameter dictionaries
        """
        import json
        path_params = []

        try:
            # Find all tr elements with data-param-in="path"
            path_tr_elements = body_element.locator('xpath=.//tr[@data-param-in="path"]')
            count = path_tr_elements.count()

            logger.info(f"Found {count} path parameters")

            for i in range(count):
                tr_element = path_tr_elements.nth(i)

                # Get data-param-name value
                param_name = tr_element.get_attribute('data-param-name')
                if not param_name:
                    continue

                param_dict = {"name": param_name}

                # Check if parameter is required (class ends with "required")
                name_div = tr_element.locator('xpath=.//div[starts-with(@class, "parameter__name")]')
                if name_div.count() > 0:
                    name_class = name_div.get_attribute('class')
                    param_dict["required"] = 'required' in name_class if name_class else False
                else:
                    param_dict["required"] = False

                # Get parameter type
                type_div = tr_element.locator('xpath=.//div[@class="parameter__type"]')
                if type_div.count() > 0:
                    type_text = type_div.inner_text().strip()
                    param_dict["type"] = type_text

                # Get description if present
                desc_td = tr_element.locator('xpath=.//td[contains(@class, "parameters-col_description")]')
                if desc_td.count() > 0:
                    p_element = desc_td.locator('xpath=.//div[@class="renderedMarkdown"]/p')
                    if p_element.count() > 0:
                        desc_text = p_element.inner_text().strip()
                        if desc_text:
                            param_dict["description"] = desc_text

                path_params.append(param_dict)
                logger.info(f"  - {param_dict}")

            logger.info(f"✅ Collected {len(path_params)} path parameters")
            return json.dumps(path_params) if path_params else ""

        except Exception as e:
            logger.error(f"Failed to get path parameters: {str(e)}")
            return json.dumps(path_params) if path_params else ""

    def get_form_data_parameters(self, body_element) -> str:
        """
        Extract form data parameters from the operation body element.

        Args:
            body_element: The opblock-body element returned by get_operation_section_by_details

        Returns:
            str: JSON string containing list of form data parameter dictionaries
        """
        import json
        form_data_params = []

        try:
            # Find all tr elements with data-param-in="formData"
            form_data_tr_elements = body_element.locator('xpath=.//tr[@data-param-in="formData"]')
            count = form_data_tr_elements.count()

            logger.info(f"Found {count} form data parameters")

            for i in range(count):
                tr_element = form_data_tr_elements.nth(i)

                # Get data-param-name value
                param_name = tr_element.get_attribute('data-param-name')
                if not param_name:
                    continue

                param_dict = {"name": param_name}

                # Check if parameter is required (class ends with "required")
                name_div = tr_element.locator('xpath=.//div[starts-with(@class, "parameter__name")]')
                if name_div.count() > 0:
                    name_class = name_div.get_attribute('class')
                    param_dict["required"] = 'required' in name_class if name_class else False
                else:
                    param_dict["required"] = False

                # Get parameter type
                type_div = tr_element.locator('xpath=.//div[@class="parameter__type"]')
                if type_div.count() > 0:
                    type_text = type_div.inner_text().strip()
                    param_dict["type"] = type_text

                # Get description if present
                desc_td = tr_element.locator('xpath=.//td[contains(@class, "parameters-col_description")]')
                if desc_td.count() > 0:
                    p_element = desc_td.locator('xpath=.//div[@class="renderedMarkdown"]/p')
                    if p_element.count() > 0:
                        desc_text = p_element.inner_text().strip()
                        if desc_text:
                            param_dict["description"] = desc_text

                form_data_params.append(param_dict)
                logger.info(f"  - {param_dict}")

            logger.info(f"✅ Collected {len(form_data_params)} form data parameters")
            return json.dumps(form_data_params) if form_data_params else ""

        except Exception as e:
            logger.error(f"Failed to get form data parameters: {str(e)}")
            return json.dumps(form_data_params) if form_data_params else ""

    def get_request_body_json(self, component_name: str, method_type: str, operation_path: str) -> str:
        """
        Extract the Example Value JSON content for a specific API operation.

        Args:
            component_name: The component/tag name (e.g., "pet", "store", "user")
            method_type: The HTTP method (e.g., "GET", "POST", "PUT", "DELETE")
            operation_path: The API path (e.g., "/pet/{petId}")

        Returns:
            str: The JSON content from the Example Value section, or empty string if not found
        """
        try:
            # Get the operation body element
            body_element = self.get_operation_section_by_details(component_name, method_type, operation_path)

            if not body_element:
                logger.error(f"Could not find operation body for {method_type} {operation_path}")
                return ""

            # Find the "Example Value" button (data-name="example")
            example_button = body_element.locator('xpath=.//button[@data-name="example"]')

            if example_button.count() == 0:
                logger.info("No Example Value button found")
                return ""

            # Click the Example Value button to ensure the panel is active
            example_button.click()
            logger.info("Clicked Example Value button")

            # Wait a moment for the content to load
            self.page.wait_for_timeout(500)

            # Find the code element with class "language-json" within the example panel
            code_element = body_element.locator('xpath=.//code[@class="language-json"]')

            if code_element.count() == 0:
                logger.info("No JSON code element found")
                return ""

            # Extract the JSON content
            json_content = code_element.inner_text().strip()
            logger.info(f"✅ Extracted Example Value JSON for {method_type} {operation_path}")
            logger.info(f"JSON content: {json_content[:200]}...")  # Log first 200 chars

            return json_content

        except Exception as e:
            logger.error(f"Failed to get example value JSON: {str(e)}")
            return ""

    def get_response_model_json(self, component_name: str, method_type: str, operation_path: str) -> str:
        """
        Extract the Model JSON content from response section or request body for a specific API operation.
        Handles multiple DOM structures: response models, request body models, arrays, nested objects.

        Args:
            component_name: The component/tag name (e.g., "pet", "store", "user")
            method_type: The HTTP method (e.g., "GET", "POST", "PUT", "DELETE")
            operation_path: The API path (e.g., "/pet/{petId}")

        Returns:
            str: The JSON representation of the model, or empty string if not found
        """
        try:
            logger.info(f"Starting model extraction for {method_type} {operation_path}")

            # Get the operation body element
            body_element = self.get_operation_section_by_details(component_name, method_type, operation_path)

            if not body_element:
                logger.error(f"Could not find operation body for {method_type} {operation_path}")
                return ""

            logger.info("Got operation body element")

            # Try to find model in multiple locations:
            # 1. Response section (for GET, DELETE responses)
            # 2. Request body parameters (for POST, PUT requests)
            model_container = None
            source_type = ""

            # Strategy 1: Check response section
            responses_section = body_element.locator('xpath=.//div[@class="opblock-section responses"]')
            if responses_section.count() > 0:
                logger.info("Found responses section")
                # Expand if collapsed
                expand_button = responses_section.locator('xpath=.//button[contains(@class, "opblock-summary-control")]')
                if expand_button.count() > 0:
                    try:
                        expand_button.click()
                        logger.info("Expanded responses section")
                        self.page.wait_for_timeout(300)
                    except:
                        pass

                # Find response row with model
                response_row = body_element.locator('xpath=.//tr[contains(@class, "response")]')
                if response_row.count() > 0:
                    response_code = response_row.nth(0).get_attribute('data-code')
                    logger.info(f"Found response row for code: {response_code}")

                    # Find and click Model button
                    model_button = response_row.nth(0).locator('xpath=.//button[@data-name="model"]')
                    if model_button.count() > 0:
                        logger.info("Found Model button in response section")
                        model_button.click()
                        self.page.wait_for_timeout(500)

                        model_container = response_row.nth(0).locator('xpath=.//div[@class="model-container"]')
                        if model_container.count() > 0:
                            source_type = f"response (code: {response_code})"
                            logger.info(f"Using model from {source_type}")

            # Strategy 2: Check request body parameters (for POST/PUT)
            if not model_container or model_container.count() == 0:
                logger.info("Checking request body parameters section")
                body_param_row = body_element.locator('xpath=.//tr[@data-param-in="body"]')

                if body_param_row.count() > 0:
                    logger.info("Found body parameter row")

                    # Find and click Model button
                    model_button = body_param_row.locator('xpath=.//button[@data-name="model"]')
                    if model_button.count() > 0:
                        logger.info("Found Model button in body parameters")
                        model_button.click()
                        self.page.wait_for_timeout(500)

                        model_container = body_param_row.locator('xpath=.//div[@class="model-container"]')
                        if model_container.count() > 0:
                            source_type = "request body"
                            logger.info(f"Using model from {source_type}")

            # If no model container found, return empty
            if not model_container or model_container.count() == 0:
                logger.info("No model-container found in any section")
                return ""

            logger.info("Found model-container, expanding all collapsed elements")

            # Iterate to expand all collapsed model elements (max 15 iterations for deeply nested structures)
            max_iterations = 15
            for iteration in range(max_iterations):
                # Find all collapsed buttons
                collapsed_buttons = model_container.locator('xpath=.//button[@class="model-box-control" and @aria-expanded="false"]')
                count = collapsed_buttons.count()

                if count == 0:
                    logger.info(f"All elements expanded (iteration {iteration + 1})")
                    break

                logger.info(f"Expanding {count} collapsed elements (iteration {iteration + 1})")

                # Click each collapsed button
                for i in range(count):
                    try:
                        collapsed_buttons.nth(i).click()
                        self.page.wait_for_timeout(100)
                    except Exception as e:
                        logger.warning(f"Failed to click button {i}: {str(e)}")

                # Wait for expansion
                self.page.wait_for_timeout(200)

            # Extract model structure - handle both object and array root types
            model_json = self._extract_model_from_container(model_container)

            if model_json:
                logger.info(f"✅ Extracted model JSON from {source_type} for {method_type} {operation_path}")
            else:
                logger.warning(f"⚠ No model structure extracted for {method_type} {operation_path}")

            return model_json

        except Exception as e:
            logger.error(f"Failed to get model JSON: {str(e)}")
    
    
    def _extract_model_from_container(self, model_container) -> str:
        """
        Extract model structure from model-container element.
        Handles both object and array root types.

        Args:
            model_container: The model-container element

        Returns:
            str: JSON representation of the model structure
        """
        try:
            import json

            # Check if root is an array (starts with [)
            root_model = model_container.locator('xpath=.//span[@class="model"]').first
            if root_model.count() == 0:
                logger.info("No root model element found")
                return ""

            root_text = root_model.inner_text()

            # Handle array at root level
            if root_text.strip().startswith('['):
                logger.info("Detected array at root level")

                # Find the inner model within the array
                inner_model = root_model.locator('xpath=.//span[@class="inner-object"]').first

                if inner_model.count() > 0:
                    # Extract the array item structure
                    item_structure = self._extract_model_structure(inner_model)
                    if item_structure:
                        # Wrap in array structure
                        array_result = {
                            "type": "array",
                            "items": json.loads(item_structure)
                        }
                        return json.dumps(array_result, indent=2)
                else:
                    # Simple array type
                    prop_type_span = root_model.locator('xpath=.//span[@class="prop-type"]').first
                    if prop_type_span.count() > 0:
                        item_type = prop_type_span.inner_text().strip()
                        array_result = {
                            "type": "array",
                            "items": {"type": item_type}
                        }
                        return json.dumps(array_result, indent=2)

                return ""

            # Handle object at root level
            else:
                logger.info("Detected object at root level")
                inner_object = model_container.locator('xpath=.//span[@class="inner-object"]').first

                if inner_object.count() > 0:
                    return self._extract_model_structure(inner_object)
                else:
                    logger.info("No inner-object found")
                    return ""

        except Exception as e:
            logger.error(f"Failed to extract model from container: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return ""

    def _extract_model_structure(self, element) -> str:
        """
        Helper method to extract model structure from inner-object element.
        Handles nested objects, arrays, required fields, examples, descriptions, and enums.

        Args:
            element: The inner-object element

        Returns:
            str: JSON representation of the model structure
        """
        try:
            import json
            model_dict = {}

            # Find all property rows (tr with class containing "property-row")
            property_rows = element.locator('xpath=.//tr[contains(@class, "property-row")]')
            count = property_rows.count()

            for i in range(count):
                row = property_rows.nth(i)

                # Get property name (first td)
                name_td = row.locator('xpath=.//td[1]')
                if name_td.count() == 0:
                    continue

                prop_name = name_td.inner_text().strip()
                # Remove the * from required fields
                prop_name = prop_name.replace('*', '').strip()

                # Check if required (class contains "required")
                is_required = "required" in row.get_attribute('class')

                # Get property type (second td)
                type_td = row.locator('xpath=.//td[2]')
                if type_td.count() == 0:
                    continue

                prop_info = {}
                if is_required:
                    prop_info["required"] = True

                # Check if it's an array (starts with [)
                type_text = type_td.inner_text()
                is_array = type_text.strip().startswith('[')

                if is_array:
                    prop_info["type"] = "array"
                    # Extract array item type
                    array_item = self._extract_array_item(type_td)
                    if array_item:
                        prop_info["items"] = array_item
                else:
                    # Check if it's a nested object
                    nested_object = type_td.locator('xpath=.//span[@class="model"]//span[@class="inner-object"]')
                    if nested_object.count() > 0:
                        prop_info["type"] = "object"
                        # Recursively extract nested object
                        nested_json = self._extract_model_structure(nested_object)
                        if nested_json:
                            prop_info["properties"] = json.loads(nested_json)
                    else:
                        # Simple type
                        prop_type_span = type_td.locator('xpath=.//span[@class="prop-type"]')
                        if prop_type_span.count() > 0:
                            prop_type = prop_type_span.inner_text().strip()
                            prop_info["type"] = prop_type

                            # Check for format
                            prop_format_span = type_td.locator('xpath=.//span[@class="prop-format"]')
                            if prop_format_span.count() > 0:
                                prop_format = prop_format_span.inner_text().strip()
                                prop_info["format"] = prop_format

                # Extract example if present (multiple formats)
                example_span = type_td.locator('xpath=.//span[@class="property primitive"]')
                if example_span.count() > 0:
                    example_text = example_span.inner_text().strip()
                    if example_text:
                        # Handle "example: value" format
                        if "example:" in example_text.lower():
                            example_value = example_text.split("example:")[-1].strip()
                            prop_info["example"] = example_value
                        # Handle "xml:" or other metadata
                        elif "xml:" in example_text.lower():
                            prop_info["xml"] = example_text

                # Extract description if present
                description_div = type_td.locator('xpath=.//div[@class="markdown"]//p')
                if description_div.count() > 0:
                    description_text = description_div.inner_text().strip()
                    if description_text:
                        prop_info["description"] = description_text

                # Extract additional property metadata (xml, etc.)
                property_spans = type_td.locator('xpath=.//span[@class="property"]')
                if property_spans.count() > 0:
                    for j in range(property_spans.count()):
                        prop_meta = property_spans.nth(j).inner_text().strip()
                        if prop_meta and "xml:" in prop_meta.lower() and "xml" not in prop_info:
                            prop_info["xml_metadata"] = prop_meta

                # Extract enum if present
                enum_span = type_td.locator('xpath=.//span[@class="prop-enum"]')
                if enum_span.count() > 0:
                    enum_text = enum_span.inner_text().strip()
                    if enum_text and "Enum:" in enum_text:
                        # Extract enum values
                        enum_values = enum_text.split("Enum:")[-1].strip()
                        # Remove brackets and split
                        enum_values = enum_values.strip('[]').strip()
                        if enum_values:
                            prop_info["enum"] = [v.strip() for v in enum_values.split(',')]

                model_dict[prop_name] = prop_info

            return json.dumps(model_dict, indent=2)

        except Exception as e:
            logger.error(f"Failed to extract model structure: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return "{}"

    def _extract_array_item(self, type_td) -> dict:
        """
        Helper method to extract array item type information.

        Args:
            type_td: The type td element containing array information

        Returns:
            dict: Array item type information
        """
        try:
            import json
            item_info = {}

            # Check if array contains nested object
            nested_object = type_td.locator('xpath=.//span[@class="model"]//span[@class="inner-object"]')
            if nested_object.count() > 0:
                item_info["type"] = "object"
                # Recursively extract nested object
                nested_json = self._extract_model_structure(nested_object)
                if nested_json:
                    item_info["properties"] = json.loads(nested_json)
            else:
                # Simple type in array
                prop_type_span = type_td.locator('xpath=.//span[@class="prop-type"]')
                if prop_type_span.count() > 0:
                    prop_type = prop_type_span.inner_text().strip()
                    item_info["type"] = prop_type

                # Check for format
                prop_format_span = type_td.locator('xpath=.//span[@class="prop-format"]')
                if prop_format_span.count() > 0:
                    prop_format = prop_format_span.inner_text().strip()
                    item_info["format"] = prop_format

            return item_info

        except Exception as e:
            logger.error(f"Failed to extract array item: {str(e)}")
            return {}