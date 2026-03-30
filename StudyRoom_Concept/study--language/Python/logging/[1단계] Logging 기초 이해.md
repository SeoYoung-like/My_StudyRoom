# 1단계. Python Logging 기초 이해

## 1.1 logging을 사용하는 이유?

많은 입문자가 `print()`로 변수 값을 확인하곤 합니다. 하지만 서비스가 커지면 `print()`는 재앙이 됩니다.

| **구분**      | **print()**                        | **logging**                                 |
| ------------- | ---------------------------------- | ------------------------------------------- |
| **목적**      | 표준 출력(화면)에 즉시 표시        | 프로그램의 상태 기록 및 추적                |
| **제어**      | 하나하나 지우거나 주석 처리해야 함 | **설정 한 줄로 전체 로그 On/Off 가능**      |
| **심각도**    | 구분이 안 됨 (모두 동일함)         | **레벨별(INFO, ERROR 등) 구분 가능**        |
| **저장 위치** | 터미널 화면 (휘발성)               | **파일, 데이터베이스, 이메일 등 전송 가능** |
| **부가 정보** | 수동으로 작성해야 함               | **시간, 파일명, 라인 번호 자동 포함**       |

> **교수의 한마디:** `print()`는 개발자의 혼잣말이라면, `logging`은 시스템이 남기는 공식 일지입니다.

---

```python
# 많은 초보자들이 이렇게 디버깅한다
print("여기 도달함")
print("user_id:", user_id)
print("에러 발생!")
```

**배포할 때 어떻게 하지?** → 하나하나 주석 처리? 삭제? **다시 디버깅 필요하면?** → 다시 하나하나 복구?

이게 `logging`이 존재하는 이유입니다.

------

### 1) print vs logging 비교표

| 항목              | `print()`        | `logging`                           |
| ----------------- | ---------------- | ----------------------------------- |
| 출력 대상         | stdout 고정      | 콘솔 / 파일 / 원격 서버 등 자유롭게 |
| 레벨 구분         | ❌ 없음           | ✅ DEBUG~CRITICAL 5단계              |
| 타임스탬프        | ❌ 직접 구현      | ✅ 자동 포함 가능                    |
| 운영 중 끄기/켜기 | ❌ 코드 수정 필요 | ✅ 레벨 설정 한 줄로 제어            |
| 모듈 위치 추적    | ❌ 불가           | ✅ 파일명, 라인번호 자동 기록        |
| 멀티 모듈 관리    | ❌ 혼재됨         | ✅ 모듈별 독립 관리                  |

------



### 2) 로그를 남기는 3가지 목적

```
① 문제 추적 (Debugging)
   → "언제, 어디서, 무엇이 잘못됐는가?"
   → 재현하기 어려운 버그를 사후에 분석

② 운영 상태 확인 (Monitoring)  
   → "서버가 지금 정상적으로 동작하고 있는가?"
   → 요청 수, 처리 시간, 사용자 활동 추적

③ 에러 기록 (Error Tracking)
   → "어떤 예외가 발생했고 stack trace는?"
   → 운영 중 발생한 에러를 놓치지 않고 기록
```

------



### 3) 실무에서의 결정적 차이

```python
# ❌ print 방식 — 운영 서버에서 이 코드를 어떻게 관리할 것인가?
def process_order(order_id):
    print(f"주문 처리 시작: {order_id}")      # 배포 전에 지워야 하나?
    print(f"DB 조회 중...")                   # 이것도?
    print(f"ERROR: 재고 없음")               # 이건 남겨야 하나?

# ✅ logging 방식 — 레벨로 완전히 제어 가능
import logging

def process_order(order_id):
    logging.debug(f"주문 처리 시작: {order_id}")   # 개발 시에만 출력
    logging.debug(f"DB 조회 중...")                 # 개발 시에만 출력
    logging.error(f"재고 없음: {order_id}")        # 운영에서도 항상 출력
```

> **운영 서버에서 레벨을 `WARNING`으로 설정하면** → `debug()` 호출은 전부 자동으로 무시됨 → 코드 한 줄도 수정 없이!

------



## 1.2 로그 레벨 이해하기 

