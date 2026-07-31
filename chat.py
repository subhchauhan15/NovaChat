from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import requests
import os

load_dotenv()

API_KEY = os.getenv("NVIDIA_API_KEY")

url = "https://integrate.api.nvidia.com/v1/chat/completions"


env = Environment(
    loader=FileSystemLoader(".")
)
template=env.get_template("prompt.jinja")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

while True:
    user_input=input("ask the query:- ")
    if user_input=="exit":
        print("thak gya kya, chal kuch or puchna ho to vpas aana-Good Bye🫡 😉")
        break
    prompt=template.render(
        user_query=user_input
    )
    payload = {
            "model": "nvidia/nemotron-3-super-120b-a12b",
            "messages": [{"role": "user", "content": user_input}],
            "temperature": 0.7
        }
    response = requests.post(url, headers=headers, json=payload)
    data=response.json()
    print(data['choices'][0]['message']['content'])

