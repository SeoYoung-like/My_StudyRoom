# Matchers 로직 검증 

조건문 로직이나 계산 로직을 테스트할 때 필수입니다.



## 01. 참/거짓 검증 - Truthiness

자바스크립트는 `true`/`false` 말고도 참/거짓으로 취급되는 값들이 있죠? 그걸 잡아냅니다.

- **`toBeTruthy()`**: `true`, `1`, `"hello"`, `[]`, `{}` 등
- **`toBeFalsy()`**: `false`, `0`, `""` (빈 문자열), `null`, `undefined`, `NaN`



### 1. toBeTruthy() - true로 평가되는 모든 값

JavaScript에서 조건문에서 `true`로 취급되는 값들을 검증합니다.

```javascript
describe('toBeTruthy 사용법', () => {
  test('true 값들', () => {
    expect(true).toBeTruthy();
    expect(1).toBeTruthy();
    expect(-1).toBeTruthy();
    expect('hello').toBeTruthy();
    expect('0').toBeTruthy();  // 문자열 '0'은 truthy
    expect([]).toBeTruthy();   // 빈 배열도 truthy
    expect({}).toBeTruthy();   // 빈 객체도 truthy
  });

  test('실전 예시: 사용자 로그인 상태', () => {
    const currentUser = { id: 1, name: 'John' };
    expect(currentUser).toBeTruthy();
  });
});
```



### 2. toBeFalsy() - false로 평가되는 모든 값

JavaScript의 **Falsy 값** 6가지를 검증합니다.

```javascript
describe('toBeFalsy 사용법', () => {
  test('false 값들 (6가지)', () => {
    expect(false).toBeFalsy();
    expect(0).toBeFalsy();
    expect('').toBeFalsy();      // 빈 문자열
    expect(null).toBeFalsy();
    expect(undefined).toBeFalsy();
    expect(NaN).toBeFalsy();
  });

  test('실전 예시: 로그아웃 상태', () => {
    const currentUser = null;
    expect(currentUser).toBeFalsy();
  });
});
```



### 3. 명확한 검증: toBeNull, toBeUndefined, toBeDefined

더 명확한 검증을 위한 전용 Matchers입니다.

```javascript
describe('명확한 null/undefined 검증', () => {
  test('null 검증', () => {
    const value = null;
    
    expect(value).toBeNull();
    expect(value).toBeFalsy();      // 이것도 통과하지만
    expect(value).not.toBeUndefined(); // null은 undefined가 아님
  });

  test('undefined 검증', () => {
    let value;
    
    expect(value).toBeUndefined();
    expect(value).toBeFalsy();
  });

  test('defined 검증', () => {
    const value = 0;  // 0도 정의된 값!
    
    expect(value).toBeDefined();
    expect(value).toBeFalsy();  // 하지만 falsy
  });
});
```



### 4. 실전 활용 - 조건부 로직 테스트

```javascript
// src/auth.js
function isLoggedIn(user) {
  return !!user;  // user가 있으면 true
}

function hasPermission(user, permission) {
  return user && user.permissions && user.permissions.includes(permission);
}

// src/auth.test.js
describe('인증 함수 테스트', () => {
  test('사용자가 있으면 로그인 상태', () => {
    const user = { id: 1, name: 'John' };
    expect(isLoggedIn(user)).toBeTruthy();
  });

  test('사용자가 없으면 로그아웃 상태', () => {
    expect(isLoggedIn(null)).toBeFalsy();
    expect(isLoggedIn(undefined)).toBeFalsy();
  });

  test('권한 확인', () => {
    const admin = {
      id: 1,
      permissions: ['read', 'write', 'delete']
    };
    
    expect(hasPermission(admin, 'write')).toBeTruthy();
    expect(hasPermission(admin, 'admin')).toBeFalsy();
  });

  test('권한 정보가 없는 사용자', () => {
    const user = { id: 2 };
    expect(hasPermission(user, 'read')).toBeFalsy();
  });
});
```

------





