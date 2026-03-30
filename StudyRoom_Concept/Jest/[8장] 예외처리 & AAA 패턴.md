## 01. 예외 처리 테스트 - toThrow

"에러가 나야 정상인 상황"을 테스트합니다. 
(예: 비밀번호 없이 로그인 시도하면 에러가 터져야 함)

**⚠️ 주의할 점:** 함수를 실행해버리면 테스트가 터집니다. **함수를 래핑(Wrapping)**해서 넘겨야 합니다.

```js
function errorFunc() {
  throw new Error("잘못된 입력입니다");
}

test('에러가 제대로 발생하는가?', () => {
  // expect(errorFunc()).toThrow();  <-- 틀림! (실행되어 테스트 중단됨)
  
  expect(() => errorFunc()).toThrow(); // <-- 정답! (함수 자체를 전달)
  expect(() => errorFunc()).toThrow("잘못된 입력입니다"); // 에러 메시지까지 확인 가능
});
```



### 1. toThrow() 기본 사용법

에러가 발생해야 정상인 경우를 테스트합니다.

**중요**: 함수를 직접 호출하지 말고, **함수 자체를 전달**해야 합니다!

```javascript
describe('toThrow 기본', () => {
  test('에러 발생 확인', () => {
    function throwError() {
      throw new Error('Something went wrong');
    }
    
    // ✅ 올바른 방법: 함수를 전달
    expect(() => throwError()).toThrow();
    
    // ❌ 잘못된 방법: 함수를 직접 호출
    // expect(throwError()).toThrow();  // 에러!
  });

  test('특정 에러 메시지 확인', () => {
    function divide(a, b) {
      if (b === 0) {
        throw new Error('0으로 나눌 수 없습니다');
      }
      return a / b;
    }
    
    expect(() => divide(10, 0)).toThrow('0으로 나눌 수 없습니다');
    expect(() => divide(10, 0)).toThrow(/나눌 수 없습니다/);
  });
});
```



### 2. 실전 예시 - 입력 검증

```javascript
// src/user-service.js
class UserService {
  createUser(userData) {
    // 필수 필드 검증
    if (!userData.email) {
      throw new Error('이메일은 필수입니다');
    }
    
    if (!userData.password) {
      throw new Error('비밀번호는 필수입니다');
    }
    
    // 이메일 형식 검증
    if (!userData.email.includes('@')) {
      throw new Error('유효하지 않은 이메일 형식입니다');
    }
    
    // 비밀번호 길이 검증
    if (userData.password.length < 8) {
      throw new Error('비밀번호는 최소 8자 이상이어야 합니다');
    }
    
    return {
      id: Date.now(),
      ...userData
    };
  }

  deleteUser(userId) {
    if (!userId) {
      throw new Error('사용자 ID가 필요합니다');
    }
    
    if (typeof userId !== 'number') {
      throw new Error('사용자 ID는 숫자여야 합니다');
    }
    
    return true;
  }
}

// src/user-service.test.js
describe('UserService', () => {
  let service;

  beforeEach(() => {
    service = new UserService();
  });

  describe('createUser - 성공 케이스', () => {
    test('유효한 데이터로 사용자 생성', () => {
      const userData = {
        email: 'test@example.com',
        password: 'password123'
      };
      
      const user = service.createUser(userData);
      
      expect(user).toHaveProperty('id');
      expect(user.email).toBe('test@example.com');
    });
  });

  describe('createUser - 에러 케이스', () => {
    test('이메일 없이 호출하면 에러', () => {
      expect(() => {
        service.createUser({ password: 'password123' });
      }).toThrow('이메일은 필수입니다');
    });

    test('비밀번호 없이 호출하면 에러', () => {
      expect(() => {
        service.createUser({ email: 'test@test.com' });
      }).toThrow('비밀번호는 필수입니다');
    });

    test('잘못된 이메일 형식', () => {
      expect(() => {
        service.createUser({
          email: 'invalid-email',
          password: 'password123'
        });
      }).toThrow('유효하지 않은 이메일 형식입니다');
      
      // 정규식으로도 확인 가능
      expect(() => {
        service.createUser({
          email: 'invalid-email',
          password: 'password123'
        });
      }).toThrow(/이메일 형식/);
    });

    test('짧은 비밀번호', () => {
      expect(() => {
        service.createUser({
          email: 'test@test.com',
          password: 'short'
        });
      }).toThrow('비밀번호는 최소 8자 이상이어야 합니다');
    });
  });

  describe('deleteUser', () => {
    test('유효한 ID로 삭제 성공', () => {
      expect(service.deleteUser(123)).toBe(true);
    });

    test('ID 없이 호출하면 에러', () => {
      expect(() => {
        service.deleteUser();
      }).toThrow('사용자 ID가 필요합니다');
    });

    test('숫자가 아닌 ID는 에러', () => {
      expect(() => {
        service.deleteUser('123');
      }).toThrow('사용자 ID는 숫자여야 합니다');
    });
  });
});
```



