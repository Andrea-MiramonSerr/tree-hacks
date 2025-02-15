"""
Implements the tester back-end using perplexity. 
Feature Requirements: 
    - Capability of mistake-catching 
    - Capability of suggesting industry standard solutions
    - Citations
    - Memory in the conversation
    - Fast responses 
    - Streamed responses

Features Implemented: 
    - Memory 
    - 

Date: 02/15/25
Author: Andrea Miramontes Serrano

"""
import requests
import json

# Andrea's key
API_KEY = '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'
URL = "https://api.perplexity.ai/chat/completions"

def ask_perplexity(prompt: str) -> str:
    """
    Initializes a perplexity API call: 
    - Asks for interview context #TODO: expand feature set to also social anxiety context 
    - enables user to choose prompt #TODO: expand to have this be a voice input. 
    - Capability of mistake-catching 
    - Capability of suggesting industry standard solutions
    - Citations
    - Memory in the conversation
    - Fast responses 
    - Streamed responses

    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "sonar-pro",  # Ensure you're using a valid model
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 0.1  # Set to a valid value (>0)
    }



    response = requests.post(URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# ----------------- USAGE -----------------
import sys #TODO: remove - only here for debugging purposes
if len(sys.argv) > 1:
    user_input = sys.argv[1]  # Takes input from launch.json
else:
    user_input = input("Enter your prompt: ")  # Fallback manual input
# user_prompt = input("Enter your prompt: ")
response = ask_perplexity(user_input)
print("\nPerplexity AI Response:\n", response)
