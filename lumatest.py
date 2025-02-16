import os
import requests
import time
from lumaai import LumaAI, AsyncLumaAI
os.environ["LUMAAI_API_KEY"] = "luma-1c2a2983-47d5-4305-a3e6-7b10596fba7e-3fe1e6aa-bc71-4aa8-8723-bd0215c17360"

client = LumaAI(
    auth_token=os.environ.get("LUMAAI_API_KEY"),
)

print(client)

generation = client.generations.create(
#   prompt="Filmed from point of view of a candidate getting interviewed by a manager for a job position. Manager is looking at the camera directly speaking to it. Background is a serious office. Make him say 'hello'.",
# prompt="A serious character in a suit is talking to the viewer. They are talking and making exaggerated expressions. Their mouth is open sometimes.",
# )
prompt="Make a film where: a real-life manager looks at the camera opens their mouth every second as if they were talking, interviewing the candidate seriously, while eating a banana. ")

completed = False
while not completed:
  generation = client.generations.get(id=generation.id)
  if generation.state == "completed":
    completed = True
  elif generation.state == "failed":
    raise RuntimeError(f"Generation failed: {generation.failure_reason}")

video_url = generation.assets.video

# download the video
response = requests.get(video_url, stream=True)
with open(f'{generation.id}.mp4', 'wb') as file:
    file.write(response.content)
print(f"File downloaded as {generation.id}.mp4")