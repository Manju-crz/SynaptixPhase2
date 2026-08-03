"""
REST API Client Utility - Reusable methods for all HTTP operations
"""

import os
import logging
from typing import Dict, Optional, Any, List, Tuple, Union
import requests
from requests.models import Response

logging.basicConfig(
    level=logging.INFO,
    format='\n%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class ApiResponse:
    """
    Unified response object for all API calls
    """

    def __init__(self, response: Response):
        """
        Initialize API response wrapper.

        Args:
            response: requests.Response object
        """
        self.raw_response = response
        self.status_code = response.status_code
        self.headers = dict(response.headers)
        self.url = response.url
        self.elapsed_time = response.elapsed.total_seconds()

        try:
            self.json_data = response.json()
        except ValueError:
            self.json_data = None

        self.text = response.text
        self.ok = response.ok
        self.reason = response.reason

    def is_success(self) -> bool:
        """Check if request was successful (2xx status code)"""
        return 200 <= self.status_code < 300

    def is_client_error(self) -> bool:
        """Check if client error (4xx status code)"""
        return 400 <= self.status_code < 500

    def is_server_error(self) -> bool:
        """Check if server error (5xx status code)"""
        return 500 <= self.status_code < 600

    def __repr__(self):
        return f"ApiResponse(status={self.status_code}, url={self.url})"

    def __str__(self):
        return f"Status: {self.status_code} | URL: {self.url} | Time: {self.elapsed_time:.2f}s"


class RestApiClient:
    """
    REST API Client with reusable methods for all HTTP operations.
    Supports GET, POST, PUT, PATCH, DELETE with headers, query params, payloads, and file uploads.
    """

    def __init__(self, base_url: Optional[str] = None, default_headers: Optional[Dict[str, str]] = None,
                 timeout: int = 30, verify_ssl: bool = True):
        """
        Initialize REST API Client.

        Args:
            base_url: Base URL for all requests (optional)
            default_headers: Default headers to include in all requests
            timeout: Request timeout in seconds (default: 30)
            verify_ssl: Whether to verify SSL certificates (default: True)
        """
        self.base_url = base_url.rstrip('/') if base_url else ''
        self.default_headers = default_headers or {}
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session()

        logger.info(f"🔧 REST API Client initialized | Base URL: {self.base_url or 'None'}")

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from base URL and endpoint"""
        if endpoint.startswith('http://') or endpoint.startswith('https://'):
            return endpoint

        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}" if self.base_url else endpoint

    def _merge_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        """Merge default headers with request-specific headers"""
        merged = self.default_headers.copy()
        if headers:
            merged.update(headers)
        return merged

    def _log_request(self, method: str, url: str, headers: Dict, params: Optional[Dict],
                     payload: Optional[Any], files: Optional[Dict]):
        """Log request details"""
        logger.info(f"\n{'='*80}")
        logger.info(f"📦 REQUEST: {method} {url}")
        logger.info(f"{'='*80}")

        if headers:
            logger.info(f"📋 Request Headers:")
            for key, value in headers.items():
                logger.info(f"    {key}: {value}")

        if params:
            logger.info(f"🔍 Query Parameters:")
            for key, value in params.items():
                logger.info(f"    {key}: {value}")

        if payload:
            logger.info(f"📦 Request Body:")
            if isinstance(payload, dict):
                import json
                logger.info(json.dumps(payload, indent=2))
            else:
                logger.info(f"  {payload}")

        if files:
            logger.info(f"📎 Files: {list(files.keys())}")

    def _log_response(self, response: ApiResponse):
        """Log response details"""
        status_emoji = "✅" if response.is_success() else "❌"
        logger.info(f"\n{'='*80}")
        logger.info(f"{status_emoji} RESPONSE: {response.status_code} {response.reason} | Time: {response.elapsed_time:.2f}s")
        logger.info(f"{'='*80}")

        logger.info(f"📋 Response Headers:")
        for key, value in list(response.headers.items())[:10]:
            logger.info(f"    {key}: {value}")

        if response.json_data:
            logger.info(f"📦 Response Body (JSON):")
            import json
            logger.info(json.dumps(response.json_data, indent=2))
        elif response.text:
            logger.info(f"📄 Response Body (Text):")
            # Limit text output to first 500 characters
            text_preview = response.text[:500] + "..." if len(response.text) > 500 else response.text
            logger.info(f"  {text_preview}")

    def get(self, endpoint: str, headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, Any]] = None) -> ApiResponse:
        """
        Perform GET request.

        Args:
            endpoint: API endpoint or full URL
            headers: Request headers (merged with default headers)
            params: Query parameters

        Returns:
            ApiResponse object
        """
        url = self._build_url(endpoint)
        merged_headers = self._merge_headers(headers)

        self._log_request('GET', url, merged_headers, params, None, None)

        response = self.session.get(
            url,
            headers=merged_headers,
            params=params,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        api_response = ApiResponse(response)
        self._log_response(api_response)

        return api_response

    def post(self, endpoint: str, headers: Optional[Dict[str, str]] = None,
             params: Optional[Dict[str, Any]] = None, json_payload: Optional[Dict] = None,
             data: Optional[Any] = None, files: Optional[Dict[str, Tuple]] = None) -> ApiResponse:
        """
        Perform POST request.

        Args:
            endpoint: API endpoint or full URL
            headers: Request headers (merged with default headers)
            params: Query parameters
            json_payload: JSON payload (dict will be serialized to JSON)
            data: Form data or raw data
            files: Files to upload - Dict of {field_name: (filename, file_object, content_type)}
                   Example: {'file': ('test.txt', open('test.txt', 'rb'), 'text/plain')}
                   Or simplified: {'file': open('test.txt', 'rb')}

        Returns:
            ApiResponse object
        """
        url = self._build_url(endpoint)
        merged_headers = self._merge_headers(headers)

        if json_payload and 'Content-Type' not in merged_headers:
            merged_headers['Content-Type'] = 'application/json'

        self._log_request('POST', url, merged_headers, params, json_payload or data, files)

        response = self.session.post(
            url,
            headers=merged_headers if merged_headers else None,
            params=params,
            json=json_payload,
            data=data,
            files=files,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        api_response = ApiResponse(response)
        self._log_response(api_response)

        return api_response

    def put(self, endpoint: str, headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, Any]] = None, json_payload: Optional[Dict] = None,
            data: Optional[Any] = None, files: Optional[Dict[str, Tuple]] = None) -> ApiResponse:
        """
        Perform PUT request.

        Args:
            endpoint: API endpoint or full URL
            headers: Request headers (merged with default headers)
            params: Query parameters
            json_payload: JSON payload (dict will be serialized to JSON)
            data: Form data or raw data
            files: Files to upload - Dict of {field_name: (filename, file_object, content_type)}

        Returns:
            ApiResponse object
        """
        url = self._build_url(endpoint)
        merged_headers = self._merge_headers(headers)

        if json_payload and 'Content-Type' not in merged_headers:
            merged_headers['Content-Type'] = 'application/json'

        self._log_request('PUT', url, merged_headers, params, json_payload or data, files)

        response = self.session.put(
            url,
            headers=merged_headers if merged_headers else None,
            params=params,
            json=json_payload,
            data=data,
            files=files,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        api_response = ApiResponse(response)
        self._log_response(api_response)

        return api_response

    def patch(self, endpoint: str, headers: Optional[Dict[str, str]] = None,
              params: Optional[Dict[str, Any]] = None, json_payload: Optional[Dict] = None,
              data: Optional[Any] = None, files: Optional[Dict[str, Tuple]] = None) -> ApiResponse:
        """
        Perform PATCH request.

        Args:
            endpoint: API endpoint or full URL
            headers: Request headers (merged with default headers)
            params: Query parameters
            json_payload: JSON payload (dict will be serialized to JSON)
            data: Form data or raw data
            files: Files to upload - Dict of {field_name: (filename, file_object, content_type)}

        Returns:
            ApiResponse object
        """
        url = self._build_url(endpoint)
        merged_headers = self._merge_headers(headers)

        if json_payload and 'Content-Type' not in merged_headers:
            merged_headers['Content-Type'] = 'application/json'

        self._log_request('PATCH', url, merged_headers, params, json_payload or data, files)

        response = self.session.patch(
            url,
            headers=merged_headers if merged_headers else None,
            params=params,
            json=json_payload,
            data=data,
            files=files,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        api_response = ApiResponse(response)
        self._log_response(api_response)

        return api_response

    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None,
               params: Optional[Dict[str, Any]] = None, json_payload: Optional[Dict] = None) -> ApiResponse:
        """
        Perform DELETE request.

        Args:
            endpoint: API endpoint or full URL
            headers: Request headers (merged with default headers)
            params: Query parameters
            json_payload: JSON payload (optional, some DELETE requests accept body)

        Returns:
            ApiResponse object
        """
        url = self._build_url(endpoint)
        merged_headers = self._merge_headers(headers)

        if json_payload and 'Content-Type' not in merged_headers:
            merged_headers['Content-Type'] = 'application/json'

        self._log_request('DELETE', url, merged_headers, params, json_payload, None)

        response = self.session.delete(
            url,
            headers=merged_headers if merged_headers else None,
            params=params,
            json=json_payload,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        api_response = ApiResponse(response)
        self._log_response(api_response)

        return api_response

    def close(self):
        """Close the session"""
        self.session.close()
        logger.info("🔒 REST API Client session closed")


def get_request(url: str, headers: Optional[Dict[str, str]] = None,
                params: Optional[Dict[str, Any]] = None, timeout: int = 30,
                verify_ssl: bool = True) -> ApiResponse:
    """
    Convenience function for GET request without creating client instance.

    Args:
        url: Full URL
        headers: Request headers
        params: Query parameters
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates

    Returns:
        ApiResponse object
    """
    client = RestApiClient(timeout=timeout, verify_ssl=verify_ssl)
    response = client.get(url, headers=headers, params=params)
    client.close()
    return response


def post_request(url: str, headers: Optional[Dict[str, str]] = None,
                 params: Optional[Dict[str, Any]] = None, json_payload: Optional[Dict] = None,
                 data: Optional[Any] = None, files: Optional[Dict[str, Tuple]] = None,
                 timeout: int = 30, verify_ssl: bool = True) -> ApiResponse:
    """
    Convenience function for POST request without creating client instance.

    Args:
        url: Full URL
        headers: Request headers
        params: Query parameters
        json_payload: JSON payload
        data: Form data or raw data
        files: Files to upload
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates

    Returns:
        ApiResponse object
    """
    client = RestApiClient(timeout=timeout, verify_ssl=verify_ssl)
    response = client.post(url, headers=headers, params=params, json_payload=json_payload,
                           data=data, files=files)
    client.close()
    return response


def put_request(url: str, headers: Optional[Dict[str, str]] = None,
                params: Optional[Dict[str, Any]] = None, json_payload: Optional[Dict] = None,
                data: Optional[Any] = None, files: Optional[Dict[str, Tuple]] = None,
                timeout: int = 30, verify_ssl: bool = True) -> ApiResponse:
    """
    Convenience function for PUT request without creating client instance.

    Args:
        url: Full URL
        headers: Request headers
        params: Query parameters
        json_payload: JSON payload
        data: Form data or raw data
        files: Files to upload
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates

    Returns:
        ApiResponse object
    """
    client = RestApiClient(timeout=timeout, verify_ssl=verify_ssl)
    response = client.put(url, headers=headers, params=params, json_payload=json_payload,
                          data=data, files=files)
    client.close()
    return response


def patch_request(url: str, headers: Optional[Dict[str, str]] = None,
                  params: Optional[Dict[str, Any]] = None, json_payload: Optional[Dict] = None,
                  data: Optional[Any] = None, files: Optional[Dict[str, Tuple]] = None,
                  timeout: int = 30, verify_ssl: bool = True) -> ApiResponse:
    """
    Convenience function for PATCH request without creating client instance.

    Args:
        url: Full URL
        headers: Request headers
        params: Query parameters
        json_payload: JSON payload
        data: Form data or raw data
        files: Files to upload
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates

    Returns:
        ApiResponse object
    """
    client = RestApiClient(timeout=timeout, verify_ssl=verify_ssl)
    response = client.patch(url, headers=headers, params=params, json_payload=json_payload,
                            data=data, files=files)
    client.close()
    return response


def delete_request(url: str, headers: Optional[Dict[str, str]] = None,
                   params: Optional[Dict[str, Any]] = None, json_payload: Optional[Dict] = None,
                   timeout: int = 30, verify_ssl: bool = True) -> ApiResponse:
    """
    Convenience function for DELETE request without creating client instance.

    Args:
        url: Full URL
        headers: Request headers
        params: Query parameters
        json_payload: JSON payload (optional)
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates

    Returns:
        ApiResponse object
    """
    client = RestApiClient(timeout=timeout, verify_ssl=verify_ssl)
    response = client.delete(url, headers=headers, params=params, json_payload=json_payload)
    client.close()
    return response