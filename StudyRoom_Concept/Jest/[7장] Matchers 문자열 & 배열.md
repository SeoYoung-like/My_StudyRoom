## 01. 문자열 검증 - toMatch

- 정규표현식이나 특정 단어 포함 여부를 봅니다.
- 예: `expect("hello world").toMatch(/world/);`



### 1. 기본 문자열 포함 확인

```javascript
describe('문자열 매칭', () => {
  test('부분 문자열 확인', () => {
    const message = 'Hello World';
    
    expect(message).toMatch('World');
    expect(message).toMatch('Hello');
    expect(message).not.toMatch('Goodbye');
  });

  test('정규식 사용', () => {
    const email = 'test@example.com';
    
    // @ 포함 확인
    expect(email).toMatch(/@/);
    
    // 이메일 형식 검증
    expect(email).toMatch(/.*@.*\..*/);
    
    // 대소문자 무시
    expect(email).toMatch(/EXAMPLE/i);
  });
});
```



### 2. 실전 예시 - 이메일 검증

```javascript
// src/validators.js
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function validatePassword(password) {
  // 최소 8자, 대문자 1개, 숫자 1개 포함
  return password.length >= 8 &&
         /[A-Z]/.test(password) &&
         /[0-9]/.test(password);
}

// src/validators.test.js
describe('이메일 검증', () => {
  test('유효한 이메일 형식', () => {
    expect(validateEmail('test@example.com')).toBe(true);
    expect('test@example.com').toMatch(/@/);
    expect('test@example.com').toMatch(/\./);
  });

  test('유효하지 않은 이메일', () => {
    expect(validateEmail('invalid')).toBe(false);
    expect(validateEmail('test@')).toBe(false);
    expect(validateEmail('@example.com')).toBe(false);
  });
});

describe('비밀번호 검증', () => {
  test('유효한 비밀번호', () => {
    const password = 'Password123';
    
    expect(validatePassword(password)).toBe(true);
    expect(password).toMatch(/[A-Z]/);  // 대문자 포함
    expect(password).toMatch(/[0-9]/);  // 숫자 포함
    expect(password.length).toBeGreaterThanOrEqual(8);
  });

  test('유효하지 않은 비밀번호', () => {
    expect(validatePassword('short1')).toBe(false);      // 너무 짧음
    expect(validatePassword('lowercase123')).toBe(false); // 대문자 없음
    expect(validatePassword('PASSWORD')).toBe(false);     // 숫자 없음
  });
});
```



### 3. 에러 메시지 검증

```javascript
describe('에러 메시지 확인', () => {
  test('특정 단어 포함 확인', () => {
    const error = 'User not found in database';
    
    expect(error).toMatch(/not found/);
    expect(error).toMatch(/User/);
    expect(error).toMatch(/database/);
  });

  test('대소문자 구분 없이', () => {
    const error = 'INVALID INPUT';
    
    expect(error).toMatch(/invalid/i);  // i 플래그: 대소문자 무시
  });
});
```





## 02. 배열과 반복 가능 객체

### 1. toContain() - 배열 요소 포함 확인

배열 안에 특정 요소가 들어있는지 확인합니다. 반복문 돌리지 말고 이거 쓰세요.

```js
test('장바구니 확인', () => {
  const cart = ['사과', '바나나', '우유'];
  expect(cart).toContain('바나나'); // PASS
});
```

---

```javascript
describe('배열 요소 확인', () => {
  test('배열에 특정 값 포함', () => {
    const fruits = ['apple', 'banana', 'orange'];
    
    expect(fruits).toContain('banana');
    expect(fruits).not.toContain('grape');
  });

  test('숫자 배열', () => {
    const numbers = [1, 2, 3, 4, 5];
    
    expect(numbers).toContain(3);
    expect(numbers).not.toContain(10);
  });

  test('문자열에 부분 문자열 포함', () => {
    const message = 'Hello World';
    
    expect(message).toContain('World');
    expect(message).toContain('Hello');
  });
});
```



### 2. toHaveLength() - 배열/문자열 길이

- 배열이나 문자열의 길이를 잴 때 씁니다.
- 예: `expect([1, 2, 3]).toHaveLength(3);`

```javascript
describe('길이 검증', () => {
  test('배열 길이', () => {
    const numbers = [1, 2, 3, 4, 5];
    expect(numbers).toHaveLength(5);
  });

  test('문자열 길이', () => {
    const name = 'John';
    expect(name).toHaveLength(4);
  });

  test('빈 배열', () => {
    const empty = [];
    expect(empty).toHaveLength(0);
  });
});
```



### 3. 실전 예시 - 쇼핑몰 기능

```javascript
// src/shopping-cart.js
class ShoppingCart {
  constructor() {
    this.items = [];
  }

  addItem(item) {
    this.items.push(item);
  }

  removeItem(itemName) {
    this.items = this.items.filter(item => item.name !== itemName);
  }

  getItemNames() {
    return this.items.map(item => item.name);
  }

  getTotalItems() {
    return this.items.length;
  }

  hasItem(itemName) {
    return this.items.some(item => item.name === itemName);
  }
}

// src/shopping-cart.test.js
describe('ShoppingCart', () => {
  let cart;

  beforeEach(() => {
    cart = new ShoppingCart();
  });

  test('상품 추가', () => {
    cart.addItem({ name: '사과', price: 1000 });
    
    expect(cart.items).toHaveLength(1);
    expect(cart.getItemNames()).toContain('사과');
    expect(cart.hasItem('사과')).toBe(true);
  });

  test('여러 상품 추가', () => {
    cart.addItem({ name: '사과', price: 1000 });
    cart.addItem({ name: '바나나', price: 1500 });
    cart.addItem({ name: '오렌지', price: 2000 });
    
    expect(cart.items).toHaveLength(3);
    expect(cart.getTotalItems()).toBe(3);
    
    const names = cart.getItemNames();
    expect(names).toContain('사과');
    expect(names).toContain('바나나');
    expect(names).toContain('오렌지');
    expect(names).not.toContain('포도');
  });

  test('상품 제거', () => {
    cart.addItem({ name: '사과', price: 1000 });
    cart.addItem({ name: '바나나', price: 1500 });
    
    cart.removeItem('사과');
    
    expect(cart.items).toHaveLength(1);
    expect(cart.getItemNames()).not.toContain('사과');
    expect(cart.getItemNames()).toContain('바나나');
  });

  test('빈 장바구니', () => {
    expect(cart.items).toHaveLength(0);
    expect(cart.getTotalItems()).toBe(0);
    expect(cart.hasItem('사과')).toBe(false);
  });
});
```