### 3. 매개변수가 있는 함수의 에러 테스트

```javascript
describe('매개변수가 있는 함수 에러 테스트', () => {
  function divide(a, b) {
    if (b === 0) throw new Error('0으로 나눌 수 없습니다');
    if (typeof a !== 'number' || typeof b !== 'number') {
      throw new Error('숫자만 입력 가능합니다');
    }
    return a / b;
  }

  test('다양한 에러 상황', () => {
    // 화살표 함수로 감싸서 전달
    expect(() => divide(10, 0)).toThrow();
    expect(() => divide('10', 2)).toThrow('숫자만 입력 가능합니다');
    expect(() => divide(10, '2')).toThrow(/숫자만/);
  });
});
```



### 4. 비동기 함수의 에러 테스트

```javascript
describe('비동기 에러 테스트', () => {
  async function fetchUser(id) {
    if (!id) {
      throw new Error('ID는 필수입니다');
    }
    // API 호출 시뮬레이션
    return { id, name: 'John' };
  }

  test('비동기 함수 에러', async () => {
    // await + expect + rejects 조합
    await expect(fetchUser()).rejects.toThrow('ID는 필수입니다');
  });

  // 또는
  test('비동기 함수 에러 - try/catch', async () => {
    try {
      await fetchUser();
      // 에러가 발생하지 않으면 테스트 실패
      throw new Error('에러가 발생해야 합니다');
    } catch (error) {
      expect(error.message).toMatch(/ID는 필수/);
    }
  });
});
```





## 02. AAA 패턴으로 테스트 작성하기

테스트 코드를 짤 때 이 3단 구조를 지키는 습관을 들이세요. 가독성이 10배 좋아집니다.

1. **Arrange (준비):** 변수 선언, 객체 생성 등 준비 단계.
2. **Act (실행):** 테스트할 함수 실행.
3. **Assert (검증):** 결과가 맞는지 `expect`로 확인.

```js
describe('계산기 테스트', () => {
  test('2와 3을 더하면 5가 된다', () => {
    // 1. Arrange (준비)
    const a = 2;
    const b = 3;

    // 2. Act (실행)
    const result = a + b;

    // 3. Assert (검증)
    expect(result).toBe(5);
  });
});
```



### 1. AAA 패턴이란?

**Arrange-Act-Assert** (준비-실행-검증) 패턴은 모든 테스트의 기본 구조입니다.

```javascript
test('테스트 설명', () => {
  // Arrange (준비): 테스트에 필요한 데이터와 환경 설정
  const input = '준비 데이터';
  
  // Act (실행): 테스트하려는 동작 수행
  const result = functionToTest(input);
  
  // Assert (검증): 결과가 예상과 일치하는지 확인
  expect(result).toBe('예상 결과');
});
```



### 2. AAA 패턴 실전 적용

```javascript
// src/calculator.js
class Calculator {
  add(a, b) {
    return a + b;
  }

  subtract(a, b) {
    return a - b;
  }

  multiply(a, b) {
    return a * b;
  }

  divide(a, b) {
    if (b === 0) {
      throw new Error('0으로 나눌 수 없습니다');
    }
    return a / b;
  }
}

// src/calculator.test.js
describe('Calculator', () => {
  test('두 수를 더한다', () => {
    // Arrange
    const calculator = new Calculator();
    const a = 5;
    const b = 3;
    const expected = 8;
    
    // Act
    const result = calculator.add(a, b);
    
    // Assert
    expect(result).toBe(expected);
  });

  test('나눗셈에서 0으로 나누면 에러', () => {
    // Arrange
    const calculator = new Calculator();
    const a = 10;
    const b = 0;
    
    // Act & Assert (에러 테스트는 함께)
    expect(() => calculator.divide(a, b)).toThrow('0으로 나눌 수 없습니다');
  });
});
```



### 3. 복잡한 예시 - 할인 계산

