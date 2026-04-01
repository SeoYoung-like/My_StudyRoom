## 01. Matchers란 무엇인가?

### 1. Matcher의 개념

**Matcher**는 `expect()` 뒤에 붙여서 값을 검증하는 메서드입니다.

```javascript
expect(실제값).toBe(기대값);
//            ^^^^
//            이 부분이 Matcher
```

**비유**: Matcher는 "검사관"입니다.

- `expect()`가 검사할 물건을 내밀면
- Matcher가 "합격/불합격"을 판정합니다



### 2. Matcher의 기본 구조

```javascript
test('테스트 설명', () => {
  const actual = 2 + 2;        // 실제 값
  const expected = 4;          // 기대하는 값
  
  expect(actual).toBe(expected);
  // "2 + 2의 결과가 4와 같아야 한다"
});
```

**실패하는 경우**:

```javascript
test('실패 예시', () => {
  expect(2 + 2).toBe(5);
});

// 에러 메시지:
// Expected: 5
// Received: 4
```





## 02. 동등성 검증 - toBe vs toEqual

이것이 가장 중요하고 가장 헷갈리는 부분입니다!



### 1. toBe() - 원시 타입 :: 엄격한 일치 비교

**toBe()**는 JavaScript의 `===` 연산자와 동일하게 동작합니다.

- **사용 대상**: 숫자, 문자열, 불린, null, undefined
- **용도:** 숫자, 문자열, 불리언(Boolean) 같은 **원시 값(Primitive Value)**이 정확히 같은지 볼 때 씁니다.
- **특징:** 메모리 주소까지 봅니다. (Object.is와 동일)

```javascript
describe('toBe 사용법', () => {
  test('숫자 비교', () => {
    expect(2 + 2).toBe(4);
    expect(10 - 5).toBe(5);
  });

  test('문자열 비교', () => {
    const name = 'John';
    expect(name).toBe('John');
  });

  test('불린 비교', () => {
    expect(true).toBe(true);
    expect(false).toBe(false);
  });

  test('null 비교', () => {
    const value = null;
    expect(value).toBe(null);
  });
});
```

**중요한 특징**: toBe()는 **참조를 비교**합니다.

```javascript
test('객체 비교 - 실패함!', () => {
  const obj1 = { name: 'John' };
  const obj2 = { name: 'John' };
  
  // ❌ 실패! 내용은 같지만 다른 객체(다른 참조)
  expect(obj1).toBe(obj2);
});

test('같은 객체를 참조하면 성공', () => {
  const obj1 = { name: 'John' };
  const obj2 = obj1;  // 같은 객체를 가리킴
  
  // ✅ 성공! 같은 참조
  expect(obj1).toBe(obj2);
});
```



### 2. toEqual() - 객체/배열 :: 내용 일치 비교 ⭐

**toEqual()**은 객체나 배열의 **내용**을 깊이 비교합니다.

- **사용 대상**: 객체, 배열 (가장 많이 사용!)
- **용도:** **객체(Object)나 배열(Array)**을 비교할 때 씁니다.
- **이유:** 자바스크립트에서 `{ a: 1 }`과 `{ a: 1 }`은 모양은 같지만 메모리 주소가 달라서 `toBe`로 비교하면 실패합니다. `toEqual`은 **"내용물(값)이 같은가?"**를 재귀적으로 확인합니다.

```javascript
describe('toEqual 사용법', () => {
  test('객체 내용 비교', () => {
    const user = {
      name: 'John',
      age: 30
    };
    
    // ✅ 내용이 같으면 성공!
    expect(user).toEqual({
      name: 'John',
      age: 30
    });
  });

  test('배열 내용 비교', () => {
    const numbers = [1, 2, 3];
    
    expect(numbers).toEqual([1, 2, 3]);
  });

  test('중첩된 객체 비교', () => {
    const data = {
      user: {
        name: 'Alice',
        address: {
          city: 'Seoul'
        }
      },
      items: [1, 2, 3]
    };
    
    expect(data).toEqual({
      user: {
        name: 'Alice',
        address: {
          city: 'Seoul'
        }
      },
      items: [1, 2, 3]
    });
  });
});
```



### 3. toBe vs toEqual 실전 비교

