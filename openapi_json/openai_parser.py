"""
OpenAPI/Swagger JSON Parser Utility
Parses OpenAPI specifications directly from JSON/YAML without UI scraping
"""

import json
import logging
import requests
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin

logging.basicConfig(
    level=logging.INFO,
    format='\n%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class OpenAPIParser:
    """Parser for OpenAPI/Swagger specifications"""

    def __init__(self, spec_url: str):
        """
        Initialize parser with OpenAPI spec URL

        Args:
            spec_url: URL to the OpenAPI JSON/YAML specification
        """
        self.spec_url = spec_url
        self.spec = None
        self.base_url = None

    def fetch_spec(self) -> bool:
        """
        Fetch the OpenAPI specification from the URL

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info(f"Fetching OpenAPI spec from: {self.spec_url}")
            response = requests.get(self.spec_url, timeout=30)
            response.raise_for_status()

            self.spec = response.json()
            logger.info(f"✅ Successfully fetched OpenAPI spec")

            # Extract base URL if available
            if 'servers' in self.spec and self.spec['servers']:
                self.base_url = self.spec['servers'][0].get('url', '')
            elif 'host' in self.spec:
                scheme = self.spec.get('schemes', ['https'])[0]
                base_path = self.spec.get('basePath', '')
                self.base_url = f"{scheme}://{self.spec['host']}{base_path}"

            logger.info(f"Base URL: {self.base_url}")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch OpenAPI spec: {str(e)}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {str(e)}")
            return False

    def get_info(self) -> Dict[str, Any]:
        """
        Get API information (title, version, description)

        Returns:
            dict: API information
        """
        if not self.spec:
            return {}

        return self.spec.get('info', {})

    def get_tags(self) -> List[Dict[str, str]]:
        """
        Get all tags/components from the spec

        Returns:
            list: List of tags with name and description
        """
        if not self.spec:
            return []

        tags = []
        for tag in self.spec.get('tags', []):
            tags.append({
                'name': tag.get('name', ''),
                'description': tag.get('description', '')
            })

        logger.info(f"Found {len(tags)} tags")
        return tags

    def extract_parameters(self, parameters: List[Dict]) -> Dict[str, str]:
        """
        Extract and format parameters by location

        Args:
            parameters: List of parameter objects

        Returns:
            dict: Parameters grouped by location as JSON strings
        """
        import json

        result = {
            'header': [],
            'query': [],
            'path': [],
            'formData': []
        }

        for param in parameters:
            param_in = param.get('in', '')
            if param_in not in result:
                continue

            param_dict = {
                'name': param.get('name', ''),
                'required': param.get('required', False),
            }

            # Add type
            param_type = param.get('type', param.get('schema', {}).get('type', ''))
            if param_type:
                param_dict['type'] = param_type

            # Add description
            description = param.get('description', '')
            if description:
                param_dict['description'] = description

            result[param_in].append(param_dict)

        # Convert lists to JSON strings
        return {
            'header_parameters': json.dumps(result['header']) if result['header'] else '',
            'query_parameters': json.dumps(result['query']) if result['query'] else '',
            'path_parameters': json.dumps(result['path']) if result['path'] else '',
            'form_data_parameters': json.dumps(result['formData']) if result['formData'] else ''
        }

    def extract_request_body_schema(self, request_body: Dict, parameters: List[Dict] = None) -> str:
        """
        Extract request body schema as JSON
        Handles both OpenAPI 3.0 (requestBody) and Swagger 2.0 (body parameter)

        Args:
            request_body: Request body object from OpenAPI 3.0 spec
            parameters: Parameters list (for Swagger 2.0 body parameter)

        Returns:
            str: JSON representation of the schema
        """
        try:
            # OpenAPI 3.0 structure: requestBody.content
            if request_body:
                content = request_body.get('content', {})

                # Try common content types
                for content_type in ['application/json', 'application/xml', '*/*']:
                    if content_type in content:
                        schema = content[content_type].get('schema', {})
                        return self._resolve_schema(schema)

            # Swagger 2.0 structure: parameters with in="body"
            if parameters:
                for param in parameters:
                    if param.get('in') == 'body' and 'schema' in param:
                        return self._resolve_schema(param['schema'])

            return ""
        except Exception as e:
            logger.warning(f"Failed to extract request body schema: {str(e)}")
            return ""

    def extract_response_schema(self, responses: Dict) -> str:
        """
        Extract response schema from first successful response (200, 201, etc.)
        Handles both OpenAPI 3.0 (content wrapper) and Swagger 2.0 (direct schema)

        Args:
            responses: Responses object from OpenAPI spec

        Returns:
            str: JSON representation of the response schema
        """
        try:
            # Try common success codes
            for code in ['200', '201', '202', '204', 'default']:
                if code in responses:
                    response = responses[code]

                    # OpenAPI 3.0 structure: response.content
                    content = response.get('content', {})
                    if content:
                        # Try common content types
                        for content_type in ['application/json', 'application/xml', '*/*']:
                            if content_type in content:
                                schema = content[content_type].get('schema', {})
                                return self._resolve_schema(schema)

                    # Swagger 2.0 structure: response.schema (direct)
                    if 'schema' in response:
                        return self._resolve_schema(response['schema'])

            return ""
        except Exception as e:
            logger.warning(f"Failed to extract response schema: {str(e)}")
            return ""

    def _resolve_schema(self, schema: Dict, depth: int = 0) -> str:
        """
        Recursively resolve schema references and build JSON structure

        Args:
            schema: Schema object
            depth: Current recursion depth (to prevent infinite loops)

        Returns:
            str: JSON representation of the schema
        """
        if depth > 10:
            return json.dumps({"error": "max_depth_exceeded"})

        try:
            # Handle $ref
            if '$ref' in schema:
                ref_path = schema['$ref']
                resolved = self._resolve_reference(ref_path)
                if resolved:
                    return self._resolve_schema(resolved, depth + 1)

            schema_type = schema.get('type', 'object')
            result = {}

            # Handle array type
            if schema_type == 'array':
                items = schema.get('items', {})
                items_schema = self._resolve_schema(items, depth + 1)
                return json.dumps({
                    "type": "array",
                    "items": json.loads(items_schema) if items_schema else {}
                }, indent=2)

            # Handle object type
            elif schema_type == 'object' or 'properties' in schema:
                properties = schema.get('properties', {})
                required = schema.get('required', [])

                for prop_name, prop_schema in properties.items():
                    prop_info = {}

                    # Check if required
                    if prop_name in required:
                        prop_info['required'] = True

                    # Get type
                    prop_type = prop_schema.get('type', '')
                    if prop_type:
                        prop_info['type'] = prop_type

                    # Get format
                    prop_format = prop_schema.get('format', '')
                    if prop_format:
                        prop_info['format'] = prop_format

                    # Get description
                    description = prop_schema.get('description', '')
                    if description:
                        prop_info['description'] = description

                    # Get example
                    example = prop_schema.get('example', '')
                    if example:
                        prop_info['example'] = str(example)

                    # Get enum
                    enum = prop_schema.get('enum', [])
                    if enum:
                        prop_info['enum'] = enum

                    # Handle nested objects
                    if prop_type == 'object' or 'properties' in prop_schema:
                        nested = self._resolve_schema(prop_schema, depth + 1)
                        if nested:
                            prop_info['properties'] = json.loads(nested)

                    # Handle arrays
                    elif prop_type == 'array':
                        items = prop_schema.get('items', {})
                        items_schema = self._resolve_schema(items, depth + 1)
                        if items_schema:
                            prop_info['items'] = json.loads(items_schema)

                    # Handle $ref in property
                    elif '$ref' in prop_schema:
                        ref_schema = self._resolve_schema(prop_schema, depth + 1)
                        if ref_schema:
                            prop_info['properties'] = json.loads(ref_schema)

                    result[prop_name] = prop_info

                return json.dumps(result, indent=2)

            # Handle primitive types
            else:
                return json.dumps({
                    "type": schema_type,
                    "format": schema.get('format', ''),
                    "description": schema.get('description', '')
                }, indent=2)

        except Exception as e:
            logger.error(f"Failed to resolve schema: {str(e)}")
            return "{}"

    def _resolve_reference(self, ref_path: str) -> Optional[Dict]:
        """
        Resolve a $ref reference to its definition

        Args:
            ref_path: Reference path (e.g., "#/definitions/Pet")

        Returns:
            dict: Resolved schema or None
        """
        if not self.spec or not ref_path.startswith('#/'):
            return None

        try:
            # Remove leading #/ and split path
            path_parts = ref_path[2:].split('/')

            # Navigate through spec
            current = self.spec
            for part in path_parts:
                current = current.get(part, {})

            return current if current else None

        except Exception as e:
            logger.warning(f"Failed to resolve reference {ref_path}: {str(e)}")
            return None

    def get_all_operations(self) -> List[Dict[str, Any]]:
        """
        Extract all API operations from the spec

        Returns:
            list: List of operation dictionaries with all details
        """
        if not self.spec or 'paths' not in self.spec:
            return []

        operations = []
        sl_no = 1

        for path, path_item in self.spec['paths'].items():
            # Get path-level parameters
            path_params = path_item.get('parameters', [])

            for method in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
                if method not in path_item:
                    continue

                operation = path_item[method]

                # Get tags (component)
                tags = operation.get('tags', ['default'])
                component = tags[0] if tags else 'default'

                # Combine path-level and operation-level parameters
                all_params = path_params + operation.get('parameters', [])
                params = self.extract_parameters(all_params)

                # Extract request body (for POST/PUT)
                # OpenAPI 3.0 uses requestBody, Swagger 2.0 uses body parameter
                request_body = operation.get('requestBody', {})
                example_json = self.extract_request_body_schema(request_body, all_params)

                # Extract response model
                responses = operation.get('responses', {})
                response_model_json = self.extract_response_schema(responses)

                # Build operation record
                op_record = {
                    'Sl_No': sl_no,
                    'Component': component,
                    'Component_SmallDescription': '',
                    'Operation_Method': method.upper(),
                    'Operation_Path': path,
                    'Operation_Summary': operation.get('summary', ''),
                    'Operation_SecondarySummary': operation.get('description', ''),
                    'header_parameters': params['header_parameters'],
                    'query_parameters': params['query_parameters'],
                    'path_parameters': params['path_parameters'],
                    'form_data_parameters': params['form_data_parameters'],
                    'example_value_json': example_json,
                    'response_model_json': response_model_json
                }

                operations.append(op_record)
                sl_no += 1

        logger.info(f"✅ Extracted {len(operations)} operations")
        return operations

    def enrich_with_tag_descriptions(self, operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add tag descriptions to operations

        Args:
            operations: List of operation records

        Returns:
            list: Operations with tag descriptions added
        """
        tags = self.get_tags()
        tag_map = {tag['name']: tag['description'] for tag in tags}

        for op in operations:
            component = op['Component']
            op['Component_SmallDescription'] = tag_map.get(component, '')

        return operations