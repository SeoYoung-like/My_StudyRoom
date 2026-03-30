## 01. 첫 테스트 파일 작성하기

### 1. 실제 코드 작성

먼저 테스트할 간단한 함수를 만들어봅시다.

**src/math.js** (실제 코드)

```javascript
// 두 수를 더하는 함수
function add(a, b) {
  return a + b;
}

// 두 수를 빼는 함수
function subtract(a, b) {
  return a - b;
}

// 두 수를 곱하는 함수
function multiply(a, b) {
  return a * b;
}

// 두 수를 나누는 함수
function divide(a, b) {
  if (b === 0) {
    throw new Error('0으로 나눌 수 없습니다');
  }
  return a / b;
}

// 다른 파일에서 사용할 수 있도록 export
module.exports = {
  add,
  subtract,
  multiply,
  divide
};
```



### 2. 첫 테스트 작성

**src/math.test.js** (테스트 코드)

```javascript
// 테스트할 함수들을 import
const { add, subtract, multiply, divide } = require('./math');

// 첫 번째 테스트
test('1 + 2는 3이다', () => {
  expect(add(1, 2)).toBe(3);
});
```

**코드 한 줄씩 이해하기**:

```javascript
test('1 + 2는 3이다', () => {
  // test(): Jest가 제공하는 함수
  // 첫 번째 인자: 테스트 설명 (한글 가능!)
  // 두 번째 인자: 실제 테스트 로직을 담은 함수
  
  expect(add(1, 2)).toBe(3);
  // expect(): 검증할 값을 전달
  // toBe(): Matcher - 기대하는 값과 일치하는지 확인
});
```



### 3. 테스트 실행

터미널에서 실행합니다:

```bash
npm test
```

**성공 시 출력**:

```
 PASS  src/math.test.js
  ✓ 1 + 2는 3이다 (3 ms)

Test Suites: 1 passed, 1 total
Tests:       1 passed, 1 total
Snapshots:   0 total
Time:        1.234 s
Ran all test suites.
```

**축하합니다! 🎉 첫 테스트를 성공적으로 작성하고 실행했습니다!**



### 4. 더 많은 테스트 추가하기

```javascript
const { add, subtract, multiply, divide } = require('./math');

test('1 + 2는 3이다', () => {
  expect(add(1, 2)).toBe(3);
});

test('5 - 3은 2이다', () => {
  expect(subtract(5, 3)).toBe(2);
});

test('3 * 4는 12이다', () => {
  expect(multiply(3, 4)).toBe(12);
});

test('10 / 2는 5이다', () => {
  expect(divide(10, 2)).toBe(5);
});

test('0으로 나누면 에러가 발생한다', () => {
  expect(() => {
    divide(10, 0);
  }).toThrow('0으로 나눌 수 없습니다');
});
```

**실행 결과**:

```
 PASS  src/math.test.js
  ✓ 1 + 2는 3이다 (2 ms)
  ✓ 5 - 3은 2이다 (1 ms)
  ✓ 3 * 4는 12이다 (1 ms)
  ✓ 10 / 2는 5이다 (1 ms)
  ✓ 0으로 나누면 에러가 발생한다 (1 ms)

Tests: 5 passed, 5 total
```







## 02. describe로 테스트 그룹화하기

### 1. describe()란?

관련된 테스트들을 논리적으로 그룹화하는 함수입니다. 
테스트가 많아지면 조직화가 필수입니다.

이제 코드를 작성해 봅시다. 테스트 코드는 문법이 아니라 **패턴**입니다.

**[ 기본 구조 ]**

```javascript
describe('그룹 이름', () => {
  test('테스트 1', () => {
    // ...
  });

  test('테스트 2', () => {
    // ...
  });
});
```



#### 1.1. 기본 구조: describe, test(it)

테스트 파일은 보통 **그룹(describe) - 개별 테스트(test) - 검증(expect)**의 계층 구조를 가집니다.

```javascript
// math.test.js

// 1. describe: 테스트 그룹 만들기 (관련된 테스트들을 묶어주는 폴더 역할)
describe('계산기 사칙연산 테스트', () => {

  // 2. test: 개별 테스트 케이스 (실제 검증 시나리오)
  test('1 더하기 2는 3이어야 한다', () => {
    // 검증 로직 (Expectation)
    expect(1 + 2).toBe(3);
  });

  // 3. it: test와 기능은 100% 똑같습니다. (문장을 자연스럽게 읽히게 할 때 사용)
  // "It should return..." 처럼 영어 문장을 만들 때 주로 씁니다.
  it('양수와 음수를 더하면 올바른 값을 반환해야 한다', () => {
    expect(5 + (-3)).toBe(2);
  });

});
```

#### 1.2. 핵심 요약

- **`describe()`**: "자, 이제부터 **이 기능**을 테스트할 거야." (명찰 달기)
- **`test()` 혹은 `it()`**: "구체적으로 **이 상황**에서 잘 되는지 보자." (체크리스트)
- **`expect(A).toBe(B)`**: "결과값 A가 기대값 B와 **같니?**" (채점하기)



### 2. 실전 예시

**src/math.test.js** (개선된 버전)

