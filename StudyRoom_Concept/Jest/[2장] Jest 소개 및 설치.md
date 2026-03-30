## 1. Jest 소개

### 1-1. Jest란 무엇인가?

**Jest**는 Facebook(현 Meta)에서 개발한 JavaScript 테스팅 프레임워크입니다. 현재 가장 인기 있는 JavaScript 테스트 도구입니다.



#### **Jest가 인기 있는 이유**:

**1) Zero Configuration (설정 없이 바로 사용)**

다른 테스트 도구는 복잡한 설정 파일이 필요하지만, Jest는 설치만 하면 바로 사용할 수 있습니다.

```bash
# 다른 도구들
npm install mocha chai sinon
# + 설정 파일 작성
# + assertion 라이브러리 선택
# + mocking 라이브러리 설치

# Jest
npm install --save-dev jest
# 끝! 바로 사용 가능
```



**2) 빠른 실행 속도**

Jest는 테스트를 병렬로 실행하고, 변경된 파일만 테스트합니다.

```bash
# 첫 실행: 모든 테스트 실행 (5초)
npm test

# 파일 수정 후: 변경된 테스트만 실행 (0.5초)
npm test
```



**3) 풍부한 내장 기능**

별도 라이브러리 없이 다음 기능을 모두 제공합니다:

- Assertion (검증)
- Mocking (모의 객체)
- Code Coverage (코드 커버리지)
- Snapshot Testing (스냅샷 테스팅)
- Watch Mode (자동 재실행)



**4) 훌륭한 에러 메시지**

테스트 실패 시 정확히 무엇이 잘못되었는지 알려줍니다.

```javascript
test('계산 테스트', () => {
  expect(2 + 2).toBe(5);
});

// 에러 메시지:
// Expected: 5
// Received: 4
//
//   3 | test('계산 테스트', () => {
// > 4 |   expect(2 + 2).toBe(5);
//     |                 ^
//   5 | });
```



**Jest를 사용하는 유명 프로젝트**:

- React (Facebook)
- Vue.js
- Node.js 프로젝트 수천 개
- Airbnb, Uber, Twitter 등





## 2. Jest 설치 및 설정

### 2-1. 프로젝트 준비하기

먼저 새로운 프로젝트를 만들어봅시다.

```bash
# 1. 프로젝트 폴더 생성
mkdir jest-tutorial
cd jest-tutorial

# 2. package.json 생성
npm init -y
```

**package.json 파일이 생성됩니다**:

```json
{
  "name": "jest-tutorial",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```



### 2-2. Jest 설치하기

패키지 매니저에 따라 선택하세요.

**npm 사용 시**:

```bash
npm install --save-dev jest
```

**yarn 사용 시**:

```bash
yarn add --dev jest
```

**pnpm 사용 시**:

```bash
pnpm add -D jest
```

**옵션 설명**:

- `--save-dev` (또는 `-D`): 개발 의존성으로 설치
- 개발 의존성: 개발 중에만 필요하고, 실제 서비스에는 필요 없는 패키지

**설치 확인**:

`package.json` 파일을 열어보면 다음과 같이 추가되어 있습니다:
( Jest는 개발할 때만 필요하고 배포될 때는 필요 없으므로 `devDependencies`로 설치합니다. )

```json
{
  "devDependencies": {
    "jest": "^29.7.0"
  }
}
```



### 2-3. package.json에 테스트 명령어 설정하기

`package.json`의 `scripts` 섹션을 다음과 같이 수정합니다:

```js
{
  "scripts": {
    "test": "jest"
  }
}
```

---

```json
{
  "name": "jest-tutorial",
  "version": "1.0.0",
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "devDependencies": {
    "jest": "^29.7.0"
  }
}
```

**실행 테스트**:

```bash
npm test
```

**결과**:

```
No tests found, exiting with code 1
```

정상입니다! 아직 테스트 파일을 만들지 않았으니까요.



---



**[ 1. `"name"`과 `"version"` ]**

이 두 필드는 프로젝트의 **'명함'**이자 **'주민등록증'** 같은 역할을 합니다.

