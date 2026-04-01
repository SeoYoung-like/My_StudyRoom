**세미콜론 자동 삽입 기능(ASI)**

자바스크립트 엔진은 세미콜론 자동 삽입 기능(ASI)이 있어 세미콜론을 생략해도 대부분 작동한다.

자바스크립트는 문의 끝에 세미콜론이 없으면 엔진이 자동으로 삽입해주는 ASI 기능을 가지고 있습니다.


-----

**원시 타입(Primitive Type)**

* 원시 타입 (primitive data type)
  * number
  * string
  * boolean
  * null
  * undefined
  * symbol (New in ECMAScript 6)

* 객체 타입 (Object data type)
  * object



----------------------


## 비교 정리

```javascript
// 더하기 (+) - 문자열 연결 우선
console.log(5 + 5);             // 10 (숫자)
console.log(5 + "5");           // "55" (문자열)
console.log("5" + 5);           // "55" (문자열)
console.log("5" + "5");         // "55" (문자열)

// 빼기 (-) - 숫자 연산 우선
console.log(5 - 5);             // 0 (숫자)
console.log(5 - "5");           // 0 (숫자)
console.log("5" - 5);           // 0 (숫자)
console.log("5" - "5");         // 0 (숫자)

// 곱하기 (*) - 숫자 연산 우선
console.log(5 * 5);             // 25 (숫자)
console.log(5 * "5");           // 25 (숫자)
console.log("5" * 5);           // 25 (숫자)
console.log("5" * "5");         // 25 (숫자)

// 나누기 (/) - 숫자 연산 우선
console.log(10 / 5);            // 2 (숫자)
console.log(10 / "5");          // 2 (숫자)
console.log("10" / 5);          // 2 (숫자)
console.log("10" / "5");        // 2 (숫자)
```

------



## 4. 실전 예제 및 주의사항

### 예제 1: 사용자 입력 처리

```javascript
// prompt는 항상 문자열 반환!
const input1 = prompt("첫 번째 숫자:");  // "10"
const input2 = prompt("두 번째 숫자:");  // "20"

console.log(input1 + input2);           // "1020" ❌ (문자열 연결)

// 올바른 방법
console.log(Number(input1) + Number(input2));  // 30 ✅
console.log(parseInt(input1) + parseInt(input2));  // 30 ✅
console.log(+input1 + +input2);         // 30 ✅ (단항 + 연산자)
```

### 예제 2: 헷갈리는 경우

```javascript
let a = "5";
let b = 3;

console.log(a + b);     // "53" (문자열 연결)
console.log(a - b);     // 2 (숫자 빼기)
console.log(a * b);     // 15 (숫자 곱하기)
console.log(a / b);     // 1.666... (숫자 나누기)
```

### 예제 3: 복합 연산

```javascript
let x = "10";
let y = "5";

// 괄호로 명확하게!
console.log((+x) + (+y));           // 15 (숫자 덧셈)
console.log(Number(x) + Number(y)); // 15 (숫자 덧셈)

// 빼기는 자동 변환
console.log(x - y);                 // 5
```

### 예제 4: 변환 실패

```javascript
console.log("abc" - 5);             // NaN
console.log("10abc" - 5);           // NaN
console.log("abc" * 2);             // NaN
console.log("abc" / 2);             // NaN

// parseInt는 앞부분만 변환
console.log(parseInt("10abc"));     // 10
console.log(Number("10abc"));       // NaN
```

------

## 5. 명시적 변환 방법

### 문자열 → 숫자

```javascript
// 방법 1: Number()
Number("123");                      // 123
Number("12.5");                     // 12.5
Number("abc");                      // NaN

// 방법 2: parseInt() / parseFloat()
parseInt("123");                    // 123
parseInt("123.45");                 // 123 (정수만)
parseFloat("123.45");               // 123.45
parseInt("10abc");                  // 10 (앞부분만)

// 방법 3: 단항 + 연산자
+"123";                             // 123
+"12.5";                            // 12.5

// 방법 4: 수학 연산 이용
"123" * 1;                          // 123
"123" / 1;                          // 123
"123" - 0;                          // 123
```

### 숫자 → 문자열

```javascript
// 방법 1: String()
String(123);                        // "123"

// 방법 2: toString()
(123).toString();                   // "123"

// 방법 3: 빈 문자열 더하기
123 + "";                           // "123"

// 방법 4: 템플릿 리터럴
`${123}`;                           // "123"
```

------

## 6. 핵심 정리 표

| 연산자 | 숫자 + 숫자 | 문자열 + 숫자    | 동작 방식        |
| ------ | ----------- | ---------------- | ---------------- |
| **+**  | 10 + 5 = 15 | "10" + 5 = "105" | 문자열 연결 우선 |
| **-**  | 10 - 5 = 5  | "10" - 5 = 5     | 숫자 연산 우선   |
| *****  | 10 * 5 = 50 | "10" * 5 = 50    | 숫자 연산 우선   |
| **/**  | 10 / 5 = 2  | "10" / 5 = 2     | 숫자 연산 우선   |
| **%**  | 10 % 3 = 1  | "10" % 3 = 1     | 숫자 연산 우선   |

------

## 7. 베스트 프랙티스

```javascript
// ❌ 나쁜 예: 암묵적 변환에 의존
let result = userInput + 10;  // userInput이 문자열이면?

// ✅ 좋은 예: 명시적 변환
let result = Number(userInput) + 10;
let result2 = parseInt(userInput) + 10;

// ❌ 나쁜 예: 헷갈리는 코드
console.log(1 + 2 + "3" + 4 + 5);  // "3345"

// ✅ 좋은 예: 명확한 의도
console.log((1 + 2) + String(3) + String(4) + String(5));
```

**핵심 기억:**

- `+` 연산자는 **문자열 연결 우선** (하나라도 문자열이면 모두 문자열로!)
- `-`, `*`, `/`, `%` 연산자는 **숫자 연산 우선** (자동으로 숫자 변환 시도)
- 변환 실패 시 `NaN` 반환
- **명시적 변환**이 암묵적 변환보다 안전하고 명확!



---



**[] (빈 배열)**

자바스크립트에서 빈 배열([])이나 빈 객체({})는 객체 타입이므로 Truthy 값으로 평가됩니다.




-----------------



**문자열**

문자열은 원시 타입으로 불변성을 가지므로, 인덱스로 접근하여 일부 문자를 변경하려고 해도 반영되지 않고 원본이 유지됩니다.
(ex) var str = 'Hello'; str[0] = 'h'; console.log(str); // 결과: 'Hello'




-----------------



**단항 산술 연산자(Unary operator) '+'의 효과**

피연산자를 숫자 타입으로 변환하여 반환한다.
+'10'은 숫자 10이 되고, +true는 1이 되는 등 피연산자를 숫자로 변환하는 효과가 있습니다.



---