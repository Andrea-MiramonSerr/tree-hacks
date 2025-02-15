from tester import ask_perplexity
from speechrecog import get_speech
from texttosspeech import tts, play_audio

live_convo = True
user_turn = 0
status = ['Not initialized', 'User speaking', 'Tester speaking']

def parse_reply(reply):
    out = ''.join([i for i in reply if (i.isalpha() or i.isspace())])
    return out

while (live_convo):
    if (user_turn == 0):
        user_turn = 1
        print('asking perplexity')
        reply, citations = ask_perplexity('Please ask the interviewee to introduce themselves.')
        reply = parse_reply(reply)
        print(reply)

    user_spoken = ''
    if (user_turn == 1):
        print(status[user_turn])
        user_spoken = get_speech()
        print(user_spoken)
        user_turn = -1 * user_turn
    if(user_turn == -1):
        print(status[user_turn])
        reply, citations = ask_perplexity(user_spoken)
        reply = parse_reply(reply)
        print(reply)
        # agent_spoken = tts(reply)
        play_audio(agent_spoken)
        user_turn = -1 * user_turn


