import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

print(response.status_code)  # 200

if response.status_code == 200:
    print("요청 성공")
elif response.status_code == 404:
    print("해당 데이터 없음")
elif response.status_code >= 500:
    print("서버 오류, 나중에 다시 시도")