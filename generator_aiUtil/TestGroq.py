"""
Simple Groq API Test Script
Uses Groq API to interact with ultra-fast LLM models
"""

import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def query_groq(prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
    """
    Send a query to Groq and get the response.

    Args:
        prompt: The user's query/prompt
        model: Groq model to use (default: llama-3.3-70b-versatile)
        Options:
        - llama-3.3-70b-versatile (recommended)
        - llama-3.1-70b-versatile
        - llama-3.1-8b-instant
        - mixtral-8x7b-32768
        - gemma2-9b-it

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
    print("🚀 Groq API Test\n")

    # Test query
    query = "Given a natural language description, generate clean python code"

    print(f"📝 Query: {query}\n")
    print("⏳ Waiting for response...\n")

    # Get response
    response = query_groq(query)

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

        response = query_groq(user_input)
        print(f"\nGroq: {response}\n")