```javascript
const { add, subtract, multiply, divide } = require('./math');

describe('수학 계산 함수', () => {
  
  describe('add 함수', () => {
    test('양수 덧셈', () => {
      expect(add(2, 3)).toBe(5);
    });

    test('음수 덧셈', () => {
      expect(add(-1, -2)).toBe(-3);
    });

    test('0과의 덧셈', () => {
      expect(add(5, 0)).toBe(5);
    });
  });

  describe('subtract 함수', () => {
    test('양수 뺄셈', () => {
      expect(subtract(5, 3)).toBe(2);
    });

    test('음수 뺄셈', () => {
      expect(subtract(-5, -3)).toBe(-2);
    });
  });

  describe('multiply 함수', () => {
    test('양수 곱셈', () => {
      expect(multiply(3, 4)).toBe(12);
    });

    test('0과의 곱셈', () => {
      expect(multiply(5, 0)).toBe(0);
    });

    test('음수 곱셈', () => {
      expect(multiply(-2, 3)).toBe(-6);
    });
  });

  describe('divide 함수', () => {
    test('정상적인 나눗셈', () => {
      expect(divide(10, 2)).toBe(5);
    });

    test('0으로 나누면 에러 발생', () => {
      expect(() => divide(10, 0)).toThrow();
    });
  });

});
```

**실행 결과** (계층 구조로 표시됨):

```
 PASS  src/math.test.js
  수학 계산 함수
    add 함수
      ✓ 양수 덧셈 (2 ms)
      ✓ 음수 덧셈 (1 ms)
      ✓ 0과의 덧셈 (1 ms)
    subtract 함수
      ✓ 양수 뺄셈 (1 ms)
      ✓ 음수 뺄셈 (1 ms)
    multiply 함수
      ✓ 양수 곱셈 (1 ms)
      ✓ 0과의 곱셈 (1 ms)
      ✓ 음수 곱셈 (1 ms)
    divide 함수
      ✓ 정상적인 나눗셈 (1 ms)
      ✓ 0으로 나누면 에러 발생 (2 ms)

Tests: 10 passed, 10 total
```



### 3. describe() 중첩

describe 안에 describe를 중첩할 수 있습니다:

```javascript
describe('사용자 관리', () => {
  
  describe('회원가입', () => {
    test('유효한 정보로 가입 성공', () => {
      // ...
    });

    test('중복 이메일은 거부', () => {
      // ...
    });
  });

  describe('로그인', () => {
    describe('성공 케이스', () => {
      test('올바른 이메일과 비밀번호', () => {
        // ...
      });
    });

    describe('실패 케이스', () => {
      test('잘못된 비밀번호', () => {
        // ...
      });

      test('존재하지 않는 사용자', () => {
        // ...
      });
    });
  });

});
```

**실무 팁**: 2-3단계 정도의 중첩이 적당합니다. 너무 깊으면 오히려 복잡해집니다.

------

## 03 test() vs it() - 무엇을 사용할까?

### 1. 둘은 완전히 동일합니다

Jest에서 `test()`와 `it()`은 **완전히 같은 함수**입니다. 별칭(alias) 관계입니다.

```javascript
// 이 두 개는 완전히 동일
test('덧셈이 작동한다', () => {
  expect(add(2, 3)).toBe(5);
});

it('덧셈이 작동한다', () => {
  expect(add(2, 3)).toBe(5);
});
```



### 2. 언제 무엇을 사용하나?

**test() 스타일** (권장):

```javascript
test('사용자를 생성할 수 있다', () => {
  // ...
});

test('중복 이메일은 거부한다', () => {
  // ...
});
```

**장점**:

- 명확하고 직관적
- Jest 공식 문서에서 주로 사용
- 초보자가 이해하기 쉬움



**it() 스타일** (BDD):

```javascript
describe('UserService', () => {
  it('should create a new user', () => {
    // ...
  });

  it('should reject duplicate emails', () => {
    // ...
  });
});
```

**특징**:

- BDD(Behavior-Driven Development) 스타일
  - **Behavior-Driven Development(행동 주도 개발)**의 약자입니다. 코드가 "무엇을 하는지"보다 "어떻게 행동해야 하는지"에 초점을 맞추는 개발 방법론입니다.

- 영어로 읽었을 때 자연스러움: "it should create a new user"
  - 자연어처럼 읽힌다
  - `it`이라는 주어가 테스트 대상(UserService)을 가리키므로, 마치 문장을 읽는 것처럼 자연스럽습니다.

- RSpec(Ruby), Jasmine에서 유래





### 3. 실무 권장사항

**저의 권장: `test()` 사용**

이유:

1. 더 명확하고 직관적
2. Jest 공식 문서의 주요 방식
3. 한글 설명과도 잘 어울림
4. 팀원 전체가 쉽게 이해

```javascript
// test() - 자연스러움
test('비밀번호는 8자 이상이어야 한다', () => {
  // ...
});

// it() - 한글과는 어색함
it('비밀번호는 8자 이상이어야 한다', () => {
  // ...
});
```

**하지만**: 팀의 컨벤션을 따르세요. 일관성이 가장 중요합니다.
