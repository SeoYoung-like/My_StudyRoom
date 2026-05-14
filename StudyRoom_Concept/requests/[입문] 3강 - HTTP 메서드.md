

# 3단계. 자주 쓰는 HTTP 메서드 익히기

**[ 핵심 목표 ]**

이번 단계의 목표는 `requests` 라이브러리에서 자주 사용하는 **HTTP 메서드**를 익히는 것입니다.

HTTP 메서드는 쉽게 말하면 **서버에게 어떤 작업을 요청할 것인지 알려주는 명령어**입니다.

```text
GET     → 데이터 조회
POST    → 데이터 전송 또는 생성
PUT     → 전체 수정
PATCH   → 일부 수정
DELETE  → 삭제
```

웹 API를 사용할 때는 대부분 이 메서드들을 기준으로 기능이 나뉩니다.

예를 들어 게시판 API가 있다고 하면 다음처럼 생각할 수 있습니다.

```text
게시글 목록 조회      → GET
게시글 작성           → POST
게시글 전체 수정      → PUT
게시글 일부 수정      → PATCH
게시글 삭제           → DELETE
```



# 1. HTTP 메서드란 무엇인가

HTTP 메서드는 클라이언트가 서버에게 보내는 **요청의 목적**입니다.
서버에 **"어떤 작업을 원하는지"** 알려주는 수단으로 사용된다.

웹 브라우저에서 페이지를 열 때, 로그인 버튼을 누를 때, 게시글을 삭제할 때 — 이 모든 동작이 각각 다른 HTTP 메서드로 서버에 전달됩니다. 메서드를 구분하는 이유는 서버가 같은 URL이라도 **어떤 동작을 해야 하는지 명확하게 파악**하기 위해서입니다.

데이터베이스의 CRUD(Create, Read, Update, Delete) 개념과 1:1로 대응된다고 이해하면 직관적입니다.

---

클라이언트는 Python 코드일 수도 있고, 웹 브라우저일 수도 있고, 모바일 앱일 수도 있습니다.

```text
클라이언트
  → 서버에게 요청
  → 요청 목적을 HTTP 메서드로 표현
  → 서버가 응답 반환
```

예를 들어 Python에서 다음 코드를 실행한다고 해보겠습니다.

```python
import requests

response = requests.get("https://httpbin.org/get")
```

이 코드는 서버에게 이렇게 말하는 것과 같습니다.

```text
이 주소에 있는 데이터를 조회하고 싶습니다.
```

반대로 `POST`는 서버에게 데이터를 보내는 요청입니다.

```python
response = requests.post(
    "https://httpbin.org/post",
    data={"name": "seo"}
)
```

이 코드는 서버에게 이렇게 말하는 것과 비슷합니다.

```text
name이 seo인 데이터를 서버로 보냅니다.
```

------









# 2. 5가지 메서드 개념

현대적인 API 설계(REST API)에서는 상황에 맞는 메서드 사용을 엄격히 권장합니다.

- **GET (조회):** 서버로부터 특정 데이터를 가져올 때 사용합니다. 게시글 읽기, 사용자 정보 확인 등이 해당합니다.
- **POST (전송/생성):** 서버에 새로운 데이터를 제출하여 리소스를 생성할 때 사용합니다. 회원가입, 게시글 작성 등이 대표적입니다.
- **PUT (전체 수정):** 기존의 리소스를 새로운 데이터로 완전히 교체할 때 사용합니다.
- **PATCH (일부 수정):** 리소스의 전체가 아닌 일부 항목만 수정할 때 사용합니다. (예: 사용자의 프로필 사진만 변경)
- **DELETE (삭제):** 특정 리소스를 삭제할 때 사용합니다.

| 메서드 | 역할               | DB 대응       | 중요도   |
| ------ | ------------------ | ------------- | -------- |
| GET    | 데이터 조회        | Read          | ★ 최우선 |
| POST   | 데이터 전송 / 생성 | Create        | ★ 최우선 |
| PUT    | 데이터 전체 수정   | Update (전체) | 중간     |
| PATCH  | 데이터 일부 수정   | Update (일부) | 중간     |
| DELETE | 데이터 삭제        | Delete        | 중간     |



**[ GET — 데이터 조회 ★ ]**

서버에 있는 데이터를 **읽어오는** 메서드입니다.

