# 1단계. requests가 무엇인지 이해하기

개발의 세계에서 외부 세상과 소통하는 가장 기본적인 방법이 바로 **HTTP 통신**입니다. 파이썬의 `requests` 라이브러리는 이 복잡한 통신 과정을 "인간이 이해하기 쉬운" 방식으로 추상화해 준 도구입니다.

------

## 목차

1. requests가 하는 일
2. HTTP 기본 개념
   - 2-1. 요청과 응답
   - 2-2. URL 구조
   - 2-3. 상태 코드
   - 2-4. Header
3. 왜 requests를 쓰는가
4. 핵심 정리

------



## 1. requests가 하는 일

한 줄로 정의하면 다음과 같습니다.

> requests는 Python에서 웹 서버에 HTTP 요청을 보내고 응답을 받아오는 라이브러리입니다.

우리가 크롬 브라우저에서 주소창에 URL을 입력하면, 브라우저가 해당 서버에 "이 페이지 데이터 주세요"라고 요청을 보냅니다. requests는 이 과정을 Python 코드로 할 수 있게 해주는 도구입니다.

브라우저가 하는 일을 코드로 대신하는 것이라고 이해하면 됩니다.

```python
import requests

response = requests.get("https://www.naver.com")
print(response.status_code)  # 200
```

위 코드 한 줄이 브라우저에서 네이버를 여는 것과 본질적으로 같은 동작입니다.

------



## 2. HTTP 기본 개념

HTTP(HyperText Transfer Protocol)는 웹에서 데이터를 주고받기 위한 약속입니다. 가장 중요한 것은 **요청(Request)**과 **응답(Response)**의 쌍으로 이루어진다는 점입니다.

- **요청(Request):** 클라이언트(나의 코드)가 서버(웹사이트)에게 "이 데이터 좀 줘" 혹은 "이 데이터 좀 저장해 줘"라고 말하는 행위입니다.
- **응답(Response):** 서버가 클라이언트의 요청을 확인하고 "여기 있어(데이터)" 혹은 "안돼(에러)"라고 대답하는 결과물입니다.

이 과정은 마치 레스토랑에서 손님이 메뉴를 주문(요청)하면 주방에서 요리(응답)를 내오는 과정과 같습니다.



### 2-1. 요청과 응답

HTTP 통신의 구조는 항상 다음 두 가지로 이루어집니다.

```
클라이언트 (내 Python 코드)
        |
        |  요청 (Request) : "이 데이터 주세요"
        v
서버 (네이버, 공공 API, GitHub 등)
        |
        |  응답 (Response) : "네, 여기 있습니다"
        v
클라이언트 (내 Python 코드)
```

요청(Request)에는 다음 정보가 담깁니다.

- 어디로 보낼지 (URL)
- 어떤 행동을 원하는지 (메서드 : GET, POST 등)
- 추가 정보 (Header, Body)

응답(Response)에는 다음 정보가 담깁니다.

- 요청이 성공했는지 여부 (상태 코드)
- 실제 데이터 (Body : HTML, JSON 등)
- 서버 정보 (Header)

------

### 2-2. URL 구조

우리가 흔히 '주소'라고 부르는 URL(Uniform Resource Locator)은 생각보다 정교하게 구성되어 있습니다.

```
https://api.example.com/v1/users?id=123
```

- **Scheme (https):** 통신 방식(규약)을 결정합니다. 보안이 적용된 HTTP를 의미합니다.

- **Host (api.example.com):** 목적지 서버의 이름입니다.

- **Path (/v1/users):** 서버 내에서 구체적으로 어떤 자원(Resource)에 접근할지 지정합니다.

- **Query String (?id=123):** 추가적인 조건을 달 때 사용합니다. "사용자 중에서 ID가 123인 사람을 보여줘"라는 뜻입니다.

URL은 다음과 같이 여러 부분으로 구성됩니다.

```
https://api.example.com/users/123?sort=asc&page=1
|----| |---------------| |------| |--------------|
scheme      host           path      query string
```

각 부분의 역할은 아래와 같습니다.

| 구성 요소    | 예시            | 역할                             |
| ------------ | --------------- | -------------------------------- |
| scheme       | https           | 통신 규약 (http 또는 https)      |
| host         | api.example.com | 서버 주소 (도메인)               |
| path         | /users/123      | 서버 내 자원의 위치              |
| query string | sort=asc&page=1 | 추가 조건, ? 뒤에 key=value 형태 |

