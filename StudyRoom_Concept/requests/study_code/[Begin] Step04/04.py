import requests

# 1. params= — URL에 조회 조건 붙이기
r1 = requests.get(
    "https://httpbin.org/get",
    params={"keyword": "python", "page": 1}
)
print("[GET + params] URL:", r1.url)

# 2. data= — 폼 데이터로 전송
r2 = requests.post(
    "https://httpbin.org/post",
    data={"username": "seo", "password": "1234"}
)
print("[POST + data] status:", r2.status_code)

# 3. json= — JSON으로 전송 (REST API 방식)
r3 = requests.post(
    "https://httpbin.org/post",
    json={"title": "hello", "content": "world"}
)
print("[POST + json] status:", r3.status_code)