from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play, stream, save

ELEVENLABS_API_KEY = 'sk_e5f53a150de75465187a3fa312e6cbca028f3454447133ca'
load_dotenv()
client = ElevenLabs(api_key = ELEVENLABS_API_KEY)
audio = client.text_to_speech.convert(
    text="Hi candidate, welcome to the interview.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)
play(audio)

save(audio, 'test.mp3')
# audio_stream = client.text_to_speech.convert_as_stream(

#     text="This is a test",

#     voice_id="JBFqnCBsd6RMkjVDRZzb",

#     model_id="eleven_multilingual_v2"

# )

# # option 1: play the streamed audio locally

# stream(audio_stream)