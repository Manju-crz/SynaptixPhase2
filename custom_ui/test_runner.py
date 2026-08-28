"""
Test Runner - Executes Playwright tests from UI
"""

import sys
import os
import json
import tempfile
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from swagger.browser_utils import BrowserUtils
from swagger.swagger_page import SwaggerPage
from openapi_json.openai_parser import OpenAPIParser
from ext_util import create_excel_with_data

logging.basicConfig(
    level=logging.INFO,
    format='\n%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

columns = [
    "Sl_No",
    "Component",
    "Component_SmallDescription",
    "Operation_Method",
    "Operation_Path",
    "Operation_Summary",
    "Operation_SecondarySummary",
    "header_parameters",
    "query_parameters",
    "path_parameters",
    "form_data_parameters",
    "request_content_type",
    "request_body_json",
    "standard_response_model"
]


def run_swagger_scraper(url: str, filename_prefix: str = "Swagger_Data") -> dict:
    """
    Run the Swagger page test with the provided URL.

    Args:
        url: The URL to navigate to

    Returns:
        dict: Result with success status and message
    """
    browser_utils = BrowserUtils()
    logs = []

    try:
        logs.append(f"Launching browser...")
        page = browser_utils.launch_browser(headless=True)
        logs.append(f"Navigating to: {url}")
        browser_utils.navigate_to_url(url)
        logs.append(f"Page Title: {page.title()}")
        logs.append(f"Page URL: {page.url}")
        # Verify Swagger UI using page object
        swagger_page = SwaggerPage(page)
        if swagger_page.verify_swagger_ui_visible():
            logs.append("✅ Swagger UI element is visible")
        else:
            logs.append("ℹ️ No Swagger UI element found (may not be a Swagger page)")

        tag_data = swagger_page.get_h3_tag_data()

        # Dictionary to store h3 component name and description
        components = {}
        # It just holders the component names list Components: ['pet', 'store', 'user'] along with their smaller descriptions
        for tag, is_open in tag_data.items():
            if is_open == "false":
                swagger_page.expand_h3_tag(tag)
            description = swagger_page.get_h3_small_description(tag)
            components[tag] = description
        logs.append(f"✅ Collected {len(components)} tag descriptions")

        # Dictionary to store API operations for each component
        api_operations = {}  # It just holders the basci API operations for each component like:
        # {'pet': [{'method': 'POST', 'path': '/pet/{petId}/uploadImage', 'summary': 'uploads an image', 'expanded': 'false'},
        for tag in components.keys():
            operations = swagger_page.get_api_operations_basics(tag)
            api_operations[tag] = operations
        logs.append(f"✅ Collected API operations for {len(api_operations)} components")

        # Get operation body section for each API operation and update api_operations dictionary
        for tag, operations in api_operations.items():
            for operation in operations:
                try:
                    body_section = swagger_page.get_operation_section_by_details(
                        tag,
                        operation['method'],
                        operation['path']
                    )
                    operation['body_element'] = body_section
                    logs.append(f"Got body section for {operation['method']} {operation['path']}")
                except Exception as e:
                    logs.append(f"Failed to get body section for {operation['method']} {operation['path']}: {str(e)}")
                    operation['body_element'] = None

        # Prepare data for Excel export
        excel_data = []
        sl_no = 1

        for tag, operations in api_operations.items():
            # Get the component description
            component_description = components.get(tag, "")

            # Create a row for each operation
            for operation in operations:
                # Get operation description text if body_element exists
                secondary_summary = ""
                header_params = ""
                query_params = ""
                path_params = ""
                form_data_params = ""
                example_json = ""
                standard_response_model = ""

                if operation.get('body_element'):
                    secondary_summary = swagger_page.get_operation_description_text(operation['body_element'])
                    header_params = swagger_page.get_header_parameters(operation['body_element'])
                    query_params = swagger_page.get_query_parameters(operation['body_element'])
                    path_params = swagger_page.get_path_parameters(operation['body_element'])
                    form_data_params = swagger_page.get_form_data_parameters(operation['body_element'])
                    example_json = swagger_page.get_request_body_json(tag, operation['method'], operation['path'])
                    standard_response_model = swagger_page.get_standard_response_model(tag, operation['method'], operation['path'])

                row = [
                    sl_no,
                    tag,
                    component_description,
                    operation['method'],
                    operation['path'],
                    operation['summary'],
                    secondary_summary,  # Operation_SecondarySummary
                    header_params,
                    query_params,
                    path_params,
                    form_data_params,
                    example_json,
                    standard_response_model
                ]
                excel_data.append(row)
                sl_no += 1

        logs.append(f"✅ Prepared {len(excel_data)} rows for Excel export")

        # Create Excel file and write data
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder_path = os.path.join(PROJECT_ROOT, "Rest_API_Data")
        file_path = create_excel_with_data(folder_path, filename_prefix, "Data", columns, excel_data)
        logs.append(f"✅ Excel file created: {file_path}")

        # Remove body_element from api_operations before returning (not JSON serializable)
        for tag, operations in api_operations.items():
            for operation in operations:
                if 'body_element' in operation:
                    del operation['body_element']

        return {
            'success': True,
            'message': 'Swagger scraping completed successfully',
            'logs': logs,
            'pageTitle': page.title(),
            'pageUrl': page.url,
            'tagDescriptions': components,
            'apiOperations': api_operations,
            'excelFilePath': file_path
        }

    except Exception as e:
        logs.append(f"❌ Error: {str(e)}")
        return {
            'success': False,
            'message': str(e),
            'logs': logs
        }

    finally:
        browser_utils.close_browser()
        logs.append("Browser closed")


def run_openapi_json_parser(spec_url: str = None, spec_content: str = None, filename: str = None, filename_prefix: str = "OpenAPI_Data") -> dict:
    """
    Run the OpenAPI JSON parser with either a spec URL or raw JSON file content.

    Args:
        spec_url: The URL to the OpenAPI/Swagger JSON specification
        spec_content: Raw JSON content of the OpenAPI/Swagger specification
        filename: Optional filename for the uploaded spec (for logging)

    Returns:
        dict: Result with success status and message
    """
    logs = []
    temp_file_path = None

    try:
        logs.append(f"Initializing OpenAPI parser...")

        # Determine the source for the parser
        if spec_content:
            # Save uploaded JSON content to a temporary file
            temp_dir = tempfile.gettempdir()
            display_name = filename or "uploaded_openapi.json"
            temp_file_path = os.path.join(temp_dir, display_name)

            logs.append(f"Saving uploaded spec content to temporary file: {temp_file_path}")
            with open(temp_file_path, 'w', encoding='utf-8') as f:
                f.write(spec_content)

            parser = OpenAPIParser(temp_file_path, source_type='file')
            logs.append(f"Loading OpenAPI spec from uploaded file: {display_name}")
        elif spec_url:
            parser = OpenAPIParser(spec_url)
            logs.append(f"Fetching OpenAPI spec from: {spec_url}")
        else:
            return {
                'success': False,
                'message': 'Either spec_url or spec_content must be provided',
                'logs': logs
            }

        if not parser.fetch_spec():
            return {
                'success': False,
                'message': 'Failed to fetch/load OpenAPI specification',
                'logs': logs
            }

        # Get API info
        info = parser.get_info()
        logs.append(f"API: {info.get('title', 'N/A')} v{info.get('version', 'N/A')}")

        # Get tags
        tags = parser.get_tags()
        logs.append(f"Found {len(tags)} components/tags")

        # Extract all operations
        logs.append("Extracting all API operations...")
        operations = parser.get_all_operations()

        # Enrich with tag descriptions
        operations = parser.enrich_with_tag_descriptions(operations)
        logs.append(f"✅ Extracted {len(operations)} operations")

        # Prepare data for Excel
        excel_data = []
        for op in operations:
            row = [
                op['Sl_No'],
                op['Component'],
                op['Component_SmallDescription'],
                op['Operation_Method'],
                op['Operation_Path'],
                op['Operation_Summary'],
                op['Operation_SecondarySummary'],
                op['header_parameters'],
                op['query_parameters'],
                op['path_parameters'],
                op['form_data_parameters'],
                op['request_content_type'],
                op['request_body_json'],
                op['standard_response_model']
            ]
            excel_data.append(row)

        logs.append(f"✅ Prepared {len(excel_data)} rows for Excel export")

        # Create Excel file
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder_path = os.path.join(PROJECT_ROOT, "Rest_API_Data")
        file_path = create_excel_with_data(folder_path, filename_prefix, "Data", columns, excel_data)
        logs.append(f"✅ Excel file created: {file_path}")

        return {
            'success': True,
            'message': 'OpenAPI JSON parsing completed successfully',
            'logs': logs,
            'apiTitle': info.get('title', 'N/A'),
            'apiVersion': info.get('version', 'N/A'),
            'operationCount': len(operations),
            'excelFilePath': file_path
        }

    except Exception as e:
        logs.append(f"❌ Error: {str(e)}")
        return {
            'success': False,
            'message': str(e),
            'logs': logs
        }
    finally:
        # Clean up temporary uploaded spec file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception:
                pass