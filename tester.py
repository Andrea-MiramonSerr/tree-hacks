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
        {
            "role": "system",
            "content": "You are an interviewer conducting a job interview. Please keep responses short and conversational. To candidate's responses ask follow up, technical questions. If the user makes a factual mistake, ask them about that. Questions are industry-standard. If candidate keeps making mistakes, address their underlying misconception. If the conversation drifts away from the interview topic, do guide the interviewee back."
        # You are an interviewer conducting a job interview.
        # Keep responses short and conversational.
        # Catch mistakes, provide sources and always ask a follow up, technical question.
        # If the user makes a mistake, ask them about that. Every once in a while, ask design questions and/or industry-standard questions.
        # If there are mistakes that keep happening, detect when the user has an underlying misconception.
        # """
        }
    ]

def insert_perplexity(admin_prompt: str):
    CONV_HIST.append({"role": "system", "content": admin_prompt})
    # initial_content = CONV_HIST[0]["content"]
    # output_content = initial_content + admin_prompt
    # CONV_HIST[0]["content"] = output_content
    # response = requests.post(URL, headers=headers, data=json.dumps(data))

    # if response.status_code == 200:
    #     result = response.json()
    #     text_response, citations = result["choices"][0]["message"]["content"], result["citations"]

    #     # Add AI response to memory
    #     CONV_HIST.append({"role": "assistant", "content": text_response})
    #     return text_response, citations
    # else:
    #     return f"Error: {response.status_code}, {response.text}"

def ask_perplexity(prompt: str, role:str = "user") -> str:
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

    CONV_HIST.append({"role": role, "content": prompt})

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
        text_response, citations = result["choices"][0]["message"]["content"], result.get("citations")

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

company = 'Big Tech Co.'
interview_topic = 'Electrical Engineering'
job = 'Junior VLSI designer.'
n_rounds = 2
iteration = 0
insert_perplexity("Your role is an interviewer at {}. Please initiate the interview by introducing yourself, and telling the candidate the structure of the interview. Wait for the candidate confirmation before asking technical questions. The topic is {}. The candidate is interviewing for job {}. Do not apologize unnecessarily! After {} rounds of technical questions, move on to behavioral questions in the interview.".format(company, interview_topic, job, n_rounds))
print(CONV_HIST[0])
while (True):
    response = ask_perplexity(user_input)
    ask_perplexity(user_input)
    print("\nPerplexity AI Response:\n", response[0])
    user_input = input("Enter your prompt: ")
