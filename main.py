from tester import ask_perplexity, insert_perplexity
from speechrecog import get_speech
from texttosspeech import tts, play_audio, save_audio

live_convo = True
user_turn = 0
status = ['Not initialized', 'User speaking', 'Tester speaking']
company = 'Big Tech Co.'
interview_topic = 'Electrical Engineering'
job = 'Junior VLSI designer'
# tailor_responses = 'Please also rate on a scale of 1-10 the satisfactoriness of the answer and reply with just the number.'
request_summary = 'Please summarize the prior discussion. Tell me how I could have improved my interview answers, then we can move on to behavioral questions.'
added_text_prompt = ''
n_behavioral = 2
n_end = 5
iteration = 0


def parse_reply(reply):
    out = ''.join([i for i in reply if (i.isalpha() or i.isspace() or i in [',', '.', '?', '!', "'", "-", ";", "+", "=", "*"])])
    return out

while (live_convo):
    # if (iteration == n_rounds):
    #     response = insert_perplexity('Please proceed to the next stage of the interview.')
    #     # response = insert_perplexity('Please begin the behavioral interview stage. Ask questions that reveal how the candidate acts in difficult situations.')
    #     print(response)
    if (user_turn == 0):
        user_turn = 1
        print('asking perplexity')
        insert_perplexity("Your role is an interviewer at {}. Please initiate the interview by introducing yourself, and telling the candidate the structure of the interview. Wait for the candidate confirmation before asking technical questions. The topic is {}. The candidate is interviewing for job {}. Do not apologize unnecessarily!".format(company, interview_topic, job))
        # reply, citations = response
        # reply = parse_reply(reply)
        # print(reply)
    user_spoken = ''
    if (user_turn == 1):
        print(status[user_turn])
        user_spoken = get_speech()
        print(user_spoken)
        if (user_spoken != ''):
            user_turn = -1 * user_turn
    if(user_turn == -1):
        print(status[user_turn])
        response = ask_perplexity(user_spoken + added_text_prompt)
        # print(response)
        try:
            reply, citations = response
            reply = parse_reply(reply)
            print(reply)
            # agent_spoken = tts(reply)
            # play_audio(agent_spoken)
        except ValueError:
            print(response)
        user_turn = -1 * user_turn

    if (iteration == n_behavioral):
        added_text_prompt = request_summary


    iteration += 1


