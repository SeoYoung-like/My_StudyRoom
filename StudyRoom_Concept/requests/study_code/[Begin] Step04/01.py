import requests

r = requests.get(
    "https://httpbin.org/get",
    params={
        "keyword": "python",
        "page": 1,
    }
)

print(f"최종 url: {r.url}")
print(f"상태 코드: {r.status_code}")
print(f"응답 본문: {r.text}")