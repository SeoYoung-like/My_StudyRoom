## 2단계. Logger 구조 이해

Python의 `logging` 모듈은 단순히 콘솔에 텍스트를 찍는 도구가 아닙니다. 이는 복잡한 분산 시스템이나 대규모 애플리케이션에서 **'시스템의 혈류'**를 추적하는 정교한 프레임워크입니다. 오늘 설명할 이 구조를 정확히 이해해야 나중에 "왜 로그가 두 번 찍히지?", "왜 파일에는 로그가 안 남지?" 같은 실무적인 트러블슈팅을 완벽히 해낼 수 있습니다.

Python `logging` 모듈의 아키텍처는 처음 만날 때 "왜 이렇게 복잡한가" 싶지만, 4개의 핵심 요소만 제대로 이해하면 이후 모든 설정이 자연스럽게 따라옵니다. 
단계별로 설명하겠습니다.



### 2.1 Logger / Handler / Formatter / Filter — 4요소 개념

Python의 로깅 아키텍처는 역할을 엄격히 분리하여 유연성을 확보합니다. 

`logging` 모듈은 로그가 생성되는 순간부터 출력되는 순간까지 네 가지 객체가 파이프라인처럼 연결되어 동작합니다.
각 요소를 코드와 함께 정리하면 다음과 같습니다.![image-20260331204204015](./assets/image-20260331204204015.png)



| 구성 요소     | 설명                                                         | 역할                                            | 비유                                          |
| :------------ | :----------------------------------------------------------- | :---------------------------------------------- | --------------------------------------------- |
| **Logger**    | 로그를 생성하는 통로입니다. 애플리케이션 코드에서 직접 호출하는 객체이며, 이름 기반의 계층 구조를 갖습니다. `logger.info("메시지")` 처럼 사용합니다. | 로그 메시지를 생성하고 전달하는 진입점          | **방송국** (뉴스를 만들고 송출함)             |
| **Handler**   | 생성된 로그를 어디로 보낼지 결정합니다. 하나의 Logger에 여러 Handler를 붙일 수 있어서, 같은 로그를 동시에 콘솔과 파일 두 곳에 보낼 수 있습니다. | 생성된 로그를 특정 목적지(콘솔, 파일 등)로 전송 | **송신탑** (TV, 라디오, 스마트폰으로 전달)    |
| **Formatter** | 로그의 출력 형태를 결정합니다. 시간, 레벨, 파일명, 라인 번호 등을 어떤 순서로, 어떤 형식으로 출력할지 지정합니다. | 로그 데이터의 최종 출력 형태(레이아웃) 결정     | **자막/편집** (시간, 뉴스 헤드라인 등 배치)   |
| **Filter**    | 특정 조건에 맞는 로그만 골라내는 필터입니다. 입문 단계에서는 개념만 이해하면 충분합니다. | 어떤 로그를 통과시키고 차단할지 정밀 제어       | **검열관** (특정 키워드나 조건에 따른 필터링) |

```python
import logging

# 기본 구조를 직접 조립하는 예시
logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()           # Handler: 콘솔로 출력
formatter = logging.Formatter(             # Formatter: 출력 형식 지정
    "%(asctime)s [%(levelname)s] %(message)s"
)
handler.setFormatter(formatter)            # Handler에 Formatter 부착
logger.addHandler(handler)                 # Logger에 Handler 부착

logger.info("서버가 시작되었습니다.")
# 출력: 2024-03-15 10:23:01,234 [INFO] 서버가 시작되었습니다.
```





### 2.2 `getLogger(__name__)` 패턴 — 모듈별 Logger 분리

실무에서 가장 권장되는 패턴 방식은 `logging.info()` 같은 기본 함수를 직접 호출하는 것이 아니라, `getLogger()`를 통해 **이름이 있는 로거**를 생성하는 것입니다.
각 파이썬 파일 상단에 아래 한 줄을 선언하는 것이 관례입니다.

```python
logger = logging.getLogger(__name__)
```

`__name__`은 파이썬이 자동으로 채워주는 현재 모듈의 이름입니다. 
`myproject/api/views.py` 파일이라면 `__name__`은 `"myproject.api.views"`가 됩니다.

