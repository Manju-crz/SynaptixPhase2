"""
Simple OpenAI API Test Script
Uses OpenAI API to interact with GPT models
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def query_openai(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Send a query to OpenAI and get the response.

    Args:
        prompt: The user's query/prompt
        model: OpenAI model to use (default: gpt-4o-mini)
        Options: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo

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
    print("🤖 OpenAI API Test\n")

    # Test query
    query = "Given a natural language description, generate clean python code"

    print(f"📝 Query: {query}\n")
    print("⏳ Waiting for response...\n")

    # Get response
    response = query_openai(query)

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

        response = query_openai(user_input)
        print(f"\nOpenAI: {response}\n")