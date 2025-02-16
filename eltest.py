from elevenlabs import generate, set_api_key

set_api_key('sk_e5f53a150de75465187a3fa312e6cbca028f3454447133ca')

audio = generate(
    text="Hello World!",
    voice="Bella"
)

with open("out.wav", "wb") as fp:
    fp.write(audio)