- 가장 기본이며 가장 많이 사용합니다.
- 요청할 때 **본문(body)을 포함하지 않습니다.** 데이터를 가져오기만 할 뿐, 서버의 상태를 변경하지 않습니다.
- 검색, 목록 조회, 상세 페이지 요청 등 거의 모든 "읽기" 작업에 사용합니다.

```python
# 예: 사용자 목록 가져오기
requests.get("https://api.example.com/users")
```

------



**[ POST — 데이터 전송 / 생성 ★ ]**

서버에 **새로운 데이터를 보내거나 생성**할 때 사용하는 메서드입니다.

- 회원가입, 로그인, 게시글 작성, 파일 업로드 등 대부분의 "쓰기" 작업에 사용합니다.
- GET과 달리 요청 **본문(body)에 데이터를 담아** 전송합니다.
- 같은 요청을 여러 번 보내면 데이터가 여러 번 생성될 수 있습니다. (멱등성 없음)

```python
# 예: 새 사용자 등록
requests.post("https://api.example.com/users", data={"name": "seo"})
```

------



**[ PUT — 데이터 전체 수정 ]** 

서버에 존재하는 데이터를 **통째로 교체**할 때 사용합니다.

- 수정할 리소스의 **모든 필드를 빠짐없이** 전송해야 합니다.
- 보내지 않은 필드는 삭제되거나 기본값으로 초기화될 수 있습니다.
- 같은 요청을 여러 번 보내도 결과가 동일합니다. (멱등성 있음)

```python
# 예: 사용자 정보 전체 교체
requests.put("https://api.example.com/users/1", data={"name": "kim", "age": 30})
```

------



**[ PATCH — 데이터 일부 수정 ]**

서버에 존재하는 데이터의 **특정 필드만 수정**할 때 사용합니다.

- PUT과 달리 변경할 필드만 골라서 보내면 됩니다.
- 나머지 필드는 서버에서 기존 값을 유지합니다.
- 실무에서는 PUT보다 PATCH를 더 자주 사용하는 경우가 많습니다.

```python
# 예: 이름만 변경
requests.patch("https://api.example.com/users/1", data={"name": "lee"})
```

------



**[ DELETE — 데이터 삭제 ]**

서버에 있는 특정 리소스를 **삭제**할 때 사용합니다.

- 대부분 URL에 삭제 대상의 ID를 포함해서 보냅니다.
- 삭제 후에는 보통 204 No Content 또는 200 OK가 응답으로 돌아옵니다.

```python
# 예: ID가 1인 사용자 삭제
requests.delete("https://api.example.com/users/1")
```







## 2.1. GET: 데이터 조회

### 1) GET의 의미

`GET`은 서버에서 데이터를 가져올 때 사용합니다.

가장 많이 사용하는 HTTP 메서드 중 하나입니다.

```python
requests.get(url)
```

예시:

```python
import requests

response = requests.get("https://httpbin.org/get")

print(response.status_code)
print(response.text)
```

`GET`은 보통 다음 상황에서 사용합니다.

```text
웹페이지 가져오기
검색 결과 가져오기
상품 목록 조회하기
게시글 목록 조회하기
사용자 정보 조회하기
책 정보 검색하기
유튜브 영상 정보 조회하기
```

------



### 2) GET 요청의 특징

`GET`은 기본적으로 **데이터를 조회하는 요청**입니다.

즉, 서버에 있는 데이터를 바꾸기보다는 가져오는 목적이 강합니다.

```text
GET 요청
  → 데이터를 조회한다
  → 서버 데이터 변경 목적이 아니다
  → URL에 검색 조건을 붙이는 경우가 많다
```

예를 들어 검색어를 서버에 전달할 때는 이런 식으로 URL에 값이 붙을 수 있습니다.

```text
https://example.com/search?keyword=python
```

`requests`에서는 보통 `params`를 사용해서 검색 조건을 전달합니다.

```python
import requests

url = "https://httpbin.org/get"

params = {
    "keyword": "python",
    "page": 1
}

response = requests.get(url, params=params)

print(response.url)
print(response.text)
```

이때 최종 URL은 대략 다음과 비슷해집니다.

```text
https://httpbin.org/get?keyword=python&page=1
```

즉, `params`는 GET 요청에서 자주 사용하는 옵션입니다.

------



## 2.2. POST: 데이터 전송

### 1) POST의 의미

`POST`는 서버에 데이터를 보낼 때 사용합니다.

```python
requests.post(url)
```

예시:

```python
import requests

response = requests.post(
    "https://httpbin.org/post",
    data={"name": "seo"}
)

print(response.status_code)
print(response.text)
```