## 02. 숫자 비교 - 크기와 범위

부등호 대신 사용한다.

- `toBeGreaterThan(n)`: n보다 큰가? (`>`)
- `toBeLessThan(n)`: n보다 작은가? (`<`)
- `toBeGreaterThanOrEqual(n)`: n보다 크거나 같은가? (`>=`)
- `toBeLessThanOrEqual(n)`: n보다 작거나 같은가? (`<=`)



### 1. 기본 비교 Matchers

```javascript
describe('숫자 크기 비교', () => {
  test('보다 큼/작음', () => {
    const age = 25;
    
    expect(age).toBeGreaterThan(18);      // 18보다 큼
    expect(age).toBeGreaterThanOrEqual(25); // 25 이상
    expect(age).toBeLessThan(30);         // 30보다 작음
    expect(age).toBeLessThanOrEqual(25);  // 25 이하
  });

  test('범위 검증', () => {
    const score = 85;
    
    // 0 이상 100 이하
    expect(score).toBeGreaterThanOrEqual(0);
    expect(score).toBeLessThanOrEqual(100);
  });
});
```



### 2. 실전 예시 - 나이 검증

```javascript
// src/age-validator.js
function validateAge(age) {
  if (age < 0) {
    throw new Error('나이는 0 이상이어야 합니다');
  }
  if (age > 150) {
    throw new Error('유효하지 않은 나이입니다');
  }
  return true;
}

function isAdult(age) {
  return age >= 18;
}

function getAgeGroup(age) {
  if (age < 13) return 'child';
  if (age < 20) return 'teenager';
  if (age < 65) return 'adult';
  return 'senior';
}

// src/age-validator.test.js
describe('나이 검증', () => {
  test('유효한 나이 범위', () => {
    const age = 25;
    
    expect(age).toBeGreaterThanOrEqual(0);
    expect(age).toBeLessThanOrEqual(150);
    expect(validateAge(age)).toBe(true);
  });

  test('성인 여부', () => {
    expect(isAdult(25)).toBe(true);
    expect(isAdult(17)).toBe(false);
    expect(isAdult(18)).toBe(true);  // 경계값!
  });

  test('연령대 분류', () => {
    expect(getAgeGroup(10)).toBe('child');
    expect(getAgeGroup(15)).toBe('teenager');
    expect(getAgeGroup(30)).toBe('adult');
    expect(getAgeGroup(70)).toBe('senior');
    
    // 경계값 테스트
    expect(getAgeGroup(13)).toBe('teenager');
    expect(getAgeGroup(20)).toBe('adult');
    expect(getAgeGroup(65)).toBe('senior');
  });
});
```





## 03. 숫자 비교 - 부동소수점 비교

toBeCloseTo() 부동소수점 비교하는데 사용된다.



### toBeCloseTo() 필요성

JavaScript에서 부동소수점 연산은 정확하지 않습니다. 
이는 컴퓨터가 소수를 이진수로 표현하는 방식 때문입니다.

```javascript
// 이런 문제가 발생합니다
0.1 + 0.2 === 0.3  // false (실제로는 0.30000000000000004)

// 따라서 이렇게 테스트하면 실패합니다
test('adding decimals', () => {
  expect(0.1 + 0.2).toBe(0.3);  // ❌ 실패!
});
```



### toBeCloseTo() 문법

```javascript
expect(값).toBeCloseTo(기대값, 소수점자리수);
```

**매개변수:**

- 첫 번째: 비교할 기대값
- 두 번째 (선택): 정밀도 (기본값: 2)



### 작동 원리

`toBeCloseTo()`는 두 값의 차이가 충분히 작은지 확인합니다.

```javascript
test('decimal addition', () => {
  expect(0.1 + 0.2).toBeCloseTo(0.3);  // ✅ 성공!
});
```

내부적으로 이렇게 동작합니다:

```javascript
Math.abs(실제값 - 기대값) < Math.pow(10, -정밀도) / 2
```



### 정밀도 설정