로그 레벨은 **"이 정보가 얼마나 중요한가?"**를 결정하는 기준입니다. 파이썬은 기본적으로 5가지 표준 레벨을 제공합니다.

- **DEBUG (10):** 개발 단계에서 문제 해결을 위해 남기는 상세 정보 (변수 값 등)
- **INFO (20):** 프로그램이 정상적으로 작동하고 있다는 일반적인 확인 정보 (서버 시작 등)
- **WARNING (30):** 당장 문제는 없지만, 향후 문제가 생길 소지가 있을 때 (API 권장 중단 등)
- **ERROR (40):** 문제가 발생하여 일부 기능이 작동하지 않음 (예외 발생)
- **CRITICAL (50):** 프로그램 자체가 중단될 정도의 치명적인 상황

**필터링 원리:** 설정을 `INFO`로 하면, 그보다 높은 레벨인 `INFO, WARNING, ERROR, CRITICAL`만 출력되고 `DEBUG`는 무시됩니다.



### 1) 레벨 구조 — 숫자가 클수록 심각

```
CRITICAL  50  ── 시스템이 계속 동작할 수 없는 심각한 오류
ERROR     40  ── 기능 일부가 실패한 오류  
WARNING   30  ── 예상치 못한 일이지만 동작은 계속됨  ← 기본값
INFO      20  ── 정상 동작 확인용 정보
DEBUG     10  ── 개발/디버깅용 상세 정보
낮은 레벨 (상세) ◀──────────────────────────▶ 높은 레벨 (심각)
    DEBUG    INFO    WARNING    ERROR    CRITICAL
      10      20       30        40        50
```

> **핵심 원리**: 설정한 레벨 **이상**만 출력된다 → `WARNING`으로 설정하면 `WARNING`, `ERROR`, `CRITICAL`만 출력

------





### 2) 각 레벨 언제 쓰는가 — 실무 기준

```python
import logging

# DEBUG (10) - 개발할 때만 보고 싶은 상세 정보
logging.debug("SQL 쿼리: SELECT * FROM users WHERE id=%s", user_id)
logging.debug("캐시 히트: key=%s", cache_key)

# INFO (20) - 정상 흐름 확인, 운영에서도 남기고 싶은 기록
logging.info("서버 시작됨: port=8080")
logging.info("사용자 로그인 성공: user_id=%s", user_id)
logging.info("주문 처리 완료: order_id=%s", order_id)

# WARNING (30) - 문제는 아니지만 주의가 필요한 상황
logging.warning("디스크 사용량 80%% 초과")
logging.warning("deprecated API 호출됨: /api/v1/old-endpoint")
logging.warning("재시도 발생 (1/3): connection timeout")

# ERROR (40) - 기능이 실패했지만 서버는 살아있음
logging.error("결제 실패: order_id=%s, reason=%s", order_id, reason)
logging.error("파일 읽기 실패: %s", filepath)

# CRITICAL (50) - 즉시 대응이 필요한 심각한 상황
logging.critical("데이터베이스 연결 완전 불가 — 서비스 중단")
logging.critical("디스크 꽉 참 — 로그 기록 불가")
```

------



### 3) 레벨 필터링 원리 직접 확인

```python
import logging

# 레벨을 DEBUG로 설정 → 모든 로그 출력
logging.basicConfig(level=logging.DEBUG)

logging.debug("DEBUG 메시지")      # ✅ 출력
logging.info("INFO 메시지")        # ✅ 출력
logging.warning("WARNING 메시지")  # ✅ 출력
logging.error("ERROR 메시지")      # ✅ 출력
logging.critical("CRITICAL 메시지")# ✅ 출력

# 레벨을 WARNING으로 설정 → WARNING 이상만 출력
logging.basicConfig(level=logging.WARNING)

logging.debug("DEBUG 메시지")      # ❌ 무시됨
logging.info("INFO 메시지")        # ❌ 무시됨
logging.warning("WARNING 메시지")  # ✅ 출력
logging.error("ERROR 메시지")      # ✅ 출력
logging.critical("CRITICAL 메시지")# ✅ 출력
```

------







## 1.3 basicConfig()로 첫 로그 출력해보기 

가장 간단하게 로깅 시스템을 가동하는 방법입니다.

