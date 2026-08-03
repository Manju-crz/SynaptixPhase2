"""
Simple DeepSeek API Test Script
Uses OpenAI-compatible API to interact with DeepSeek models
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize DeepSeek client
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def query_deepseek(prompt: str, model: str = "deepseek-v4-coder") -> str:
    """
    Send a query to DeepSeek and get the response.

    Args:
        prompt: The user's query/prompt
        model: DeepSeek model to use (default: deepseek-v4-coder)

    Returns:
        The model's response as a string
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert code generator"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    # Example usage
    print("🤖 DeepSeek API Test\n")

    # Test query
    query = "Given a natural language description, generate clean python code"
    print(f"📝 Query: {query}\n")
    print("⏳ Waiting for response...\n")

    # Get response
    response = query_deepseek(query)

    print(f"💬 Response:\n{response}\n")

    # Interactive mode
    print("\n" + "="*50)
    print("Interactive Mode - Type 'exit' to quit")
    print("="*50 + "\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['exit', 'quit', 'q']:
            print("👋 Goodbye!")
            break

        if not user_input.strip():
            continue

        response = query_deepseek(user_input)
        print(f"\nDeepSeek: {response}\n")