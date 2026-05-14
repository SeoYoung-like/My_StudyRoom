import requests

resp = requests.get("https://www.naver.com")

print(resp.url)
print(resp.status_code)
print(resp.headers)
print(resp.json())



