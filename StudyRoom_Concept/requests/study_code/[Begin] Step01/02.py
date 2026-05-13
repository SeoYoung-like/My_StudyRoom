import requests

params = {
    "sort": "asc",
    "page": 1,
}

response = requests.get(url="https://www.naver.com", params=params)
print(response.url)