```Python
import logging

# 기본 설정: 레벨을 DEBUG로 설정 (기본값은 WARNING임)
logging.basicConfig(level=logging.DEBUG)

logging.debug("디버깅용 로그 - 상세한 정보를 남깁니다.")
logging.info("정보 로그 - 정상 작동 중임을 알립니다.")
logging.warning("경고 로그 - 주의가 필요합니다.")
logging.error("에러 로그 - 문제가 발생했습니다.")
logging.critical("치명적 로그 - 시스템이 위험합니다.")
```

- **핵심 포인트:** `basicConfig`를 설정하지 않으면 `WARNING` 이상의 로그만 화면에 보입니다. 입문 단계에서는 `level=logging.DEBUG` 설정을 통해 모든 로그를 확인하는 습관을 들이세요.



### 1) 가장 빠른 로깅 시작

```python
import logging

# 아무 설정 없이 — 기본값은 WARNING 레벨, 콘솔 출력
logging.warning("이것만으로도 동작함")
# 출력: WARNING:root:이것만으로도 동작함
```

------



### 2) basicConfig() 주요 파라미터

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,                    # 출력할 최소 레벨
    format="%(asctime)s [%(levelname)s] %(message)s",  # 출력 형식
    datefmt="%Y-%m-%d %H:%M:%S",           # 날짜 형식
)

logging.debug("디버그 메시지")
logging.info("정보 메시지")
logging.warning("경고 메시지")
# 출력 결과
2024-01-15 10:23:45 [DEBUG] 디버그 메시지
2024-01-15 10:23:45 [INFO] 정보 메시지
2024-01-15 10:23:45 [WARNING] 경고 메시지
```



**[ 주의 사항 ]**

`basicConfig`는 최초 1회만 적용된다.

```py
# ⚠️ basicConfig는 최초 1회만 적용됨!
logging.basicConfig(level=logging.DEBUG)    # ✅ 이게 적용됨
logging.basicConfig(level=logging.WARNING)  # ❌ 이미 설정됐으므로 무시됨

# 나중에 레벨을 바꾸려면 이렇게 해야 함
logging.getLogger().setLevel(logging.WARNING)  # ✅ root logger 레벨 변경
```

`basicConfig()`는 "아직 설정이 없을 때만" 동작하기 때문에 두 번째 호출은 사실 무시돼요!





### 3) format에서 쓸 수 있는 주요 속성

```python
# 실무에서 자주 쓰는 포맷 조합
format = "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d — %(message)s"

# 출력 예시
# 2024-01-15 10:23:45 [ERROR] order.py:42 — 결제 실패: order_id=1234
```

| 속성            | 의미        | 예시                  |
| --------------- | ----------- | --------------------- |
| `%(asctime)s`   | 발생 시각   | `2024-01-15 10:23:45` |
| `%(levelname)s` | 레벨 이름   | `DEBUG`, `ERROR`      |
| `%(message)s`   | 로그 메시지 | 내가 작성한 내용      |
| `%(filename)s`  | 파일 이름   | `app.py`              |
| `%(lineno)d`    | 라인 번호   | `42`                  |
| `%(funcName)s`  | 함수 이름   | `process_order`       |
| `%(name)s`      | Logger 이름 | `root`, `myapp`       |

------



### 4) basicConfig()의 중요한 특성

```python
import logging

# basicConfig는 단 한 번만 적용된다
logging.basicConfig(level=logging.DEBUG)   # ✅ 적용됨
logging.basicConfig(level=logging.ERROR)   # ❌ 무시됨! 이미 설정됨

# 이미 설정된 이후에는 force=True 옵션 필요 (Python 3.8+)
logging.basicConfig(level=logging.ERROR, force=True)  # ✅ 강제 재설정
```

> **실무 팁**: `basicConfig()`는 **스크립트 최상단, import 직후**에 딱 한 번만 호출하는 것이 원칙입니다.

------





## 1.4 로그 파일로 저장하기

터미널 화면에만 로그를 찍으면 프로그램 종료 시 사라집니다. 실무에서는 반드시 **파일**로 남겨야 합니다.

```Python
import logging