`POST`는 보통 다음 상황에서 사용합니다.

```text
회원가입
로그인
게시글 작성
댓글 작성
주문 생성
결제 요청
폼 데이터 제출
파일 업로드
```

------



### 2) POST 요청의 특징

`POST`는 단순 조회보다는 **서버에 어떤 데이터를 전달하는 목적**이 강합니다.

```text
POST 요청
  → 서버에 데이터를 보낸다
  → 새로운 데이터를 만들 때 자주 사용한다
  → 로그인, 회원가입, 등록, 작성 기능에서 많이 사용한다
```

예를 들어 사용자의 이름을 서버에 보낸다고 하면 다음처럼 작성할 수 있습니다.

```python
import requests

url = "https://httpbin.org/post"

data = {
    "name": "seo",
    "age": 20
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.text)
```

여기서 `data`는 서버에 보낼 데이터입니다.

------



### 3) data와 json의 차이

`POST`를 배울 때 초보자가 자주 헷갈리는 부분이 있습니다.

바로 `data`와 `json`입니다.

```python
requests.post(url, data={...})
requests.post(url, json={...})
```

둘 다 서버에 데이터를 보내지만 형식이 다릅니다.

| 방식   | 의미                    | 주 사용 상황                |
| ------ | ----------------------- | --------------------------- |
| `data` | 폼 데이터 형식으로 전송 | 일반 HTML form, 간단한 전송 |
| `json` | JSON 형식으로 전송      | REST API, 백엔드 API 통신   |

예시 1. `data` 사용

```python
import requests

response = requests.post(
    "https://httpbin.org/post",
    data={"name": "seo"}
)

print(response.text)
```

예시 2. `json` 사용

```python
import requests

response = requests.post(
    "https://httpbin.org/post",
    json={"name": "seo"}
)

print(response.text)
```

실무 API에서는 `json`을 사용하는 경우가 많습니다.

```python
response = requests.post(
    url,
    json={
        "title": "Python Requests",
        "content": "HTTP 메서드 학습"
    }
)
```

`requests.post()`는 `data=` 파라미터로 딕셔너리를 전달합니다. 이 데이터가 요청 본문에 담겨 서버로 전송됩니다.

`httpbin.org`는 받은 요청 내용을 그대로 응답으로 돌려주기 때문에, POST로 보낸 데이터가 응답 본문에 포함되어 있는지 직접 눈으로 확인할 수 있습니다. 내가 의도한 데이터가 제대로 서버에 도달했는지 검증하는 용도로 매우 유용합니다.







## 2.3. PUT: 전체 수정

### 1) PUT의 의미

`PUT`은 기존 데이터를 **전체 수정**할 때 주로 사용합니다.

```python
requests.put(url)
```

예를 들어 사용자 정보가 있다고 해보겠습니다.

```json
{
  "name": "seo",
  "age": 20,
  "job": "student"
}
```

이 정보를 `PUT`으로 수정한다면 보통 전체 데이터를 다시 보내는 방식입니다.

```python
import requests

url = "https://httpbin.org/put"

data = {
    "name": "seo",
    "age": 21,
    "job": "developer"
}

response = requests.put(url, json=data)

print(response.status_code)
print(response.text)
```

------



### 2) PUT의 핵심 개념

`PUT`은 보통 다음 의미로 이해하면 됩니다.

```text
기존 데이터를 이 내용으로 통째로 교체해줘.
```

예를 들어 게시글 수정 API가 있다고 해보겠습니다.

```text
PUT /posts/1
```

이 요청은 보통 1번 게시글을 전체 수정한다는 의미입니다.

```json
{
  "title": "수정된 제목",
  "content": "수정된 내용",
  "category": "Python"
}
```

즉, 일부 필드만 바꾸는 느낌보다 전체 자원을 새 내용으로 바꾸는 느낌이 강합니다.





## 2.4. PATCH: 일부 수정

### 1) PATCH의 의미

`PATCH`는 기존 데이터 중 **일부만 수정**할 때 사용합니다.

```python
requests.patch(url)
```

예를 들어 사용자 정보 중 나이만 바꾸고 싶다고 해보겠습니다.

기존 데이터:

```json
{
  "name": "seo",
  "age": 20,
  "job": "student"
}
```

나이만 수정:

```python
import requests

url = "https://httpbin.org/patch"

data = {
    "age": 21
}

response = requests.patch(url, json=data)

print(response.status_code)
print(response.text)
```

