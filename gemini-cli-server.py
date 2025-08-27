import os
import requests
import json
# from dotenv import load_dotenv

# load_dotenv()

# Load MCP configuration
try:
    with open('settings.json') as f:
        config = json.load(f)
except Exception as e:
    print(f"Error loading config: {e}")
    print("Create ~/.gemini/settings.json first")
    exit(1)

def query_local_model(prompt):
    """Query local model via LM Studio's OpenAI-compatible API"""
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "model": config["model_provider"]["model"],
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 128000
    }
    
    try:
        response = requests.post(
            f"{config['model_provider']['base_url']}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error querying model: {str(e)}\nMake sure LM Studio server is running!"

def handle_obsidian_query(query):
    """Query Obsidian vault through MCP server"""
    try:
        response = requests.post(
            f"{config['mcp_servers']['obsidian']['endpoint']}/query",
            json={"query": query},
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Obsidian query failed: {str(e)}"}

def main():
    print("Local CLI with LM Studio (Free & Private)")
    print("=========================================")
    print("Type 'exit' to quit, '@' commands for tools")
    print("Make sure LM Studio server is running!\n")
    
    while True:
        user_input = input("> ")
        
        if user_input.lower() == 'exit':
            break
            
        # Handle tool commands
            
        if user_input.startswith('@obsidian'):
            query = user_input.replace('@obsidian', '').strip()
            results = handle_obsidian_query(query)
            if isinstance(results, dict) and results.get("error"):
                print(f"\nError: {results['error']}")
            else:
                print("\nFound in your Obsidian vault:")
                for i, res in enumerate(results.get('results', [])):
                    print(f"\n{i}. {res['file']}")
                    print(f"   ...{res['snippet']}...")
            # continue

                while True:
                    # Regular query - use LM Studio
                    print("\n🧠 Using with your local model...")
                    prompt = f"""
                    You are a helpful assistant. Use the following context from the user's Obsidian vault to answer the question.
                    Context: {json.dumps(results.get('results', []))}
                    Question: {user_input}
                    Answer concisely.
                    """

                    response = query_local_model(prompt)
                    print("\n💬 Response:")
                    print(response)
                    print("Anything else? (type 'exit' to quit)")
                    user_input = input("> ")
                    if user_input.lower() == '> exit':
                        return

#gradio
#django
if __name__ == "__main__":
    main()