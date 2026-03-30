## 테스트 실행 옵션

### 1. 기본 실행

```bash
npm test
```

모든 테스트를 1회 실행합니다.



### 2. Watch 모드 (개발 중 최고)

```bash
npm run test:watch
```

**기능**:

- 파일 변경 감지 시 자동 재실행
- 변경된 파일과 관련된 테스트만 실행
- 대화형 메뉴 제공

**대화형 옵션**:

```
Watch Usage
 › Press a to run all tests.
 › Press f to run only failed tests.
 › Press p to filter by a filename regex pattern.
 › Press t to filter by a test name regex pattern.
 › Press q to quit watch mode.
 › Press Enter to trigger a test run.
```

**실무 활용**: 개발 중에는 항상 Watch 모드를 켜두세요. 코드를 저장할 때마다 자동으로 테스트가 실행되어 즉시 피드백을 받을 수 있습니다.



### 3. 특정 파일만 실행

```bash
npm test math.test.js
```

또는

```bash
npm test -- --testPathPattern=math
```



### 4. 코드 커버리지 확인

```bash
npm run test:coverage
```

**출력 예시**:

```
--------------------|---------|----------|---------|---------|-------------------
File                | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s 
--------------------|---------|----------|---------|---------|-------------------
All files           |     100 |      100 |     100 |     100 |                   
 math.js            |     100 |      100 |     100 |     100 |                   
--------------------|---------|----------|---------|---------|-------------------
```

**컬럼 설명**:

- **% Stmts**: 실행된 구문 비율
- **% Branch**: 실행된 분기 (if/else) 비율
- **% Funcs**: 실행된 함수 비율
- **% Lines**: 실행된 코드 라인 비율

`coverage/` 폴더에 HTML 리포트도 생성됩니다:

```bash
# 브라우저로 열기 (Mac)
open coverage/lcov-report/index.html

# 브라우저로 열기 (Windows)
start coverage/lcov-report/index.html
```

