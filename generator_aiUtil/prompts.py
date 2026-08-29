"""
Standard English prompts used by the AI code modifier utilities.
Modify these messages here to change the behavior of the LLM calls.
"""

STANDARD_METHOD_ENHANCEMENT_PROMPT = (
    "You are an expert Python pytest test method enhancer.\n\n"
    "Review the following test method and improve it by:\n"
    "- Adding proper assertions and validation if required\n"
    "- Adding proper import statements if any are missing\n"
    "- Improving error handling and logging\n"
    "- Using best practices for REST API testing\n"
    "- Ensuring values extracted from responses are used correctly in subsequent steps\n\n"
    "You must NOT change the method name, class name, or method signature.\n"
    "Return ONLY the complete updated test method code.\n"
    "Do not include explanations, notes, or markdown code blocks.\n\n"
    "Original test method:\n"
    "```python\n"
    "{method_content}\n"
    "```"
)
