import requests

API_KEY = "PASTE_YOUR_KEY_HERE"

url = "https://openrouter.ai/api/v1/models"

headers = {
    "Authorization": f"Bearer {API_KEY}",
}

response = requests.get(url, headers=headers)
print(response.json())