requests에서 query string은 다음과 같이 `params` 로 깔끔하게 처리할 수 있습니다.

```python
import requests

params = {
    "sort": "asc",
    "page": 1
}

response = requests.get("https://api.example.com/users/123", params=params)

# 실제 요청 URL 확인
print(response.url)
# https://api.example.com/users/123?sort=asc&page=1
```

직접 URL에 문자열로 이어붙이지 않아도 되는 이유가 바로 이 params 파라미터 덕분입니다.

------

### 2-3. 상태 코드 (Status Code) ★

서버는 응답을 보낼 때 숫자로 된 '상태 코드'를 함께 보냅니다. 이 숫자를 보면 요청이 성공했는지, 왜 실패했는지 즉시 알 수 있습니다.

| **코드**                      | **의미**            | **설명**                                                     |
| ----------------------------- | ------------------- | ------------------------------------------------------------ |
| **200 OK**                    | **성공**            | 요청이 완벽하게 처리되었습니다.                              |
| **404 Not Found**             | **클라이언트 오류** | 요청한 주소가 존재하지 않습니다. (오타 확인 필요)            |
| **500 Internal Server Error** | **서버 오류**       | 서버 내부에서 문제가 발생했습니다. (내 잘못이 아닐 확률 높음) |
| **401/403**                   | **권한 오류**       | 로그인이 필요하거나 접근 권한이 없습니다.                    |

상태 코드는 서버가 요청을 받아서 어떻게 처리했는지 알려주는 숫자입니다. 이것을 제대로 이해하지 못하면 이후 에러 처리 단계에서 반드시 막힙니다.

크게 다섯 가지 그룹으로 나뉩니다.

```
1xx : 정보 전달 (거의 볼 일 없음)
2xx : 성공
3xx : 리다이렉트 (다른 곳으로 이동)
4xx : 클라이언트 잘못 (내 요청이 틀림)
5xx : 서버 잘못 (서버 내부 오류)
```

실무에서 자주 마주치는 상태 코드는 다음과 같습니다.

| 상태 코드 | 의미                  | 상황                                  |
| --------- | --------------------- | ------------------------------------- |
| 200       | OK                    | 요청 성공, 데이터 정상 반환           |
| 201       | Created               | POST 요청으로 데이터 생성 성공        |
| 400       | Bad Request           | 요청 형식이 잘못됨 (파라미터 오류 등) |
| 401       | Unauthorized          | 인증 안 됨 (로그인 필요)              |
| 403       | Forbidden             | 인증은 됐지만 권한 없음               |
| 404       | Not Found             | 해당 URL에 자원 없음                  |
| 429       | Too Many Requests     | 너무 많은 요청 (API 속도 제한)        |
| 500       | Internal Server Error | 서버 내부 오류                        |
| 503       | Service Unavailable   | 서버 일시적 불능                      |

코드로 확인하는 방법은 다음과 같습니다.

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

print(response.status_code)  # 200

if response.status_code == 200:
    print("요청 성공")
elif response.status_code == 404:
    print("해당 데이터 없음")
elif response.status_code >= 500:
    print("서버 오류, 나중에 다시 시도")
```

실무 팁 : 상태 코드를 일일이 if문으로 비교하는 대신, 이후 단계에서 배울 `raise_for_status()` 를 사용하면 4xx, 5xx를 자동으로 예외로 처리할 수 있습니다.

------

### 2-4. Header

헤더는 **"데이터에 대한 데이터(메타데이터)"**입니다. 편투에 붙이는 우표나 주소 외에 적는 '취급주의' 같은 메모라고 생각하면 쉽습니다.

- **User-Agent:** 내가 브라우저인지, 파이썬 코드인지 알려줍니다. (서버가 봇을 차단할 때 체크하는 항목)
- **Content-Type:** 보내는 데이터가 JSON인지, 일반 텍스트인지 알려줍니다.
- **Authorization:** "나 이 서버 관리자야"라는 인증 키를 담을 때 사용합니다.

---

Header는 요청과 응답에 함께 실려 오는 부가 정보입니다. 실제 데이터(Body)가 아니라, 데이터를 어떻게 해석해야 하는지, 요청자가 누구인지 같은 메타 정보를 담습니다.

요청 Header의 대표적인 항목들은 다음과 같습니다.

| Header 이름   | 역할                                          |
| ------------- | --------------------------------------------- |
| Content-Type  | 전송하는 데이터의 형식 (application/json 등)  |
| Authorization | 인증 토큰 전달                                |
| User-Agent    | 요청자 정보 (브라우저인지 Python 코드인지 등) |
| Accept        | 서버에 어떤 형식의 응답을 원하는지 알림       |

requests에서 Header를 붙이는 방법입니다.

```python
import requests