이 패턴을 쓰는 이유는 두 가지입니다. 

---

**[ 왜 `__name__`을 사용하는가? ]**

`__name__`은 Python의 내장 변수로, 현재 모듈의 경로를 담고 있습니다. (예: `project.services.auth`). 

1. **발생지 추적:**

   * 로그 메시지만 봐도 어느 모듈에서 발생했는지 즉시 파악할 수 있습니다. 

2. **설정의 유연성:** 

   * 특정 패키지(예: `auth` 관련 모듈)의 로그 레벨만 `DEBUG`로 낮추어 상세히 보는 등의 개별 제어가 가능해집니다.

   * 모듈별로 로그 레벨이나 핸들러를 독립적으로 제어할 수 있습니다.

```python
# myproject/db/connection.py
import logging
logger = logging.getLogger(__name__)
# → logger 이름: "myproject.db.connection"

# myproject/api/views.py
import logging
logger = logging.getLogger(__name__)
# → logger 이름: "myproject.api.views"
```

이렇게 하면 나중에 DB 관련 로그만 DEBUG 레벨로, API 로그는 WARNING 이상만 출력하는 식의 세밀한 제어가 가능해집니다.







### 2.3 로거 계층 구조 (Hierarchy)

Python의 `logging` 모듈의 Logger들은 **점(.)으로 구분된 계층 구조**를 가집니다.

* Logger 이름에 `.` 이 들어가면 **자동으로 계층 구조**가 만들어집니다.
* 자식 Logger가 남긴 로그는 기본적으로 **부모 Logger 쪽으로 전달**됩니다.
* 맨 위 끝에는 **Root Logger**가 있습니다.
* 그래서 **Root Logger에만 Handler를 달아도**, 대부분의 하위 Logger 로그를 한 번에 처리할 수 있습니다.
* 핵심은 **"로그가 위로 올라간다"** 는 것입니다.
  * 이를 **이벤트 전달(Propagation)**이라고 합니다.
* 이렇게 계층을 만드는 이유는 "<u>관리의 편의성</u>" 때문입니다. 

---

* **Root Logger:** 모든 로거의 최상위 부모입니다. `logging.getLogger()`처럼 이름을 주지 않으면 접근할 수 있습니다.
* **Child Logger:** `logging.getLogger('parent.child')` 형태로 생성됩니다.
* **상속 관계:** `a.b` 로거는 `a` 로거의 설정을 상속받거나, 발생한 로그를 부모에게 전달합니다.

```
Root Logger                    ← logging.getLogger() 또는 logging.getLogger("")
├── myproject                  ← logging.getLogger("myproject")
│   ├── myproject.api          ← logging.getLogger("myproject.api")
│   │   └── myproject.api.views
│   └── myproject.db
│       └── myproject.db.connection
├── django                     ← 서드파티 라이브러리의 Logger
└── sqlalchemy
```

`getLogger(__name__)`을 쓰면 이 계층이 프로젝트 폴더 구조와 자동으로 일치하게 됩니다. 별도로 이름을 설계할 필요가 없다는 점이 핵심입니다.



#### 1) `basicConfig()`가 왜 편리한가?

```python
# 이 한 줄이
logging.basicConfig(level=logging.DEBUG)

# 내부적으로 이렇게 동작합니다
root_logger = logging.getLogger("")   # Root Logger 가져와서
root_logger.addHandler(StreamHandler()) # 핸들러를 Root에만 붙임
root_logger.setLevel(logging.DEBUG)
```

Root에만 핸들러를 달아도, **프로젝트 전체 어디서 찍든** 로그가 다 올라와서 출력됩니다.

```python
import logging

# Root Logger에만 핸들러 설정
logging.basicConfig(level=logging.DEBUG, format="%(name)s - %(message)s")

# 여러 depth의 로거들
logA = logging.getLogger("myproject")
logB = logging.getLogger("myproject.api")
logC = logging.getLogger("myproject.api.views")

logA.info("A에서 찍음")
logB.info("B에서 찍음")
logC.info("C에서 찍음")
# 출력 결과
myproject - A에서 찍음
myproject.api - B에서 찍음
myproject.api.views - C에서 찍음
```

