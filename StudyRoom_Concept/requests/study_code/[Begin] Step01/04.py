import requests

headers = {
    "Authorization": "Bearer my-token-1234",
    "Content-Type": "application/json",
    "User-Agent": "MyApp/1.0"
}

response = requests.get("https://www.naver.com", headers=headers)
print(response.headers)
print(response.headers["Content-Type"])