```javascript
test('precision examples', () => {
  const value = 0.1 + 0.2;  // 0.30000000000000004
  
  // 소수점 2자리까지 비교 (기본값)
  expect(value).toBeCloseTo(0.3, 2);     // ✅ 0.30과 비교
  
  // 소수점 5자리까지 비교
  expect(value).toBeCloseTo(0.3, 5);     // ✅ 0.30000과 비교
  
  // 소수점 15자리까지 비교
  expect(value).toBeCloseTo(0.3, 15);    // ❌ 실패! 너무 정밀함
});
```

**정밀도별 허용 오차:**

- `2`: ±0.005 (소수점 둘째 자리까지)
- `3`: ±0.0005 (소수점 셋째 자리까지)
- `5`: ±0.000005 (소수점 다섯째 자리까지)



### 실전 사용 예시

- 부동소수점 연산 결과
- 수학 함수 (삼각함수, 제곱근 등)
- 금융/회계 계산
- 물리/과학 시뮬레이션



#### [ 금융 계산 ]

```javascript
describe('가격 계산', () => {
  it('should calculate total price with tax', () => {
    const price = 100;
    const taxRate = 0.1;
    const total = price * (1 + taxRate);
    
    expect(total).toBeCloseTo(110.0, 2);
  });
  
  it('should calculate discount correctly', () => {
    const original = 99.99;
    const discount = 0.15;
    const final = original * (1 - discount);
    
    expect(final).toBeCloseTo(84.99, 2);
  });
});
```



#### [ 수학/과학 계산 ]

```javascript
describe('원의 넓이 계산', () => {
  it('should calculate area of circle', () => {
    const radius = 5;
    const area = Math.PI * radius * radius;
    
    expect(area).toBeCloseTo(78.54, 2);  // π * 25 ≈ 78.54
  });
});

describe('제곱근 계산', () => {
  it('should calculate square root', () => {
    expect(Math.sqrt(2)).toBeCloseTo(1.414, 3);
  });
});
```



#### [ 게임 개발 (좌표 계산) ]

```javascript
describe('캐릭터 이동', () => {
  it('should calculate position after diagonal movement', () => {
    const speed = 10;
    const angle = Math.PI / 4;  // 45도
    
    const x = speed * Math.cos(angle);
    const y = speed * Math.sin(angle);
    
    expect(x).toBeCloseTo(7.071, 3);
    expect(y).toBeCloseTo(7.071, 3);
  });
});
```





### 주의사항

정밀도를 너무 높게 설정하면 테스트가 불안정해질 수 있습니다.

```javascript
// ⚠️ 피해야 할 패턴
expect(0.1 + 0.2).toBeCloseTo(0.3, 20);  // 너무 정밀함

// ✅ 권장 패턴
expect(0.1 + 0.2).toBeCloseTo(0.3, 2);   // 적절한 정밀도
```

대부분의 경우 소수점 2-5자리 정밀도면 충분합니다. 비즈니스 로직에 필요한 만큼만 정밀하게 검증하는 것이 좋습니다.

---

JavaScript의 부동소수점 연산 오류를 처리합니다.

```javascript
describe('부동소수점 계산', () => {
  test('일반적인 소수 더하기 - 문제 발생!', () => {
    const result = 0.1 + 0.2;
    
    // ❌ 실패! 0.30000000000000004
    // expect(result).toBe(0.3);
    
    // ✅ 성공! 근사값 비교
    expect(result).toBeCloseTo(0.3);
  });

  test('가격 계산', () => {
    const price = 99.99;
    const tax = 0.1;
    const total = price * (1 + tax);
    
    expect(total).toBeCloseTo(109.989);
  });

  test('정밀도 지정', () => {
    // 두 번째 인자: 소수점 자릿수 (기본값: 2)
    expect(0.1 + 0.2).toBeCloseTo(0.3, 5);  // 소수점 5자리까지
  });
});
```

**실무 팁**: 돈이나 측정값 등 부동소수점 계산이 포함된 경우 항상 `toBeCloseTo()`를 사용하세요!
