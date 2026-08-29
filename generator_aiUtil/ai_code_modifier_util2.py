"""
AI Code Modifier Utility 2 - Enhance a single test method using AI models
Accepts a file path, a method name, and a prompt string, then replaces that method.
"""

import os
import re
import ast
import logging
from typing import Dict, Any, Optional
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv
from . import prompts

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='\n%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class AICodeModifier2:
    """Enhances individual test methods using AI models."""

    def __init__(self, ai_provider: str = "openai"):
        """Initialize AI Code Modifier 2.

        Args:
            ai_provider: AI provider to use ('openai', 'deepseek', 'groq')
        """
        self.ai_provider = ai_provider.lower()
        self.client = self._initialize_ai_client()
        logger.info(f"Initializing AI Code Modifier 2 with provider: {ai_provider}")

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

    def _extract_python_code(self, text: str) -> str:
        """Remove markdown code blocks if the model wraps the output."""
        text = text.strip()
        match = re.search(r"```(?:python)?\n(.*?)\n```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        if text.startswith("```"):
            text = text.lstrip("`").split("```", 1)[-1]
            text = text.split("```", 1)[0]
        return text.strip()

    def _extract_method(self, file_path: str, method_name: str) -> Optional[Dict[str, Any]]:
        """Extract a single method from a test file, including decorators."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            return None

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            logger.error(f"Original file has syntax error: {str(e)}")
            return None

        lines = content.split('\n')

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == method_name:
                if node.decorator_list:
                    start_line = node.decorator_list[0].lineno - 1
                else:
                    start_line = node.lineno - 1

                end_line = node.end_lineno
                base_line = lines[start_line]
                base_indent = len(base_line) - len(base_line.lstrip(' '))

                method_lines = lines[start_line:end_line]
                unindented_lines = []
                for line in method_lines:
                    if line.startswith(' ' * base_indent):
                        unindented_lines.append(line[base_indent:])
                    else:
                        unindented_lines.append(line)

                return {
                    'content': content,
                    'lines': lines,
                    'start_line': start_line,
                    'end_line': end_line,
                    'base_indent': base_indent,
                    'method_code': '\n'.join(unindented_lines)
                }

        logger.warning(f"Method '{method_name}' not found in {file_path}")
        return None

    def enhance_test_method(
        self,
        file_path: str,
        method_name: str,
        full_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Enhance a single test method using a complete prompt string.

        The prompt may include the placeholder '{method_content}' which will be
        replaced with the current method content. If the placeholder is not found,
        the original method content is prepended to the prompt.

        Args:
            file_path: Path to the test file
            method_name: Name of the test method to enhance
            full_prompt: Complete prompt string to send to the LLM (defaults to prompts.STANDARD_METHOD_ENHANCEMENT_PROMPT)

        Returns:
            Dictionary with operation result
        """
        logger.info(f"{'='*80}")
        logger.info(f"Enhancing test method with AI ({self.ai_provider.upper()})")
        logger.info(f"{'='*80}")

        if full_prompt is None:
            full_prompt = prompts.STANDARD_METHOD_ENHANCEMENT_PROMPT

        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return {
                'success': False,
                'error': f"File not found: {file_path}"
            }

        method_data = self._extract_method(file_path, method_name)
        if not method_data:
            return {
                'success': False,
                'error': f"Method '{method_name}' not found or file has syntax errors"
            }

        original_code = method_data['method_code']

        if '{method_content}' in full_prompt:
            user_prompt = full_prompt.replace('{method_content}', original_code)
        else:
            user_prompt = (
                f"ORIGINAL TEST METHOD:\n```python\n{original_code}\n```\n\n"
                f"{full_prompt}"
            )

        logger.info(f"Sending request to {self.ai_provider.upper()}...")

        try:
            response = self.client.chat.completions.create(
                model=self._get_model_name(),
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert Python pytest test method enhancer. "
                            "Return only the complete updated Python test method code, "
                            "with no explanations, notes, or markdown code blocks. "
                            "Do not change the method name or signature."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                temperature=0.2,
                max_tokens=4000
            )

            enhanced_code = self._extract_python_code(response.choices[0].message.content)

            # Validate syntax before writing
            try:
                ast.parse(enhanced_code)
            except SyntaxError as se:
                logger.error(f"Enhanced code has syntax error: {str(se)}")
                return {
                    'success': False,
                    'error': f"Enhanced code has syntax error: {str(se)}",
                    'original_code': original_code,
                    'enhanced_code': enhanced_code
                }

            # Re-indent the enhanced method to match the original class indentation
            base_indent = ' ' * method_data['base_indent']
            indented_lines = []
            for line in enhanced_code.split('\n'):
                if line.strip():
                    indented_lines.append(base_indent + line)
                else:
                    indented_lines.append(line)

            new_lines = (
                method_data['lines'][:method_data['start_line']] +
                indented_lines +
                method_data['lines'][method_data['end_line']:]
            )

            # Write enhanced file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))

            logger.info(f"Test method enhanced successfully: {method_name}")
            logger.info(f"  Original lines: {len(original_code.split(chr(10)))}")
            logger.info(f"  Enhanced lines: {len(enhanced_code.split(chr(10)))}")

            return {
                'success': True,
                'file_path': file_path,
                'method_name': method_name,
                'enhanced_code': enhanced_code,
                'ai_provider': self.ai_provider
            }

        except Exception as e:
            logger.error(f"Error enhancing test method: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'original_code': original_code,
                'file_path': file_path
            }


def enhance_test_method_with_ai(
    file_path: str,
    method_name: str,
    full_prompt: Optional[str] = None,
    ai_provider: str = "openai"
) -> Dict[str, Any]:
    """Convenience function to enhance a single test method using an LLM prompt.

    Args:
        file_path: Path to the test file
        method_name: Name of the test method to enhance
        full_prompt: Complete prompt string for the LLM (defaults to prompts.STANDARD_METHOD_ENHANCEMENT_PROMPT)
        ai_provider: AI provider to use

    Returns:
        Dictionary with operation result
    """
    modifier = AICodeModifier2(ai_provider=ai_provider)
    return modifier.enhance_test_method(file_path, method_name, full_prompt)