핸들러를 Root에만 달았는데, **모든 자식 로거의 로그가 전부 출력**됩니다.



#### 2) `getLogger(__name__)`이 왜 좋은가?

```
프로젝트 구조               __name__ 값               로거 이름
myproject/
├── api/
│   └── views.py    →   "myproject.api.views"   →  자동으로 계층 형성
└── db/
    └── models.py   →   "myproject.db.models"   →  자동으로 계층 형성
```

파일마다 `logging.getLogger(__name__)` 하나씩 쓰면, 파일 구조 그대로 로거 계층이 만들어집니다. 이름을 직접 설계할 필요가 없습니다.





### 2.4 Logger 전파(propagate) 동작 방식

[주의! 실수 구간] 로거에서 발생한 이벤트는 **자기 자신의 Handler**뿐만 아니라, **부모 로거의 Handler**로도 전달됩니다.

* **동작 원리:** `child` 로거에서 로그 발생 -> `child` 핸들러 실행 -> `parent` 로거로 전달 -> `parent` 핸들러 실행 -> `root` 로거까지 반복.
* **주의 사항:** 만약 부모와 자식 로거 모두에 `StreamHandler`(콘솔 출력)가 등록되어 있다면 로그가 중복해서 출력됩니다.
* **제어 방법:** **<u>`logger.propagate = False`</u>** 설정을 통해 부모 로거로의 전달을 끊을 수 있습니다.

전파(propagate)는 자식 Logger가 생성한 로그 레코드를 부모 Logger 쪽으로 계속 올려보내는 동작입니다. 
기본값은 `True`이며, 이 동작을 이해하지 못하면 로그가 두 번 출력되는 문제를 만나게 됩니다.

```python
# myproject.api.views에서 logger.warning("뭔가 문제 발생") 호출 시:
# 1단계: myproject.api.views → 자신의 Handler로 처리
# 2단계: propagate=True → myproject.api로 전달
# 3단계: propagate=True → myproject로 전달
# 4단계: propagate=True → Root Logger로 전달 → Root의 Handler로도 처리
```

결과적으로 각 단계에 Handler가 붙어 있으면 같은 메시지가 여러 번 출력됩니다. 아래가 전파로 인한 중복 출력을 막는 일반적인 해결 방법입니다.

```python
# 방법 1: 자식 Logger의 propagate를 False로 끄기
logger = logging.getLogger("myproject.api")
logger.propagate = False   # Root Logger로 전달하지 않음

# 방법 2 (권장): Handler는 Root Logger에만 붙이고
#               자식 Logger들은 Handler 없이 레벨만 설정
logging.basicConfig(level=logging.DEBUG)  # Root에만 Handler

child_logger = logging.getLogger("myproject.db")
child_logger.setLevel(logging.WARNING)    # 이 모듈은 WARNING 이상만
# Handler가 없으므로 Root로 전파되어 처리됨 → 중복 없음
```

실무에서는 방법 2가 훨씬 흔합니다. 
Root Logger에 Handler 설정을 집중시키고, 개별 Logger는 레벨만 제어하는 구조가 관리하기 쉽기 때문입니다.

------





### 2.5. 로그 메시지 예쁘게 만들기 (Formatter)

로그는 나중에 '검색'하기 편해야 합니다. 따라서 표준화된 포맷이 필수적입니다.

#### 1) 실무에서 자주 쓰는 포맷 변수

* `%(asctime)s`: 로그 발생 시간
* `%(levelname)s`: 로그 레벨 (INFO, ERROR 등)
* `%(name)s`: 로거 이름 (어느 모듈인지 확인)
* `%(filename)s`, `%(lineno)d`: 파일명과 줄 번호 (디버깅 시 핵심)
* `%(message)s`: 실제 로그 내용



#### 2) 추천 포맷 예시

Formatter에서 사용할 수 있는 주요 필드와 실무에서 자주 쓰는 포맷 두 가지를 정리합니다.

```python
# 1. 기본 스타일 (시간 + 레벨 + 메시지)
"%(asctime)s - %(levelname)s - %(message)s"

# 2. 상세 디버깅 스타일 (시간 + 레벨 + 로거이름 + 파일명:줄번호 + 메시지)
"%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d) - %(message)s"
```

