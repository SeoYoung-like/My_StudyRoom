import requests

resp = requests.post(
    url="https://httpbin.org/post",
    data={"name": "SEO"},
)


print("상태 코드:", resp.status_code)
print("응답 본문:", resp.text)