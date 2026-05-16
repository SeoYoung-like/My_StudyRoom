import requests

url = "https://httpbin.org/post"

params = {
    "notify": "true"
}

body = {
    "title": "hello",
    "content": "world"
}


r = requests.post(
    url,
    params=params,
    json=body,
)

print(f"최종 url: {r.url}")
print(f"상태 코드: {r.status_code}")
print(f"응답 본문: {r.text}")