---

```python
# 포맷 필드 주요 목록
# %(asctime)s    → 시간 (예: 2024-03-15 10:23:01,234)
# %(levelname)s  → 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# %(name)s       → Logger 이름 (myproject.api.views)
# %(filename)s   → 파일명 (views.py)
# %(lineno)d     → 줄 번호 (42)
# %(funcName)s   → 함수명 (create_user)
# %(message)s    → 실제 로그 메시지

# 실무 포맷 1: 시간 + 레벨 + 로거 이름 + 메시지
fmt1 = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
# 출력: 2024-03-15 10:23:01,234 [WARNING] myproject.db.connection - DB 연결 실패

# 실무 포맷 2: 시간 + 파일명 + 줄번호 + 메시지 (디버깅에 특화)
fmt2 = "%(asctime)s %(filename)s:%(lineno)d - %(message)s"
# 출력: 2024-03-15 10:23:01,234 connection.py:87 - DB 연결 실패
```

포맷 문자열의 `%s` 방식은 파이썬의 오래된 문자열 포맷 방식(`%` 연산자)과 동일한 문법입니다. `logging` 모듈이 내부적으로 이 방식을 채택하고 있어서 f-string이나 `.format()`이 아닌 `%` 기호를 씁니다.

메시지 자체를 구성할 때도 `%s` 방식을 권장합니다. `logging` 모듈은 실제로 그 레벨이 출력될 때만 문자열을 조합하기 때문에, f-string을 쓰면 레벨 필터에 걸려 출력되지 않더라도 문자열 조합이 먼저 실행되어 불필요한 연산이 생깁니다.

```python
# 권장: 실제 출력될 때만 문자열 조합
logger.debug("사용자 %s 가 로그인 시도", user_id)

# 비권장: 출력 여부와 무관하게 항상 문자열 조합
logger.debug(f"사용자 {user_id} 가 로그인 시도")
```



#### 3) 메시지 구성 팁

로그 메시지 내부에서 변수를 조합할 때는 f-string보다 **지연 로딩(Lazy Evaluation)** 방식을 권장합니다.

* **Bad:** `logger.debug(f"User {user_id} login attempt")` (로그 레벨이 낮아도 f-string 연산이 발생함)
* **Good:** `logger.debug("User %s login attempt", user_id)` (실제 로그를 남길 때만 문자열을 조합함)





### 2.6. 전체 구조를 조립한 실무 예시

```python
import logging

def setup_logging():
    # Root Logger 설정 (Handler는 여기에만)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # 콘솔 Handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    ))

    # 파일 Handler (모든 레벨 기록)
    file_h = logging.FileHandler("app.log")
    file_h.setLevel(logging.DEBUG)
    file_h.setFormatter(logging.Formatter(
        "%(asctime)s %(filename)s:%(lineno)d - %(message)s"
    ))

    root.addHandler(console)
    root.addHandler(file_h)

    # DB 모듈은 WARNING 이상만 (SQL 쿼리 로그 등 억제)
    logging.getLogger("myproject.db").setLevel(logging.WARNING)

# 각 모듈 파일에서는 이 한 줄만
logger = logging.getLogger(__name__)
```

이 구조를 프로젝트 초기에 `setup_logging()` 한 번만 호출해두면, 이후 각 모듈은 `getLogger(__name__)` 선언만으로 계층 구조에 자동 편입되어 별도의 Handler 설정 없이 로그가 흘러갑니다. 이것이 `logging` 모듈 설계의 핵심 의도입니다.



### [ 요약 ]

1. **Logger**는 입구, **Handler**는 출구, **Formatter**는 옷(양식)입니다.
2. 항상 `logging.getLogger(__name__)`을 사용하여 모듈별로 독립된 로거를 생성하세요.
3. 로그가 중복 출력된다면 **Propagate** 설정을 확인하세요.
4. 로깅 포맷에는 반드시 **시간, 레벨, 발생 위치(모듈/라인)**를 포함하여 사후 추적이 가능하게 만드세요.

