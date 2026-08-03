"""
Example usage of REST API Client Utility
"""

from rest_util import RestApiClient, get_request, post_request, put_request, patch_request, delete_request
from rest_util.config import BASE_URLS, DEFAULT_HEADERS


def example_1_simple_get_request():
    """Example 1: Simple GET request using convenience function"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Simple GET Request")
    print("="*80)

    url = f"{BASE_URLS['JSONPLACEHOLDER']}/posts/1"

    response = get_request(url)

    print(f"\n🔍 URL: {url}")
    print(f"📋 Status Code: {response.status_code}")
    print(f"⏱  Response Time: {response.elapsed_time:.2f}s")
    print(f"✅ Success: {response.is_success()}")
    print(f"📄 Response Data: {response.json_data}")


def example_2_get_with_params_and_headers():
    """Example 2: GET request with query parameters and headers"""
    print("\n" + "="*80)
    print("EXAMPLE 2: GET Request with Query Params & Headers")
    print("="*80)

    url = f"{BASE_URLS['JSONPLACEHOLDER']}/posts"

    params = {
        'userId': 1,
        '_limit': 3
    }

    headers = DEFAULT_HEADERS.copy()

    response = get_request(url, headers=headers, params=params)

    print(f"\n🔍 URL: {url}")
    print(f"📋 Query Params: {params}")
    print(f"📋 Status Code: {response.status_code}")
    print(f"📄 Number of Posts: {len(response.json_data)}")


def example_3_post_with_json_payload():
    """Example 3: POST request with JSON payload"""
    print("\n" + "="*80)
    print("EXAMPLE 3: POST Request with JSON Payload")
    print("="*80)

    url = f"{BASE_URLS['JSONPLACEHOLDER']}/posts"

    payload = {
        'title': 'New Post from Synaptix',
        'body': 'This is a test post created using REST API utility',
        'userId': 1
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = post_request(url, headers=headers, json_payload=payload)

    print(f"\n🔍 URL: {url}")
    print(f"📦 Payload: {payload}")
    print(f"📋 Status Code: {response.status_code}")
    print(f"📄 Created Resource: {response.json_data}")


def example_4_put_request():
    """Example 4: PUT request to update resource"""
    print("\n" + "="*80)
    print("EXAMPLE 4: PUT Request to Update Resource")
    print("="*80)

    url = f"{BASE_URLS['JSONPLACEHOLDER']}/posts/1"

    payload = {
        'id': 1,
        'title': 'Updated Title',
        'body': 'Updated body content',
        'userId': 1
    }

    response = put_request(url, json_payload=payload)

    print(f"\n🔍 URL: {url}")
    print(f"📦 Payload: {payload}")
    print(f"📋 Status Code: {response.status_code}")
    print(f"📄 Updated Resource: {response.json_data}")


def example_5_patch_request():
    """Example 5: PATCH request for partial update"""
    print("\n" + "="*80)
    print("EXAMPLE 5: PATCH Request for Partial Update")
    print("="*80)

    url = f"{BASE_URLS['JSONPLACEHOLDER']}/posts/1"

    payload = {
        'title': 'Partially Updated Title'
    }

    response = patch_request(url, json_payload=payload)

    print(f"\n🔍 URL: {url}")
    print(f"📦 Payload: {payload}")
    print(f"📋 Status Code: {response.status_code}")
    print(f"📄 Updated Resource: {response.json_data}")


def example_6_delete_request():
    """Example 6: DELETE request"""
    print("\n" + "="*80)
    print("EXAMPLE 6: DELETE Request")
    print("="*80)

    url = f"{BASE_URLS['JSONPLACEHOLDER']}/posts/1"

    response = delete_request(url)

    print(f"\n🔍 URL: {url}")
    print(f"📋 Status Code: {response.status_code}")
    print(f"✅ Success: {response.is_success()}")
    print(f"📄 Response: {response.json_data}")


def example_7_client_with_base_url():
    """Example 7: Using RestApiClient class with base URL"""
    print("\n" + "="*80)
    print("EXAMPLE 7: RestApiClient with Base URL (Reusable)")
    print("="*80)

    client = RestApiClient(base_url=BASE_URLS['JSONPLACEHOLDER'], default_headers=DEFAULT_HEADERS)

    print(f"\n🎯 Making multiple requests with same client:\n")

    response1 = client.get('/posts/1')
    print(f"  GET /posts/1 → Status: {response1.status_code}")

    response2 = client.get('/users/1')
    print(f"  GET /users/1 → Status: {response2.status_code}")

    response3 = client.get('/comments', params={'postId': 1, '_limit': 2})
    print(f"  GET /comments → Status: {response3.status_code}, Results: {len(response3.json_data)}")

    client.close()


def example_8_post_with_file_upload():
    """Example 8: POST request with file upload"""
    print("\n" + "="*80)
    print("EXAMPLE 8: POST Request with File Upload")
    print("="*80)

    url = f"{BASE_URLS['HTTPBIN']}/post"

    import io

    file_content = io.BytesIO(b"This is test file content from Synaptix REST utility")

    files = {
        'file': ('test_document.txt', file_content, 'text/plain')
    }

    data = {
        'description': 'Test file upload',
        'category': 'documents'
    }

    response = post_request(url, data=data, files=files)

    print(f"\n🔍 URL: {url}")
    print(f"📎 File: test_document.txt")
    print(f"📋 Status Code: {response.status_code}")
    print(f"✅ Success: {response.is_success()}")

    if response.json_data:
        print(f"📄 Files Uploaded: {list(response.json_data.get('files', {}).keys())}")


def example_9_error_handling():
    """Example 9: Error handling and response checks"""
    print("\n" + "="*80)
    print("EXAMPLE 9: Error Handling & Response Checks")
    print("="*80)

    url = f"{BASE_URLS['JSONPLACEHOLDER']}/posts/999999"

    response = get_request(url)

    print(f"\n🔍 URL: {url}")
    print(f"📋 Status Code: {response.status_code}")
    print(f"✅ Is Success (2xx): {response.is_success()}")
    print(f"⚠ Is Client Error (4xx): {response.is_client_error()}")
    print(f"❌ Is Server Error (5xx): {response.is_server_error()}")
    print(f"📄 Response Text: {response.text[:100]}")


def example_10_advanced_client_usage():
    """Example 10: Advanced usage with custom timeout and SSL verification"""
    print("\n" + "="*80)
    print("EXAMPLE 10: Advanced Client Configuration")
    print("="*80)

    client = RestApiClient(
        base_url=BASE_URLS['JSONPLACEHOLDER'],
        timeout=10,
        verify_ssl=True
    )

    response = client.post(
        '/posts',
        json_payload={
            'title': 'Advanced Post',
            'body': 'Created with advanced configuration',
            'userId': 1
        },
        params={'debug': 'true'},
        headers={'X-Custom-Header': 'CustomValue'}
    )

    print(f"\n📊 Status Code: {response.status_code}")
    print(f"⏱  Response Time: {response.elapsed_time:.2f}s")
    print(f"📄 Response Headers: {list(response.headers.keys())[:5]}")

    client.close()


if __name__ == "__main__":
    print("\n" + "🚀 REST API CLIENT UTILITY - EXAMPLES ".center(80, "="))

    try:
        example_1_simple_get_request()

        example_2_get_with_params_and_headers()

        example_3_post_with_json_payload()

        example_4_put_request()

        example_5_patch_request()

        example_6_delete_request()

        example_7_client_with_base_url()

        example_8_post_with_file_upload()

        example_9_error_handling()

        example_10_advanced_client_usage()

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*80)
    print("✅ Examples completed!")
    print("="*80 + "\n")