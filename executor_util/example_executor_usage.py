"""
Example usage of API Executor Utility
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from executor_util.executor_util import ApiExecutor, execute_single_query, execute_multiple_queries_batch
from rest_util.config import BASE_URLS

EXCEL_BASE_PATH = r"C:\BLKDeveloper\Synaptix\Rest_API_Data"


def get_base_url_from_user():
    """
    Prompt user to select or enter a base URL.

    Returns:
        str: Selected or entered base URL
    """
    print("\n" + "="*80)
    print("🌐 BASE URL CONFIGURATION")
    print("="*80)
    print("\n⚠️ PLEASE SELECT A BASE URL TO CONTINUE")
    print("\nAvailable predefined URLs:")

    for i, (key, url) in enumerate(BASE_URLS.items(), 1):
        print(f"  {i}. {key:20s} -> {url}")

    print(f"  {len(BASE_URLS) + 1}. Custom URL (enter manually)")
    print("\n" + "-"*80)

    while True:
        try:
            print("\n👉 ENTER YOUR CHOICE NOW:")
            choice = input(f"Select option (1-{len(BASE_URLS) + 1}) or press Enter for default [PETSTORE]: ").strip()

            if choice == "":
                base_url = BASE_URLS['PETSTORE']
                print(f"  ✅ Using default: {base_url}")
                return base_url

            choice_num = int(choice)

            if 1 <= choice_num <= len(BASE_URLS):
                key = list(BASE_URLS.keys())[choice_num - 1]
                base_url = BASE_URLS[key]
                print(f"  ✅ Selected: {key} -> {base_url}")
                return base_url
            elif choice_num == len(BASE_URLS) + 1:
                custom_url = input("Enter custom base URL: ").strip()
                if custom_url:
                    print(f"  ✅ Using custom URL: {custom_url}")
                    return custom_url
                else:
                    print("  ❌ Invalid URL. Please try again.")
            else:
                print(f"  ❌ Invalid choice. Please select 1-{len(BASE_URLS) + 1}")
        except ValueError:
            print("  ❌ Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user.")
            exit(0)


def get_excel_file_from_user():
    """
    Prompt user to select or enter an Excel filename.

    Returns:
        str: Full path to the selected Excel file
    """
    print("\n" + "="*80)
    print("📁 EXCEL FILE SELECTION")
    print("="*80)
    print("\n⚠️ PLEASE SELECT AN EXCEL FILE TO CONTINUE")

    try:
        files = [f for f in os.listdir(EXCEL_BASE_PATH) if f.endswith('.xlsx')]
        files.sort(reverse=True)

        if not files:
            print(f"\n❌ No Excel files found in {EXCEL_BASE_PATH}")
            exit(1)

        print("\nAvailable Excel files:")
        for i, filename in enumerate(files, 1):
            file_path = os.path.join(EXCEL_BASE_PATH, filename)
            file_size = os.path.getsize(file_path) / 1024
            print(f"  {i}. {filename} ({file_size:.1f} KB)")

        print(f"  {len(files) + 1}. Enter custom filename")
        print("\n" + "-"*80)

    except Exception as e:
        print(f"\n❌ Error listing files: {e}")
        exit(1)

    while True:
        try:
            print("\n👉 ENTER YOUR CHOICE NOW:")
            choice = input(f"Select option (1-{len(files) + 1}) or press Enter for latest file [{files[0]}]: ").strip()

            if choice == "":
                selected_file = files[0]
                print(f"  ✅ Using latest file: {selected_file}")
                return os.path.join(EXCEL_BASE_PATH, selected_file)

            choice_num = int(choice)

            if 1 <= choice_num <= len(files):
                selected_file = files[choice_num - 1]
                print(f"  ✅ Selected: {selected_file}")
                return os.path.join(EXCEL_BASE_PATH, selected_file)
            elif choice_num == len(files) + 1:
                custom_filename = input("Enter Excel filename: ").strip()
                if custom_filename:
                    custom_path = os.path.join(EXCEL_BASE_PATH, custom_filename)
                    if os.path.exists(custom_path):
                        print(f"  ✅ Using custom file: {custom_filename}")
                        return custom_path
                    else:
                        print(f"  ❌ File not found: {custom_path}")
                        print(f"     Please ensure the file exists in {EXCEL_BASE_PATH}")
                else:
                    print("  ❌ Filename cannot be empty. Please try again.")
            else:
                print(f"  ❌ Invalid choice. Please select 1-{len(files) + 1}")
        except ValueError:
            print("  ❌ Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user.")
            exit(0)


def get_queries_from_user():
    """
    Prompt user to enter natural language queries.

    Returns:
        list: List of query strings
    """
    print("\n" + "="*80)
    print("💬 QUERY INPUT")
    print("="*80)
    print("\n⚠️ ENTER YOUR NATURAL LANGUAGE QUERIES")
    print("\nYou can enter:")
    print("  • Single query: Just type one query and press Enter")
    print("  • Multiple queries: Type queries separated by semicolon (;)")
    print("\nExamples:")
    print("  Single:   Create a new pet in the pet store")
    print("  Multiple: Create a new pet; Update pet information; Delete a pet")
    print("\n" + "-"*80)

    while True:
        try:
            print("\n👉 ENTER YOUR QUERY/QUERIES NOW:")
            user_input = input("Query: ").strip()

            if not user_input:
                print("  ❌ Query cannot be empty. Please try again.")
                continue

            if ';' in user_input:
                queries = [q.strip() for q in user_input.split(';') if q.strip()]
                print(f"\n  ✅ Received {len(queries)} queries:")
                for i, q in enumerate(queries, 1):
                    print(f"    {i}. {q}")
                return queries
            else:
                print(f"\n  ✅ Received query: {user_input}")
                return [user_input]

        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user.")
            exit(0)


def example_1_single_query_execution(base_url, excel_path):
    """Example 1: Execute single API call using natural language"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Single Query Execution")
    print("="*80)

    query = "Create a new pet in the pet store"

    result = execute_single_query(
        excel_path=excel_path,
        base_url=base_url,
        query=query
    )

    print(f"\n📊 Execution Result:")
    print(f"   Success: {result['success']}")
    print(f"   Query: {result['query']}")
    print(f"   Sl_No: {result.get('sl_no')}")
    print(f"   Method: {result.get('method')}")
    print(f"   Endpoint: {result.get('endpoint')}")
    print(f"   Status Code: {result.get('status_code')}")
    print(f"   Response Time: {result.get('response_time', 0):.2f}s")

    if result.get('response_data'):
        print(f"   Response Data: {result['response_data']}")


