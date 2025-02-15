"""
Implements the tester back-end using perplexity. 
Feature Requirements: 
    - Capability of mistake-catching 
    - Capability of suggesting industry standard solutions #TODO: need to confirm
    - Follow up questions 
    - Design questions
    - Citations
    - Memory in the conversation
    - Fast responses 
    - Streamed responses

Features Implemented/Guaranteed: 
    - Output response 
    - Capability of mistake-catching 
    - Citations
    - Memory
    - Follow up questions

Date: 02/15/25
Author: Andrea Miramontes Serrano

"""
import requests
import json

# Andrea's key
API_KEY = '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'
URL = "https://api.perplexity.ai/chat/completions"

CONV_HIST = [
        {"role": "system", "content": "You are an AI test examiner. Catch mistakes, provide sources and always ask a follow up, technical question. If the user makes a mistake, ask them about that. Every once in a while, ask design questions and/or industry-standard questions. If there are mistakes that keep happening, detect when the user has an underlying misconception."}
        ]

def ask_perplexity(prompt: str) -> str:
    """
    Initializes a perplexity API call: 
    - Asks for interview context #TODO: expand feature set to also social anxiety context 
    - enables user to choose prompt #TODO: expand to have this be a voice input. 
    - Capability of mistake-catching 
    - Capability of suggesting industry standard solutions #TODO: need to confirm
    - Follow up questions 
    - Design questions
    - Citations
    - Memory in the conversation
    - Fast responses 
    - Streamed responses

    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    CONV_HIST.append({"role": "user", "content": prompt})

    data = {
        "model": "sonar-pro",# Use best available model
        "messages": CONV_HIST,  # Maintain conversation memory
        "max_tokens": 300,
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
        text_response, citations = result["choices"][0]["message"]["content"], result["citations"]

        # Add AI response to memory
        CONV_HIST.append({"role": "assistant", "content": text_response})
        return text_response, citations
    else:
        return f"Error: {response.status_code}, {response.text}"
    
        #TODO: clean up for streamed responses - this bit chunks the response. 
        # full_response = ""
        # print("\n📢 AI is responding...\n")
        # for line in response.iter_lines():
        #     if line:
        #         decoded_line = json.loads(line.decode("utf-8"))
        #         text_chunk = decoded_line["choices"][0]["message"]["content"]
        #         print(text_chunk, end="", flush=True)  # Show response progressively
        #         full_response += text_chunk

        

        # Another way of extracting citations [doesn't work as well]:
        # references = decoded_line["choices"][0]["message"].get("references", [])
        # if references:
        #     print("\n\n🔗 **Citations:**")
        #     for ref in references:
        #         print(f"- {ref['title']} ({ref['url']})")
    

# ----------------- USAGE -----------------
import sys #TODO: remove - only here for debugging purposes
if len(sys.argv) > 1:
    user_input = sys.argv[1]  # Takes input from launch.json
else:
    user_input = input("Enter your prompt: ")  # Fallback manual input

response = ask_perplexity(user_input)
ask_perplexity(user_input)
print("\nPerplexity AI Response:\n", response[0])
