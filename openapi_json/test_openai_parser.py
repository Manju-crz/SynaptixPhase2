"""
Test OpenAPI Parser - Demonstrates usage and exports to Excel
"""

import sys
import os
import logging

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from openapi_json.openapi_parser import OpenAPIParser
from ext_util.xl_util import create_excel_with_data

logging.basicConfig(
    level=logging.INFO,
    format='\n%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def test_openapi_parser(spec_url: str):
    """
    Test OpenAPI parser and export results to Excel

    Args:
        spec_url: URL to the OpenAPI specification JSON
    """
    try:
        logger.info("=" * 60)
        logger.info("OpenAPI Parser Test")
        logger.info("=" * 60)

        # Initialize parser
        parser = OpenAPIParser(spec_url)

        # Fetch the specification
        if not parser.fetch_spec():
            logger.error("Failed to fetch OpenAPI specification")
            return

        # Get API info
        info = parser.get_info()
        logger.info(f"\nAPI Information:")
        logger.info(f"  Title: {info.get('title', 'N/A')}")
        logger.info(f"  Version: {info.get('version', 'N/A')}")
        logger.info(f"  Description: {info.get('description', 'N/A')}")

        # Get tags
        tags = parser.get_tags()
        logger.info(f"\nTags/Components: {len(tags)}")
        for tag in tags:
            logger.info(f"  - {tag['name']}: {tag['description']}")

        # Extract all operations
        logger.info(f"\nExtracting all API operations...")
        operations = parser.get_all_operations()

        # Enrich with tag descriptions
        operations = parser.enrich_with_tag_descriptions(operations)

        logger.info(f"✅ Extracted {len(operations)} operations")

        # Display sample operations
        logger.info(f"\nSample Operations:")
        for i, op in enumerate(operations[:3]):
            logger.info(f"\n  Operation {i+1}:")
            logger.info(f"    Method: {op['Operation_Method']}")
            logger.info(f"    Path: {op['Operation_Path']}")
            logger.info(f"    Summary: {op['Operation_Summary']}")
            logger.info(f"    Component: {op['Component']}")
            if op['response_model_json']:
                logger.info(f"    Response Model: {op['response_model_json'][:100]}...")

        # Prepare data for Excel
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
            "example_value_json",
            "response_model_json"
        ]

        # Convert operations to rows
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
                op['example_value_json'],
                op['response_model_json']
            ]
            excel_data.append(row)

        # Export to Excel
        logger.info("\nExporting to Excel...")
        folder_path = os.path.join(PROJECT_ROOT, "Rest_API_Data")
        create_excel_with_data(folder_path, "OpenAPI_Data", "Data", columns, excel_data)

        logger.info("=" * 60)
        logger.info("✅ Test completed successfully!")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())


def main():
    """Main entry point"""

    # Common OpenAPI spec URLs
    default_specs = {
        "1": {
            "name": "Petstore (Swagger 2.0)",
            "url": "https://petstore.swagger.io/v2/swagger.json"
        },
        "2": {
            "name": "Petstore (OpenAPI 3.0)",
            "url": "https://petstore3.swagger.io/api/v3/openapi.json"
        }
    }

    print("\n" + "=" * 60)
    print("OpenAPI Parser Test")
    print("=" * 60)
    print("\nAvailable test APIs:")
    for key, spec in default_specs.items():
        print(f"  {key}. {spec['name']}")
        print(f"     {spec['url']}")
    print("\n  3. Custom URL")
    print("=" * 60)

    choice = input("\nSelect option (1-3): ").strip()

    if choice in default_specs:
        spec_url = default_specs[choice]["url"]
    elif choice == "3":
        spec_url = input("Enter OpenAPI spec URL: ").strip()
    else:
        print("Invalid choice. Using default (Petstore 2.0)")
        spec_url = default_specs["1"]["url"]

    test_openapi_parser(spec_url)


if __name__ == "__main__":
    main()