- **`"name": "jest-tutorial"`**
  - **의미:** 이 프로젝트의 이름입니다.
  - **이유:** 나중에 이 프로젝트를 npm에 배포하거나, 다른 프로젝트에서 라이브러리로 불러올 때 식별자로 사용됩니다. 또한 터미널에서 프로젝트를 구분하는 기준이 됩니다. 소문자와 하이픈(`-`)만 사용하는 것이 관례입니다.
- **`"version": "1.0.0"`**
  - **의미:** 프로젝트의 현재 버전입니다.
  - **이유:** 업데이트 기록을 관리하기 위함입니다. 보통 **SemVer(유의적 버전)** 방식을 따릅니다.
    - `1`(Major): 기존 버전과 호환되지 않는 큰 변화가 있을 때
    - `.0`(Minor): 기능이 추가되었지만 기존 기능은 그대로 쓸 수 있을 때
    - `.0`(Patch): 작은 버그 수정





**[ 2. `scripts` (명령어 별칭) ]**

터미널에서 매번 복잡한 명령어를 치기 귀찮으니, 짧은 별명을 붙여주는 곳입니다.

- **`"test": "jest"`**
  - **실행법:** `npm test` 또는 `npm run test`
    - 모든 테스트를 1회 실행
    - CI/CD 환경에서 사용
  - **역할:** 프로젝트 내의 모든 테스트 파일(`.test.js` 또는 `.spec.js`)을 찾아 **딱 한 번** 실행하고 종료합니다. 전체 코드가 잘 돌아가는지 최종 점검할 때 씁니다.
- **`"test:watch": "jest --watch"`**
  - **실행법:** `npm run test:watch`
    - 파일 변경 감지 시 자동으로 테스트 재실행
    - 개발 중에 가장 많이 사용
    - `Ctrl + C`로 종료
  - **역할:** **"관찰 모드"**입니다. 코드를 수정하고 저장할 때마다 Jest가 이를 감지해서 관련 테스트를 자동으로 다시 실행합니다. 개발 중에 실시간으로 피드백을 받을 때 아주 유용합니다.
- **`"test:coverage": "jest --coverage"`**
  - **실행법:** `npm run test:coverage`
    - 코드 커버리지 리포트 생성
    - 테스트가 코드의 몇 %를 검증하는지 확인
  - **역할:** **"테스트 커버리지"** 보고서를 생성합니다. 내 전체 코드 중 몇 %가 테스트되었는지(함수, 줄 수 등)를 표로 보여주며, 보통 `coverage`라는 폴더가 새로 생기면서 그 안에 결과가 담깁니다.



**[ 3. `devDependencies` (개발용 도구) ]**

프로젝트 실행에는 필요 없지만, **개발할 때만 필요한 도구**들을 모아두는 곳입니다.

- **`"jest": "^29.7.0"`**
  - Jest 라이브러리를 설치했다는 기록입니다.
  - `^` (캐럿) 표시는 "29.x.x 버전 중에서 가장 최신 기능을 쓰겠다"는 뜻입니다. 2026년 현재는 더 높은 버전이 있을 수 있지만, 29.x 버전은 매우 안정적인 메이저 버전입니다.



---







### [ Next.js용 `jest.config.js` 설정 ]

Next.js는 자체적인 컴파일러(SWC)를 사용하기 때문에, 일반적인 Jest 설정보다는 Next.js에서 제공하는 전용 설정을 사용하는 것이 훨씬 쉽고 빠릅니다. ( `next/jest`를 활용하면 별도의 Babel 설정 없이 깔끔하게 Jest를 설정할 수 있습니다. )



#### 1) 필수 패키지 설치

먼저 필요한 패키지를 설치하세요:

```bash
npm install -D jest jest-environment-jsdom @testing-library/react @testing-library/jes
```



#### 2) `jest.config.js` (프로젝트 루트에 생성)

프로젝트 루트에 `jest.config.js` 파일을 생성합니다. 
Next.js 16 환경에 최적화된 설정입니다.

```JavaScript
const nextJest = require('next/jest')

const createJestConfig = nextJest({
  dir: './',
})

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
  },
}

module.exports = createJestConfig(customJestConfig)
```

