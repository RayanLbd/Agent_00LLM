import requests

response = requests.get("https://api.ipify.org?format=json")
print(response.json())
