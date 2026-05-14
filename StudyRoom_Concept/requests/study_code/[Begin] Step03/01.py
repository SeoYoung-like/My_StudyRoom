import requests

resp = requests.get("https://httpbin.org/get")

print("상태 코드:", resp.status_code)
print("응답 본문:", resp.text)