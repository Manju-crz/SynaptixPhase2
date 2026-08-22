"""
AI Code Modifier Utility - Enhance generated test code using AI models
Uses extracted Excel data and query instructions to modify generated code
"""

import os
import ast
import json
import logging
from typing import Dict, List, Optional, Any
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='\n%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class AICodeModifier:
    """
    Modifies generated test code using AI models based on query instructions and Excel data.
    """

    def __init__(self, ai_provider: str = "openai"):
        """
        Initialize AI Code Modifier.

        Args:
            ai_provider: AI provider to use ('openai', 'deepseek', 'groq')
        """
        self.ai_provider = ai_provider.lower()
        self.client = self._initialize_ai_client()
        logger.info(f"🔧 Initializing AI Code Modifier with provider: {ai_provider}")

    def _initialize_ai_client(self):
        """Initialize the appropriate AI client based on provider."""
        if self.ai_provider == "openai":
            return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif self.ai_provider == "deepseek":
            return OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com"
            )
        elif self.ai_provider == "groq":
            return Groq(api_key=os.getenv("GROQ_API_KEY"))
        else:
            raise ValueError(f"Unsupported AI provider: {self.ai_provider}")

    def _get_model_name(self) -> str:
        """Get the appropriate model name for the provider."""
        models = {
            "openai": "gpt-4o-mini",
            "deepseek": "deepseek-v4-coder",
            "groq": "llama-3.3-70b-versatile"
        }
        return models.get(self.ai_provider, "gpt-4o-mini")

    def _parse_query_instructions(self, queries: List[str]) -> List[Dict[str, Any]]:
        """
        Parse queries to extract instructions from statements after -> delimiter.

        Args:
            queries: List of natural language queries

        Returns:
            List of dictionaries with query and instructions
        """
        parsed_queries = []

        for query in queries:
            # Support both ASCII (->) and Unicode (→) arrows
            if '→' in query:
                parts = query.split('→')
            else:
                parts = query.split('->')

            if len(parts) > 1:
                # First part is the main action, rest are instructions
                main_action = parts[0].strip()
                instructions = [part.strip() for part in parts[1:]]

                parsed_queries.append({
                    'main_action': main_action,
                    'instructions': instructions,
                    'full_query': query
                })
            else:
                # No instructions, just the action
                parsed_queries.append({
                    'main_action': query.strip(),
                    'instructions': [],
                    'full_query': query
                })

        return parsed_queries

    def _build_ai_prompt(
        self,
        original_code: str,
        excel_data: List[Dict[str, Any]],
        query_instructions: List[Dict[str, Any]]
    ) -> str:
        """
        Build the AI prompt for code modification.

        Args:
            original_code: Original generated test method code
            excel_data: Extracted Excel data for each step
            query_instructions: Parsed query instructions

        Returns:
            AI prompt string
        """
        prompt = f"""You are an expert Python test code modifier. Your task is to modify the given pytest test method based on specific instructions.

ORIGINAL TEST CODE:
```python
{original_code}
```

EXCEL DATA FOR EACH STEP:
"""
        for i, data in enumerate(excel_data, 1):
            prompt += f"\nStep {i} (Sl_No: {data.get('sl_no', 'N/A')}):\n"
            prompt += f"  Method: {data.get('operation_method', 'N/A')}\n"
            prompt += f"  Path: {data.get('operation_path', 'N/A')}\n"
            prompt += f"  Summary: {data.get('operation_summary', 'N/A')}\n"
            
            # Add content type information
            content_type = data.get('request_content_type', '')
            if content_type:
                prompt += f"  Content-Type: {content_type}\n"

            if data.get('header_parameters'):
                prompt += f"  Headers: {json.dumps(data['header_parameters'], indent=2)}\n"
            if data.get('query_parameters'):
                prompt += f"  Query Params: {json.dumps(data['query_parameters'], indent=2)}\n"
            if data.get('path_parameters'):
                prompt += f"  Path Params: {json.dumps(data['path_parameters'], indent=2)}\n"
            if data.get('form_data_parameters'):
                prompt += f"  Form Data Params: {json.dumps(data['form_data_parameters'], indent=2)}\n"
            if data.get('request_body_json'):
                prompt += f"  Request Body: {json.dumps(data['request_body_json'], indent=2)}\n"
            if data.get('response_json'):
                prompt += f"  Response: {json.dumps(data['response_json'], indent=2)}\n"

        prompt += "\n\nMODIFICATION INSTRUCTIONS:\n"

        for i, query_info in enumerate(query_instructions, 1):
            prompt += f"\nStep {i}: {query_info['main_action']}\n"
            if query_info['instructions']:
                for j, instruction in enumerate(query_info['instructions'], 1):
                    prompt += f"  Instruction {j}: {instruction}\n"

        prompt += """

REQUIREMENTS:
1. Modify the test code to implement ALL the instructions provided
2. Use the Excel data to understand available parameters and responses
3. Implement proper field extraction based on instructions (e.g., "Retrieve the pet_id from response")
4. Use extracted values in subsequent steps as instructed (e.g., "Use the pet_id from previous response")
5. Keep all existing Allure decorators and logging
6. Maintain proper error handling and assertions
7. Ensure the code is syntactically correct and follows pytest best practices
8. Keep the same method signature and structure
9. Add comments where modifications are made
10. **CRITICAL**: For POST/PUT requests, check the Content-Type:
    - If Content-Type is 'application/x-www-form-urlencoded', use `data=payload` parameter
    - If Content-Type is 'application/json', use `json_payload=payload` parameter
    - NEVER use `json=payload` (this parameter does not exist in RestApiClient)
11. When Form Data Params are provided, create the payload dict from those parameters

OUTPUT:
Return ONLY the complete modified Python test method code, nothing else. Do not include explanations or markdown code blocks.
"""

        return prompt

    def modify_code_with_ai(
        self,
        original_code: str,
        excel_data: List[Dict[str, Any]],
        queries: List[str]
    ) -> Dict[str, Any]:
        """
        Modify test code using AI based on instructions.

        Args:
            original_code: Original generated test method code
            excel_data: Extracted Excel data for each step
            queries: Natural language queries with instructions

        Returns:
            Dictionary with modified code and metadata
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"🤖 MODIFYING CODE WITH AI ({self.ai_provider.upper()})")
        logger.info(f"{'='*80}")

        # Parse query instructions
        query_instructions = self._parse_query_instructions(queries)

        # Log parsed instructions
        logger.info(f"\n📋 Parsed Instructions:")
        for i, qi in enumerate(query_instructions, 1):
            logger.info(f"  Step {i}: {qi['main_action']}")
            for j, inst in enumerate(qi['instructions'], 1):
                logger.info(f"    → {inst}")

        # Build AI prompt
        prompt = self._build_ai_prompt(original_code, excel_data, query_instructions)

        logger.info(f"\n📤 Sending request to {self.ai_provider.upper()}...")

        try:
            # Call AI model
            response = self.client.chat.completions.create(
                model=self._get_model_name(),
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Python pytest test test code modifier. You modify test codebased on specific instructions while maintaining code quality and best practices."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent code generation
                max_tokens=4000
            )

            modified_code = response.choices[0].message.content.strip()

            # Remove markdown code blocks if present
            if modified_code.startswith("```python"):
                modified_code = modified_code.split("```python")[1]
                modified_code = modified_code.split("```")[0].strip()
            elif modified_code.startswith("```"):
                modified_code = modified_code.split("```")[1]
                modified_code = modified_code.split("```")[0].strip()

            logger.info(f"✅ Code modification completed")
            logger.info(f"  Original lines: {len(original_code.split(chr(10)))}")
            logger.info(f"  Modified lines: {len(modified_code.split(chr(10)))}")

            return {
                'success': True,
                'modified_code': modified_code,
                'original_code': original_code,
                'ai_provider': self.ai_provider,
                'instructions_applied': len([qi for qi in query_instructions if qi['instructions']])
            }

        except Exception as e:
            logger.error(f"❌ Error modifying code: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'original_code': original_code
            }

    def replace_method_with_ai_version(
        self,
        file_path: str,
        original_method_name: str,
        modified_code: str
    ) -> Dict[str, Any]:
        """
        Replace the original method with AI-modified version (with _ai suffix).
        Removes the original method and adds the AI version in its place.

        Args:
            file_path: Path to the test file
            original_method_name: Original method name to replace
            modified_code: Modified method code

        Returns:
            Dictionary with operation result
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"💾 REPLACING METHOD WITH AI VERSION")
        logger.info(f"{'='*80}")

        try:
            # Read existing file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse the file into AST to find method boundaries
            tree = ast.parse(content)
            lines = content.split('\n')

            # Create new method name with _ai suffix
            new_method_name = f"{original_method_name}_ai"

            # Replace method name in modified code
            modified_code_with_new_name = modified_code.replace(
                f"def {original_method_name}(",
                f"def {new_method_name}(",
                1
            )

            # Find the original method to replace
            method_start_line = None
            method_end_line = None
            decorator_start_line = None
            class_indent = "    "  # Default 4 spaces

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == original_method_name:
                    # Check if method has decorators
                    if node.decorator_list:
                        # Start from first decorator
                        decorator_start_line = node.decorator_list[0].lineno - 1  # 0-indexed
                    else:
                        # No decorators, start from method definition
                        decorator_start_line = node.lineno - 1
                    
                    method_start_line = node.lineno - 1  # 0-indexed
                    method_end_line = node.end_lineno  # 1-indexed, so this is the line after the method
                    break

            if method_start_line is None:
                logger.warning(f"⚠️  Original method '{original_method_name}' not found, appending AI method instead")
                # If original method not found, append the AI method
                return self.append_modified_method_to_file(file_path, original_method_name, modified_code)

            logger.info(f"  Found original method at lines {decorator_start_line + 1}-{method_end_line} (including decorators)")

            # Indent the modified code to be inside the class
            indented_lines = []
            for line in modified_code_with_new_name.split('\n'):
                if line.strip():  # Non-empty line
                    indented_lines.append(class_indent + line)
                else:  # Empty line
                    indented_lines.append(line)

            indented_code = '\n'.join(indented_lines)

            # Replace the original method (including decorators) with AI version
            new_lines = lines[:decorator_start_line] + [indented_code] + lines[method_end_line:]

            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))

            logger.info(f"✅ Method replaced successfully")
            logger.info(f"  Original method: {original_method_name} (removed)")
            logger.info(f"  New method: {new_method_name} (replaced at same position)")
            logger.info(f"  File: {file_path}")

            return {
                'success': True,
                'new_method_name': new_method_name,
                'file_path': file_path,
                'replaced': True
            }

        except Exception as e:
            logger.error(f"❌ Error replacing method: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def append_modified_method_to_file(
        self,
        file_path: str,
        original_method_name: str,
        modified_code: str
    ) -> Dict[str, Any]:
        """
        Append modified test method to the same file with _ai suffix.
        Properly indents the method to be inside the test class.

        Args:
            file_path: Path to the test file
            original_method_name: Original method name
            modified_code: Modified method code

        Returns:
            Dictionary with operation result
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"💾 APPENDING MODIFIED METHOD TO FILE")
        logger.info(f"{'='*80}")

        try:
            # Read existing file
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Create new method name with _ai suffix
            new_method_name = f"{original_method_name}_ai"

            # Replace method name in modified code
            modified_code_with_new_name = modified_code.replace(
                f"def {original_method_name}(",
                f"def {new_method_name}(",
                1
            )

            # Find the test class and get its indentation
            class_indent = "    "  # Default 4 spaces
            insert_position = len(lines)  # Default to end of file

            # Look for the class definition
            for i, line in enumerate(lines):
                if 'class TestGeneratedAPIs' in line or 'class Test' in line:
                    # Found the class, now find the last method in the class
                    for j in range(len(lines) - 1, i, -1):
                        # Look for the end of the last method (empty lines after method)
                        if lines[j].strip() and not lines[j].startswith('#'):
                            # Found last non-empty line in class
                            insert_position = j + 1
                            break
                    break

            # Indent the modified code to be inside the class
            indented_lines = []
            for line in modified_code_with_new_name.split('\n'):
                if line.strip():  # Non-empty line
                    indented_lines.append(class_indent + line)
                else:  # Empty line
                    indented_lines.append(line)

            indented_code = '\n'.join(indented_lines)

            # Insert the method at the correct position
            lines.insert(insert_position, '\n\n')
            lines.insert(insert_position + 1, indented_code + '\n')

            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            logger.info(f"✅ Modified method appended successfully")
            logger.info(f"  New method name: {new_method_name}")
            logger.info(f"  Inserted at line: {insert_position}")
            logger.info(f"  File: {file_path}")

            return {
                'success': True,
                'new_method_name': new_method_name,
                'file_path': file_path
            }

        except Exception as e:
            logger.error(f"❌ Error appending method: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


def modify_generated_code_with_ai(
    file_path: str,
    method_name: str,
    original_code: str,
    excel_data: List[Dict[str, Any]],
    queries: List[str],
    ai_provider: str = "openai",
    replace_original: bool = True
) -> Dict[str, Any]:
    """
    Convenience function to modify generated code and replace/append to file.

    Args:
        file_path: Path to the test file
        method_name: Original method name
        original_code: Original generated code
        excel_data: Extracted Excel data for each step
        queries: Natural language queries with instructions
        ai_provider: AI provider to use
        replace_original: If True, replace original method with AI version; if False, append

    Returns:
        Dictionary with operation result
    """
    modifier = AICodeModifier(ai_provider=ai_provider)

    # Modify code with AI
    result = modifier.modify_code_with_ai(original_code, excel_data, queries)

    if not result['success']:
        return result

    # Replace or append to file based on flag
    if replace_original:
        file_result = modifier.replace_method_with_ai_version(
            file_path,
            method_name,
            result['modified_code']
        )
    else:
        file_result = modifier.append_modified_method_to_file(
            file_path,
            method_name,
            result['modified_code']
        )

    if file_result['success']:
        return {
            'success': True,
            'new_method_name': file_result['new_method_name'],
            'file_path': file_result['file_path'],
            'modified_code': result['modified_code'],
            'ai_provider': result['ai_provider'],
            'instructions_applied': result['instructions_applied'],
            'replaced': file_result.get('replaced', False)
        }
    else:
        return file_result