def example_2_multiple_queries_execution(base_url, excel_path):
    """Example 2: Execute multiple API calls from list of queries"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Multiple Queries Execution")
    print("="*80)

    queries = [
        "Create a new pet in the pet store",
        "Update an existing pet",
        "Find pet by ID",
        "Delete a pet"
    ]

    results = execute_multiple_queries_batch(
        excel_path=excel_path,
        base_url=base_url,
        queries=queries
    )

    print(f"\n📊 Execution Summary:")
    print(f"   Total Queries: {len(results)}")
    print(f"   Successful: {sum(1 for r in results if r['success'])}")
    print(f"   Failed: {sum(1 for r in results if not r['success'])}")

    print(f"\n📄 Results:")
    for i, result in enumerate(results, 1):
        print(f"\n   Query {i}: {result['query']}")
        print(f"   Sl_No: {result.get('sl_no')}")
        print(f"   Method: {result.get('method')}")
        print(f"   Endpoint: {result.get('endpoint')}")
        print(f"   Status: {result.get('status_code')}")
        print(f"   Success: {'✅' if result['success'] else '❌'}")


def example_3_executor_with_custom_config(base_url, excel_path):
    """Example 3: Using ApiExecutor class with custom configuration"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Custom Executor Configuration")
    print("="*80)

    search_columns = [
        'Component', 'Component_SmallDescription', 'Operation_Method',
        'Operation_Path', 'Operation_Summary', 'Operation_SecondarySummary'
    ]

    executor = ApiExecutor(
        excel_path=excel_path,
        base_url=base_url,
        search_columns=search_columns,
        default_timeout=60
    )

    queries = [
        "Add a new pet to the store",
        "Get pet details by ID"
    ]

    print(f"\n🔍 Executing {len(queries)} queries with custom config:")

    for query in queries:
        result = executor.execute_api_call(query)

        print(f"\n   Query: {result['query']}")
        print(f"   Sl_No: {result.get('sl_no')}")
        print(f"   {result.get('method')} {result.get('endpoint')}")
        print(f"   Status: {result.get('status_code')} | Time: {result.get('response_time', 0):.2f}s")

        if result.get('request_details'):
            details = result['request_details']
            if details.get('header_params'):
                print(f"   Headers: {details['header_params']}")
            if details.get('query_params'):
                print(f"   Query Params: {details['query_params']}")
            if details.get('json_payload'):
                print(f"   Payload: {details['json_payload']}")

    executor.close()