```javascript
// src/discount-calculator.js
class DiscountCalculator {
  calculateTotal(items, coupon = null) {
    // 기본 합계
    let total = items.reduce((sum, item) => sum + item.price, 0);
    
    // 쿠폰 적용
    if (coupon) {
      if (coupon.type === 'percent') {
        total = total * (1 - coupon.value / 100);
      } else if (coupon.type === 'fixed') {
        total = Math.max(0, total - coupon.value);
      }
    }
    
    // VIP 추가 할인 (10만원 이상)
    if (total >= 100000) {
      total = total * 0.95;
    }
    
    return Math.round(total);
  }
}

// src/discount-calculator.test.js
describe('DiscountCalculator', () => {
  let calculator;

  beforeEach(() => {
    // 각 테스트 전에 새 인스턴스 생성
    calculator = new DiscountCalculator();
  });

  test('쿠폰 없이 기본 합계 계산', () => {
    // Arrange
    const items = [
      { name: '사과', price: 1000 },
      { name: '바나나', price: 1500 },
      { name: '오렌지', price: 2000 }
    ];
    const expected = 4500;
    
    // Act
    const total = calculator.calculateTotal(items);
    
    // Assert
    expect(total).toBe(expected);
  });

  test('퍼센트 쿠폰 적용', () => {
    // Arrange
    const items = [{ name: '상품', price: 10000 }];
    const coupon = { type: 'percent', value: 20 };  // 20% 할인
    const expected = 8000;
    
    // Act
    const total = calculator.calculateTotal(items, coupon);
    
    // Assert
    expect(total).toBe(expected);
  });

  test('고정 금액 쿠폰 적용', () => {
    // Arrange
    const items = [{ name: '상품', price: 10000 }];
    const coupon = { type: 'fixed', value: 3000 };  // 3000원 할인
    const expected = 7000;
    
    // Act
    const total = calculator.calculateTotal(items, coupon);
    
    // Assert
    expect(total).toBe(expected);
  });

  test('VIP 추가 할인 (10만원 이상)', () => {
    // Arrange
    const items = [
      { name: '고가상품1', price: 60000 },
      { name: '고가상품2', price: 40000 }
    ];
    const expected = 95000;  // 100000 * 0.95
    
    // Act
    const total = calculator.calculateTotal(items);
    
    // Assert
    expect(total).toBe(expected);
    expect(total).toBeLessThan(100000);
  });

  test('쿠폰 + VIP 할인 중복 적용', () => {
    // Arrange
    const items = [
      { name: '고가상품', price: 100000 }
    ];
    const coupon = { type: 'percent', value: 10 };  // 10% 할인
    
    // 계산 과정:
    // 1. 기본: 100000
    // 2. 쿠폰 10%: 90000
    // 3. VIP 5%: 85500
    const expected = 85500;
    
    // Act
    const total = calculator.calculateTotal(items, coupon);
    
    // Assert
    expect(total).toBe(expected);
  });

  test('할인 후 0원 미만이 되지 않음', () => {
    // Arrange
    const items = [{ name: '저가상품', price: 1000 }];
    const coupon = { type: 'fixed', value: 2000 };  // 2000원 할인
    
    // Act
    const total = calculator.calculateTotal(items, coupon);
    
    // Assert
    expect(total).toBe(0);
    expect(total).toBeGreaterThanOrEqual(0);
  });
});
```





## 03. Matchers 총정리 치트시트

### 자주 사용하는 Matchers

```javascript
// ===== 동등성 =====
expect(value).toBe(값);              // 원시 타입 (===)
expect(value).toEqual(값);           // 객체/배열 내용 비교 ⭐
expect(value).not.toBe(값);          // 반대

// ===== Truthiness =====
expect(value).toBeTruthy();          // true로 평가
expect(value).toBeFalsy();           // false로 평가
expect(value).toBeNull();            // null
expect(value).toBeUndefined();       // undefined
expect(value).toBeDefined();         // 정의됨

// ===== 숫자 =====
expect(num).toBeGreaterThan(3);      // > 3
expect(num).toBeGreaterThanOrEqual(3); // >= 3
expect(num).toBeLessThan(5);         // < 5
expect(num).toBeLessThanOrEqual(5);  // <= 5
expect(num).toBeCloseTo(0.3);        // 부동소수점 ⭐

// ===== 문자열 =====
expect(str).toMatch(/pattern/);      // 정규식 매칭
expect(str).toMatch('substr');       // 부분 문자열

// ===== 배열/반복 =====
expect(arr).toContain(item);         // 요소 포함 ⭐
expect(arr).toHaveLength(3);         // 길이 ⭐

// ===== 객체 =====
expect(obj).toHaveProperty('key');   // 속성 존재
expect(obj).toHaveProperty('key', value); // 속성과 값

// ===== 예외 =====
expect(() => fn()).toThrow();        // 에러 발생 ⭐
expect(() => fn()).toThrow('msg');   // 특정 메시지
expect(() => fn()).toThrow(/pattern/); // 정규식
```

