import requests

resp = requests.put(
    url="https://httpbin.org/put",
    json={
        "name": "seo",
        "age": 21,
    }
)
print("상태 코드:", resp.status_code)
print("응답 본문:", resp.text)

resp = requests.patch(
    url="https://httpbin.org/patch",
    json={
        "name": "go",
    }
)
print("상태 코드:", resp.status_code)
print("응답 본문:", resp.text)

resp = requests.delete(url="https://httpbin.org/delete")
print("상태 코드:", resp.status_code)
print("응답 본문:", resp.text)