def example_4_detailed_response_inspection(base_url, excel_path):
    """Example 4: Inspect detailed API response"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Detailed Response Inspection")
    print("="*80)

    executor = ApiExecutor(
        excel_path=excel_path,
        base_url=base_url
    )

    query = "Find pet by status available"

    result = executor.execute_api_call(query)

    print(f"\n📊 Detailed Result for: '{query}'")
    print(f"\n🔍 Search Result:")
    print(f"   Matched Sl_No: {result.get('sl_no')}")

    print(f"\n📤 Request Details:")
    print(f"   Method: {result.get('method')}")
    print(f"   Endpoint: {result.get('endpoint')}")

    if result.get('request_details'):
        req = result['request_details']
        print(f"   Header Params: {req.get('header_params') or 'None'}")
        print(f"   Query Params: {req.get('query_params') or 'None'}")
        print(f"   Path Params: {req.get('path_params') or 'None'}")
        print(f"   Form Params: {req.get('form_params') or 'None'}")
        print(f"   JSON Payload: {req.get('json_payload') or 'None'}")

    print(f"\n📥 Response Details:")
    print(f"   Status Code: {result.get('status_code')}")
    print(f"   Response Time: {result.get('response_time', 0):.2f}s")
    print(f"   Success: {result['success']}")

    if result.get('response_data'):
        print(f"   Response Data Type: {type(result['response_data']).__name__}")
        if isinstance(result['response_data'], list):
            print(f"   Response Items Count: {len(result['response_data'])}")
            if result['response_data']:
                print(f"   First Item: {result['response_data'][0]}")
        else:
            print(f"   Response Data: {result['response_data']}")

    if result.get('headers'):
        print(f"\n📑 Response Headers:")
        for key, value in list(result['headers'].items())[:5]:
            print(f"   {key}: {value}")

    executor.close()


def example_5_error_handling(base_url, excel_path):
    """Example 5: Error handling for invalid queries"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Error Handling")
    print("="*80)

    executor = ApiExecutor(
        excel_path=excel_path,
        base_url=base_url
    )

    queries = [
        "Create a new pet in the pet store",
        "This query will not match anything in the database xyz123",
        "Update pet information"
    ]

    print(f"\n🔍 Testing error handling with {len(queries)} queries:")

    for i, query in enumerate(queries, 1):
        result = executor.execute_api_call(query)

        print(f"\n   Query {i}: {result['query'][:50]}...")

        if result['success']:
            print(f"   ✅ Success - Sl_No: {result['sl_no']}, Status: {result['status_code']}")
        else:
            print(f"   ❌ Failed - Error: {result.get('error')}")
            if result.get('sl_no'):
                print(f"      Sl_No: {result['sl_no']}")

    executor.close()


if __name__ == "__main__":
    print("\n" + "🚀 API EXECUTOR UTILITY ".center(80, "="))

    # Get Excel file from user
    excel_path = get_excel_file_from_user()

    # Get base URL from user
    base_url = get_base_url_from_user()

    # Get queries from user
    queries = get_queries_from_user()

    print("\n" + "="*80)
    print(f"📁 Excel File: {os.path.basename(excel_path)}")
    print(f"🌐 Base URL: {base_url}")
    print(f"📝 Total Queries: {len(queries)}")
    print("="*80)

    try:
        # Initialize executor
        executor = ApiExecutor(
            excel_path=excel_path,
            base_url=base_url
        )

        # Execute queries
        print("\n" + "="*80)
        print("🚀 EXECUTING QUERIES")
        print("="*80)

        results = []
        for i, query in enumerate(queries, 1):
            print(f"\n{'-'*80}")
            print(f"Query {i}/{len(queries)}: {query}")
            print(f"{'-'*80}")

            result = executor.execute_api_call(query)
            results.append(result)

            # Display result
            if result['success']:
                print(f"\n✅ SUCCESS")
                print(f"   Sl_No: {result.get('sl_no')}")
                print(f"   Method: {result.get('method')}")
                print(f"   Endpoint: {result.get('endpoint')}")
                print(f"   Status Code: {result.get('status_code')}")
                print(f"   Response Time: {result.get('response_time', 0):.2f}s")

                if result.get('response_data'):
                    print(f"\n   📄 Response Data:")
                    if isinstance(result['response_data'], list):
                        print(f"      Type: List with {len(result['response_data'])} items")
                        if result['response_data'] and len(result['response_data']) > 0:
                            print(f"      First Item: {result['response_data'][0]}")
                    elif isinstance(result['response_data'], dict):
                        print(f"      Type: Dictionary")
                        for key, value in list(result['response_data'].items())[:5]:
                            print(f"      {key}: {value}")
                    else:
                        print(f"      {result['response_data']}")
            else:
                print(f"\n❌ FAILED")
                print(f"   Error: {result.get('error')}")
                if result.get('sl_no'):
                    print(f"   Sl_No: {result.get('sl_no')}")
                if result.get('method'):
                    print(f"   Method: {result.get('method')}")
                if result.get('endpoint'):
                    print(f"   Endpoint: {result.get('endpoint')}")

        # Summary
        print("\n" + "="*80)
        print("📊 EXECUTION SUMMARY")
        print("="*80)
        print(f"   Total Queries: {len(results)}")
        print(f"   Successful: {sum(1 for r in results if r['success'])}")
        print(f"   Failed: {sum(1 for r in results if not r['success'])}")

        executor.close()

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*80)
    print("✅ Execution completed!")
    print("="*80 + "\n")