------



### 2) PATCH의 핵심 개념

`PATCH`는 보통 이렇게 이해하면 됩니다.

```text
기존 데이터 중 이 부분만 바꿔줘.
```

예를 들어 게시글 제목만 수정하고 싶다면 다음과 같은 느낌입니다.

```text
PATCH /posts/1
{
  "title": "새 제목"
}
```

즉, `PUT`보다 수정 범위가 작습니다.





## 2.5. DELETE: 데이터 삭제

### 1) DELETE의 의미

`DELETE`는 서버에 있는 데이터를 삭제할 때 사용합니다.

```python
requests.delete(url)
```

예시:

```python
import requests

response = requests.delete("https://httpbin.org/delete")

print(response.status_code)
print(response.text)
```

`DELETE`는 보통 다음 상황에서 사용합니다.

```text
게시글 삭제
댓글 삭제
회원 탈퇴
장바구니 상품 삭제
파일 삭제
등록된 데이터 제거
```

------



### 2) DELETE의 핵심 개념

`DELETE`는 말 그대로 서버에게 삭제를 요청하는 메서드입니다.

```text
이 데이터를 삭제해줘.
```

예를 들어 게시글 1번을 삭제한다면 API 주소가 이런 식일 수 있습니다.

```text
DELETE /posts/1
```

Python 코드로는 이런 느낌입니다.

```python
import requests

url = "https://example.com/posts/1"

response = requests.delete(url)

print(response.status_code)
```

다만 실제 서비스 API에서는 삭제 요청에 인증 토큰이 필요한 경우가 많습니다.

------





# 3. requests 학습 팁

## 3.1. requests에서 HTTP 메서드 사용하는 방법

requests는 각 HTTP 메서드에 대응하는 함수를 직관적인 이름으로 제공합니다.
구조는 모두 동일하며, **함수 이름만 바꾸면** 다른 메서드로 전환됩니다.

| HTTP 메서드 | requests 함수          | 주 용도           |
| ----------- | ---------------------- | ----------------- |
| `GET`       | `requests.get(url)`    | 데이터 조회       |
| `POST`      | `requests.post(url)`   | 데이터 전송, 생성 |
| `PUT`       | `requests.put(url)`    | 전체 수정         |
| `PATCH`     | `requests.patch(url)`  | 일부 수정         |
| `DELETE`    | `requests.delete(url)` | 삭제              |

```python
requests.get(url)       # GET    — 데이터 조회
requests.post(url)      # POST   — 데이터 전송 / 생성
requests.put(url)       # PUT    — 데이터 전체 수정
requests.patch(url)     # PATCH  — 데이터 일부 수정
requests.delete(url)    # DELETE — 데이터 삭제
```

> 공식 문서(requests.readthedocs.io)에서도 이 다섯 가지 함수를 주요 API로 안내하고 있습니다.

데이터를 함께 보낼 때는 보통 `data` 또는 `json`을 사용합니다.

```python
requests.post(url, data={"name": "seo"})
requests.post(url, json={"name": "seo"})
```

------



## 3.2. GET과 POST를 먼저 익혀야 하는 이유

초보 단계에서는 `GET`과 `POST`를 가장 먼저 익히는 것이 좋습니다.

왜냐하면 실무에서 가장 자주 만나게 되는 요청이기 때문입니다.

```text
GET  → 데이터를 가져올 때
POST → 데이터를 보낼 때
```

대부분의 API 학습은 이 두 개로 시작합니다.

예를 들어 다음과 같은 프로그램을 만든다고 해보겠습니다.

---

**책 검색 프로그램**

```text
책 목록 검색 → GET
```

---

**로그인 프로그램**

```text
아이디와 비밀번호 전송 → POST
```

---

**유튜브 데이터 조회 프로그램**

```text
영상 정보 조회 → GET
댓글 목록 조회 → GET
```

---

**게시판 프로그램**

```text
게시글 목록 조회 → GET
게시글 작성 → POST
```

---

그래서 처음에는 이렇게 우선순위를 잡으면 됩니다.

```text
1순위: GET
2순위: POST
3순위: PUT, PATCH, DELETE
```

`PUT`, `PATCH`, `DELETE`는 API를 직접 다루거나 백엔드와 연동할 때 자연스럽게 익히면 됩니다.





# 4. 전체 예제 코드

## 4.1 GET 예제

```python
import requests

response = requests.get("https://httpbin.org/get")

print("상태 코드:", response.status_code)
print("응답 본문:", response.text)
```