**각 필드 설명:**

- `setupFilesAfterEnv`: 각 테스트 파일 실행 전에 실행할 설정 파일
- `testEnvironment`: 브라우저 환경을 시뮬레이션하는 jsdom 사용
  - `jsdom` 입력해서 사용 가능 : Jest는 사용자의 편의를 위해 다음과 같은 규칙을 가집니다.
    - `'jsdom'` 입력 시 → **`jest-environment-jsdom`** 패키지를 찾음
    - `'node'` 입력 시 → **`jest-environment-node`** 패키지를 찾음
- `moduleNameMapper`: TypeScript path alias 매핑 (`@/components` 같은 경로)





#### 3) `jest.setup.js` 설정 (선택)

프로젝트 루트에 `jest.setup.js` 파일을 생성합니다. 선택 사항이지만 강력 추천합니다.
( Testing Library의 확장 matcher를 사용하기 위한 설정입니다. )

테스트 코드에서 `expect(...).toBeInTheDocument()` 같은 편리한 문법을 쓰기 위해 필요합니다.

```js
// jest.setup.js
import '@testing-library/jest-dom'
```





#### 4) Next.js 16 최적화 설정의 장점

**1) 자동 SWC 변환**

Next.js의 `next/jest` 라이브러리를 사용하면, 별도의 Babel 설정 없이도 `.tsx`, `.ts` 파일을 알아서 이해합니다. 빌드 속도가 매우 빠릅니다.

---

**2) 환경 변수 로드**

`.env.local` 파일에 적어둔 변수들을 테스트 환경에서도 자동으로 인식합니다.

---

**3) 정적 파일 처리**

CSS나 이미지 파일을 불러오는 코드가 있어도 테스트 중에 에러가 나지 않도록 자동으로 가짜(Mock) 처리를 해줍니다.

---





### 2-4. 테스트 실행해보기

이제 아까 `package.json`에 적어둔 명령어로 테스트를 시작하시면 됩니다!

```Bash
npm test
```

만약 프로젝트의 `app/` 폴더 안에 있는 컴포넌트들을 테스트할 계획이라면, 위 설정이 가장 표준적인 가이드가 될 것입니다. 진행하시다 막히는 에러가 있으면 바로 말씀해 주세요!





## 4. 테스트 파일 규칙

### 4-1. Jest가 테스트 파일을 찾는 방법

Jest는 다음 패턴의 파일을 자동으로 테스트 파일로 인식합니다:

**규칙 1: `\*.test.js` 패턴** (가장 많이 사용)

```
src/
  utils/
    calculator.js          # 실제 코드
    calculator.test.js     # 테스트 코드
  services/
    userService.js
    userService.test.js
```

**규칙 2: `\*.spec.js` 패턴**

```
src/
  components/
    Button.jsx
    Button.spec.jsx
  utils/
    formatter.js
    formatter.spec.js
```

**규칙 3: `__tests__` 폴더**

```
src/
  utils/
    calculator.js
    __tests__/
      calculator.test.js
      calculator-advanced.test.js
```

**어떤 규칙을 사용해야 하나?**

실무에서는 **`\*.test.js`** 방식을 가장 많이 사용합니다:

- 원본 파일과 테스트 파일을 같은 폴더에 배치
- import 경로가 짧아짐 (`./calculator` vs `../utils/calculator`)
- 파일 찾기가 쉬움

**예시 프로젝트 구조**:

```
my-project/
├── package.json
├── src/
│   ├── math.js
│   ├── math.test.js
│   ├── string-utils.js
│   └── string-utils.test.js
└── node_modules/
```





### 4-2. 파일 확장자

Jest는 다음 확장자를 모두 지원합니다:

- `.js` - 일반 JavaScript
- `.jsx` - React JSX
- `.ts` - TypeScript
- `.tsx` - TypeScript JSX
- `.mjs` - ES Modules

**예시**:

- `calculator.test.js` ✅
- `Button.test.jsx` ✅
- `utils.spec.ts` ✅
- `Component.test.tsx` ✅