logging.basicConfig(
    filename='app.log',         # 로그를 저장할 파일명
    filemode='a',               # 'a'는 이어쓰기(Append), 'w'는 새로쓰기
    level=logging.INFO,         # INFO 레벨부터 기록
    format='%(asctime)s - %(levelname)s - %(message)s' # 출력 형식 지정
)

logging.info("이 메시지는 파일에 저장됩니다.")
logging.error("파일에 기록된 에러 메시지입니다.")
```



### 1) 파일 저장 기본

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="app.log",        # 파일명 지정
    filemode="a",              # "a" = 이어쓰기, "w" = 덮어쓰기
    encoding="utf-8",          # 한글 깨짐 방지
)

logging.info("서버 시작")
logging.warning("경고 발생")
logging.error("에러 발생")
# app.log 파일 내용
2024-01-15 10:23:45 [INFO] 서버 시작
2024-01-15 10:23:46 [WARNING] 경고 발생
2024-01-15 10:23:47 [ERROR] 에러 발생
```

------



### 2) 파일 + 콘솔 동시 출력 (실무 패턴)

> `basicConfig()`만으로는 동시 출력이 어렵습니다. **Handler를 직접 추가**하는 방식을 씁니다. (2단계에서 본격적으로 다룸)

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 콘솔 핸들러
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)   # 콘솔엔 WARNING 이상만

# 파일 핸들러  
file_handler = logging.FileHandler("app.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)        # 파일엔 DEBUG부터 전부

# 포맷 설정
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# logger에 핸들러 등록
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 사용
logger.debug("상세 디버그")   # 파일에만 기록
logger.warning("경고!")       # 콘솔 + 파일 모두 기록
logger.error("에러!")         # 콘솔 + 파일 모두 기록
```

------





## [ 1단계 종합 실습 예제 ]

```python
import logging

# ── 설정 ──────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)-8s] %(filename)s:%(lineno)d — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="stage1_practice.log",
    encoding="utf-8",
    filemode="w",
)

# ── 실습: 쇼핑몰 주문 처리 시뮬레이션 ──────────────
def check_stock(item_id: int, quantity: int) -> bool:
    logging.debug("재고 확인 시작: item_id=%d, quantity=%d", item_id, quantity)
    stock = 5  # 실제론 DB 조회
    if quantity > stock:
        logging.warning("재고 부족: 요청=%d, 재고=%d", quantity, stock)
        return False
    logging.info("재고 확인 완료: 충분함")
    return True

def process_payment(amount: int) -> bool:
    logging.debug("결제 시도: amount=%d", amount)
    if amount <= 0:
        logging.error("유효하지 않은 결제 금액: %d", amount)
        return False
    logging.info("결제 성공: %d원", amount)
    return True

def process_order(item_id: int, quantity: int, amount: int):
    logging.info("=== 주문 처리 시작 ===")
    
    if not check_stock(item_id, quantity):
        logging.error("주문 실패: 재고 부족")
        return
    
    if not process_payment(amount):
        logging.critical("결제 시스템 오류 — 즉시 확인 필요")
        return
    
    logging.info("주문 완료: item_id=%d, 수량=%d, 금액=%d원",
                 item_id, quantity, amount)

# ── 실행 ──────────────────────────────────────────
process_order(item_id=101, quantity=3, amount=15000)   # 정상
process_order(item_id=102, quantity=10, amount=50000)  # 재고 부족
process_order(item_id=103, quantity=1, amount=-1000)   # 결제 오류
```

------





## [ 1단계 핵심 정리 ]

```
1. print는 제어 불가 → logging은 레벨로 완전 제어
2. 레벨 5단계: DEBUG(10) < INFO(20) < WARNING(30) < ERROR(40) < CRITICAL(50)
3. 설정 레벨 "이상"만 출력 — 이것이 핵심 필터링 원리
4. basicConfig()는 딱 한 번, 스크립트 최상단에서 호출
5. 파일 저장은 filename= 파라미터로 간단히 가능
6. 콘솔+파일 동시 출력은 Handler를 직접 추가 (→ 2단계에서 심화)
```

> **다음 단계 예고**: 2단계에서는 `Logger / Handler / Formatter / Filter` 4요소의 관계를 이해하고, 실무에서 쓰는 `getLogger(__name__)` 패턴을 배웁니다.