------



## 4.2 POST 예제

```python
import requests

response = requests.post(
    "https://httpbin.org/post",
    data={"name": "seo"}
)

print("상태 코드:", response.status_code)
print("응답 본문:", response.text)
```

------



## 4.3 GET과 POST 함께 사용하기

```python
import requests

# GET: 데이터 조회
r1 = requests.get("https://httpbin.org/get")

print("GET 상태 코드:", r1.status_code)
print("GET 응답 본문:", r1.text)


# POST: 데이터 전송
r2 = requests.post(
    "https://httpbin.org/post",
    data={"name": "seo"}
)

print("POST 상태 코드:", r2.status_code)
print("POST 응답 본문:", r2.text)
```

------

```
import requests

# 1. GET 요청 예시: 데이터를 조회합니다.
# 서버의 응답 결과를 r1 객체에 담습니다.
r1 = requests.get("https://httpbin.org/get")

# 2. POST 요청 예시: 데이터를 서버로 전송합니다.
# 'data' 파라미터를 통해 딕셔너리 형태의 데이터를 보낼 수 있습니다.
r2 = requests.post("https://httpbin.org/post", data={"name": "seo"})

# 3. 결과 확인
# 전송 후 서버가 정상적으로 처리했는지 상태 코드를 확인합니다 (200 또는 201이 일반적).
print(f"POST 요청 상태 코드: {r2.status_code}")
```



## 4.4 PUT, PATCH, DELETE 예제

```python
import requests

# PUT: 전체 수정
put_response = requests.put(
    "https://httpbin.org/put",
    json={
        "name": "seo",
        "age": 21
    }
)

print("PUT 상태 코드:", put_response.status_code)


# PATCH: 일부 수정
patch_response = requests.patch(
    "https://httpbin.org/patch",
    json={
        "age": 22
    }
)

print("PATCH 상태 코드:", patch_response.status_code)


# DELETE: 삭제
delete_response = requests.delete("https://httpbin.org/delete")

print("DELETE 상태 코드:", delete_response.status_code)
```

------











# [ 핵심 정리 ]

이번 단계에서 반드시 기억해야 할 내용은 다음과 같습니다.

| 메서드   | 의미              | requests 함수          | 중요도 |
| -------- | ----------------- | ---------------------- | ------ |
| `GET`    | 데이터 조회       | `requests.get(url)`    | ★★★    |
| `POST`   | 데이터 전송, 생성 | `requests.post(url)`   | ★★★    |
| `PUT`    | 전체 수정         | `requests.put(url)`    | ★★     |
| `PATCH`  | 일부 수정         | `requests.patch(url)`  | ★★     |
| `DELETE` | 삭제              | `requests.delete(url)` | ★★     |

가장 중요한 코드는 아래입니다.

```python
import requests

# GET
r1 = requests.get("https://httpbin.org/get")

# POST
r2 = requests.post(
    "https://httpbin.org/post",
    data={"name": "seo"}
)

print(r1.status_code)
print(r2.status_code)
```

초보자는 보통 `requests.get()`과 `requests.post()`를 단순한 함수로만 외우려고 합니다.

하지만 실무 관점에서는 이렇게 이해해야 합니다.

```text
HTTP 메서드는 서버에게 요청의 목적을 알려주는 약속이다.
```

즉, 중요한 것은 함수 이름 자체가 아니라 **요청의 의도**입니다.

```text
조회하고 싶다      → GET
보내거나 만들고 싶다 → POST
전체를 바꾸고 싶다  → PUT
일부만 바꾸고 싶다  → PATCH
삭제하고 싶다      → DELETE
```

이 개념을 이해하면 API 문서를 읽을 때 훨씬 쉬워집니다.



★ API 문서에서 다음과 같은 내용을 보면:

```text
GET /books
POST /books
GET /books/{id}
PATCH /books/{id}
DELETE /books/{id}
```

이제 대략 이렇게 해석할 수 있어야 합니다.

```text
GET /books        → 책 목록 조회
POST /books       → 새 책 등록
GET /books/{id}   → 특정 책 조회
PATCH /books/{id} → 특정 책 일부 수정
DELETE /books/{id}→ 특정 책 삭제
```

결국 이 단계의 목표는 단순히 코드를 실행하는 것이 아니라, **API 문서를 읽고 어떤 요청을 보내야 하는지 판단하는 힘**을 기르는 것입니다.