```javascript
describe('toBe vs toEqual 비교', () => {
  test('원시 타입: 둘 다 사용 가능', () => {
    expect(5).toBe(5);
    expect(5).toEqual(5);  // 둘 다 성공
  });

  test('객체: toEqual 사용 필수', () => {
    const obj = { name: 'John' };
    
    // ❌ 실패
    // expect(obj).toBe({ name: 'John' });
    
    // ✅ 성공
    expect(obj).toEqual({ name: 'John' });
  });

  test('배열: toEqual 사용 필수', () => {
    const arr = [1, 2, 3];
    
    // ❌ 실패
    // expect(arr).toBe([1, 2, 3]);
    
    // ✅ 성공
    expect(arr).toEqual([1, 2, 3]);
  });
});
```

**황금 규칙**:

- **원시 타입** (숫자, 문자열, 불린) → `toBe()` 또는 `toEqual()` (둘 다 가능, toBe 권장)
- **객체, 배열** → `toEqual()` (필수!)

---

```js
test('toBe와 toEqual의 차이', () => {
  const user = { name: 'Kim' };
  
  // expect(user).toBe({ name: 'Kim' }); // FAIL! (메모리 주소가 다름)
  expect(user).toEqual({ name: 'Kim' }); // PASS! (내용이 같음)
  expect(user.name).toBe('Kim');         // PASS! (문자열은 원시 값이므로 toBe 가능)
});
```



### 4. 실전 예시

**예시 1: API 응답 검증**

```javascript
// src/api.js
async function getUser(id) {
  return {
    id: id,
    name: 'John Doe',
    email: 'john@example.com',
    role: 'admin'
  };
}

// src/api.test.js
test('사용자 정보 조회', async () => {
  const user = await getUser(1);
  
  // ✅ 객체이므로 toEqual 사용
  expect(user).toEqual({
    id: 1,
    name: 'John Doe',
    email: 'john@example.com',
    role: 'admin'
  });
});
```

**예시 2: 장바구니 기능**

```javascript
// src/cart.js
class ShoppingCart {
  constructor() {
    this.items = [];
  }

  addItem(item) {
    this.items.push(item);
  }

  getItems() {
    return this.items;
  }
}

// src/cart.test.js
test('장바구니에 상품 추가', () => {
  const cart = new ShoppingCart();
  
  cart.addItem({ name: '사과', price: 1000 });
  cart.addItem({ name: '바나나', price: 1500 });
  
  // ✅ 배열이므로 toEqual 사용
  expect(cart.getItems()).toEqual([
    { name: '사과', price: 1000 },
    { name: '바나나', price: 1500 }
  ]);
});
```







## 03. not - 반대 조건 테스트

- "이게 아니어야 통과"입니다.
- 예: `expect(1 + 1).not.toBe(3);`



### 1. not의 개념

**not**은 Matcher의 결과를 반대로 만듭니다.

```javascript
expect(value).not.toBe(기대하지_않는_값);
// "value가 이 값이 아니어야 한다"
```



### 2. not 활용 예시

```javascript
describe('not 사용법', () => {
  test('같지 않음을 검증', () => {
    expect(2 + 2).not.toBe(5);
    expect('hello').not.toBe('world');
  });

  test('배열에 포함되지 않음', () => {
    const fruits = ['apple', 'banana'];
    expect(fruits).not.toContain('orange');
  });

  test('객체가 다름을 검증', () => {
    const user = { name: 'John', age: 30 };
    
    expect(user).not.toEqual({ name: 'Jane', age: 25 });
  });

  test('속성이 없음을 검증', () => {
    const user = { name: 'John' };
    expect(user).not.toHaveProperty('age');
  });
});
```



### 3. 실전 예시 - 유효성 검증

```javascript
// src/validator.js
function validateEmail(email) {
  return email.includes('@') && email.includes('.');
}

// src/validator.test.js
describe('이메일 검증', () => {
  test('유효한 이메일', () => {
    expect(validateEmail('test@example.com')).toBe(true);
  });

  test('유효하지 않은 이메일', () => {
    // not 사용
    expect(validateEmail('invalid-email')).not.toBe(true);
    // 또는
    expect(validateEmail('invalid-email')).toBe(false);
  });

  test('@ 없는 이메일은 거부', () => {
    expect(validateEmail('test.com')).not.toBe(true);
  });
});
```

------

## 
