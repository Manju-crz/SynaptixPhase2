# AI Code Modifier Readme

## Overview

The AI Code Modifier Utility provides capabilities to modify and enhance generated test code using AI providers.

## Features

- Modify generated pytest code with AI instructions
- Support for multiple AI providers (OpenAI, Grok, DeepSeek)
- Extract and apply instructions from natural language queries
- Add error handling, logging, and validation to generated code

## Usage

```python
from generator_aiUtil.ai_code_modifier_util import modify_generated_code_with_ai

result = modify_generated_code_with_ai(
    file_path="test_file.py",
    method_name="test_create_pet",
    original_code=original_code,
    excel_data=excel_data,
    queries=["Create a pet -> Add error handling"],
    ai_provider="openai"
)
```

## AI Providers

- **OpenAI**: GPT-4 based code generation
- **Grok**: Grok API based generation
- **DeepSeek**: DeepSeek API based generation