headers = {
    "Authorization": "Bearer my-token-1234",
    "Content-Type": "application/json",
    "User-Agent": "MyApp/1.0"
}

response = requests.get("https://api.example.com/data", headers=headers)
```

응답 Header를 확인하는 방법입니다.

```python
print(response.headers)
# {'Content-Type': 'application/json', 'Date': '...', ...}

print(response.headers["Content-Type"])
# application/json
```

이 단계에서는 Header가 "요청/응답에 붙는 부가 정보 꾸러미"라는 개념만 잡아두면 충분합니다. 구체적인 활용은 인증, Session 단계에서 자연스럽게 다시 나옵니다.

------

## 3. 왜 requests를 쓰는가

Python에는 표준 라이브러리로 `urllib` 이 있습니다. 그런데도 실무에서 requests를 쓰는 이유는 단순합니다. 코드가 훨씬 간결하고 읽기 쉽기 때문입니다. 파이썬에는 기본적으로 통신을 위한 `urllib`이 내장되어 있지만, `requests`는 압도적인 편의성을 제공합니다.

아래는 같은 GET 요청을 urllib과 requests로 각각 작성한 비교입니다.

```python
# urllib 방식 (표준 라이브러리)
import urllib.request
import json

url = "https://jsonplaceholder.typicode.com/posts/1"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode("utf-8"))
print(data)
# requests 방식
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
data = response.json()
print(data)
```

코드 줄 수와 가독성의 차이가 극명합니다.

requests가 실제로 쓰이는 주요 상황은 다음과 같습니다.

**API 호출**

- 날씨, 환율, 지도, 결제 등 외부 서비스의 데이터를 가져오거나 전송할 때 사용합니다.
- 카카오 API, 공공데이터포털, GitHub API 등 모든 REST API 연동의 기본 도구입니다.

**웹 데이터 가져오기**

- 웹 크롤링 / 스크래핑의 첫 번째 단계입니다.
- requests로 HTML을 가져온 뒤 BeautifulSoup 같은 파싱 라이브러리로 분석합니다.

**로그인 / 세션 유지**

- `Session` 객체를 활용하면 로그인 상태를 유지하면서 여러 페이지를 자동으로 탐색할 수 있습니다.

**자동화 스크립트에서 외부 서비스 연동**

- Slack으로 알림 보내기, Notion 페이지 자동 생성, GitHub 이슈 자동 등록 등 반복 업무 자동화에 핵심적으로 쓰입니다.

------





## 4. 핵심 정리

> **[ 요약 ]**
>
> **첫째,** `requests`는 여러분의 파이썬 코드가 웹 서버와 대화할 수 있게 해주는 **"통역사"**입니다.
>
> **둘째,** 통신이 끝나면 반드시 **상태 코드(Status Code)**를 확인하십시오. 200번이 떠야 비로소 다음 로직을 진행할 수 있습니다.
>
> **셋째,** HTTP 통신은 **"가는 요청(Request)이 있어야 오는 응답(Response)이 있다"**는 일방향적인 사이클임을 명심하십시오.

---

이 단계에서 반드시 가져가야 할 개념 두 가지입니다.

**첫째. requests는 "웹에 데이터 요청을 보내는 도구"다**

브라우저가 사람 대신 서버에 요청하듯, requests는 Python 코드 대신 서버에 요청합니다. 브라우저 없이 코드만으로 웹과 통신할 수 있게 해주는 것이 requests의 본질입니다.

**둘째. HTTP 상태 코드와 응답 구조를 이해해야 한다**

요청이 성공했는지 실패했는지, 실패했다면 왜 실패했는지를 판단하는 기준이 상태 코드입니다. 이후 모든 에러 처리, 재시도 로직, 인증 처리는 전부 상태 코드를 기반으로 동작합니다.

```
200번대 : 내가 잘 함, 서버도 잘 함
400번대 : 내가 잘못 요청함
500번대 : 서버가 잘못 처리함
```

이 세 줄만 지금 당장 외워두어도 충분합니다. 나머지는 실습하면서 자연스럽게 익혀집니다.

------

다음 단계인 2단계에서는 GET, POST, PUT, DELETE 등 실제 요청 메서드를 코드로 직접 다룹니다.

