# 나만의 퀴즈 게임 (second-mission)

터미널에서 동작하는 **Python 콘솔 퀴즈 게임**입니다.
메뉴에서 번호를 골라 퀴즈 풀기 / 추가 / 목록 / 점수 확인 / 종료를 할 수 있고,
퀴즈와 최고 점수는 `state.json`에 저장되어 프로그램을 다시 실행해도 유지됩니다.

## 1. 프로젝트 개요
- Codyssey 입학연수 2차 미션 "컴퓨터에게 명령 내리는 말(파이썬) 처음 배우기"의 결과물입니다.
- Python 기본 문법(변수, 조건문, 반복문, 함수)과 클래스(`Quiz`, `QuizGame`), 파일 입출력(JSON), 예외 처리(`try/except`)를 한 프로그램에 적용했습니다.
- Git으로 기능 단위 커밋, 브랜치 생성/병합, `clone`/`pull` 을 실습하고 GitHub에 공개했습니다.
- Python 3.10+ **표준 라이브러리만** 사용합니다 (외부 라이브러리 없음).

## 2. 퀴즈 주제와 선정 이유
- **주제: 한국 상식/역사** (한글 창제, 이순신, 3·1 운동, 남한 최고봉, 광복절, 팔만대장경)
- 선정 이유: 정답이 명확해 오답 시비가 없고, 누구나 아는 내용이라 게임 흐름(출제 → 입력 → 정오답 → 점수)을 검증하기 좋습니다. 또한 퀴즈를 직접 추가하며 확장하기에도 부담이 적습니다.

## 3. 실행 방법
```bash
# 1) 저장소 복제
git clone https://github.com/jyk901/codyssey-second-mission.git
cd codyssey-second-mission

# 2) 실행 (Python 3.10 이상)
python main.py
```
- 메뉴에서 `1`~`5` 숫자를 입력합니다. (앞뒤 공백은 무시됩니다.)
- `Ctrl+C` 를 누르거나 입력 스트림이 끊겨도 안내 후 저장하고 안전하게 종료합니다.

## 4. 기능 목록
| 메뉴 | 기능 | 설명 |
|---|---|---|
| 1 | 퀴즈 풀기 | 풀 문제 수 선택 → 무작위 출제 → 정답 번호 입력(`h`=힌트) → 정답/오답 안내 → 결과 표시 (퀴즈가 없으면 안내) |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호(1~4), 힌트(선택)를 입력받아 등록하고 즉시 `state.json`에 저장 |
| 3 | 퀴즈 목록 | 등록된 퀴즈의 문제 목록 출력 (퀴즈가 없으면 안내) |
| 4 | 점수 확인 | 최고 점수와 전체 게임 기록 출력 (아직 풀지 않았다면 안내). 퀴즈를 풀 때마다 비교·갱신·저장 |
| 5 | 퀴즈 삭제 | 목록에서 번호를 골라 삭제하고 즉시 `state.json`에 반영 |
| 6 | 종료 | 저장 후 종료 |

### 보너스 과제 구현 내용
| 보너스 | 구현 |
|---|---|
| 랜덤 출제 | `random.sample()` 로 문제 순서를 무작위로 섞어 출제 |
| 문제 수 선택 | 퀴즈 풀기 시작 시 풀 문제 수(1~전체) 입력 |
| 힌트 기능 | `Quiz.hint` 속성 추가, 풀이 중 `h` 입력 시 힌트 표시. 문제당 1회 사용 시 점수 = (정답 수 − 힌트 수 × 0.5) ÷ 문제 수 × 100 (최소 0점) |
| 퀴즈 삭제 | 메뉴 5번, 삭제 후 파일 반영 |
| 점수 기록 히스토리 | 날짜/시간, 푼 문제 수, 정답 수, 점수를 `history` 에 누적 저장·표시 |

**공통 입력/예외 처리**: 앞뒤 공백 제거 · 숫자 변환 실패(`abc`) · 허용 범위 밖(메뉴 `9`, 정답 `0`) · 빈 입력(Enter)은 모두 안내 메시지 후 재입력합니다. `KeyboardInterrupt`/`EOFError` 는 비정상 종료 없이 저장 후 종료합니다.

**데이터 파일 복구**: `state.json` 이 없으면 기본 퀴즈로 시작하고, 손상되었거나 구조가 틀리면 안내 후 `state.json.corrupt` 로 백업하고 기본 퀴즈로 복구합니다.

## 5. 파일 구조
```
second-mission/
├── main.py        # 진입점 (UTF-8 출력 설정, QuizGame 실행)
├── game.py        # QuizGame 클래스: 메뉴, 풀기/추가/목록/점수/삭제/기록, state.json 저장/불러오기
├── quiz.py        # Quiz 클래스: 문제/선택지/정답/힌트, 출력·정답 확인·dict 변환
├── quiz_data.py   # 기본 퀴즈 데이터 6개+힌트 (Quiz 인스턴스 생성)
├── inputs.py      # 입력 처리 함수 (read_int, read_answer, read_text, read_optional)
├── state.json     # 저장 데이터 (퀴즈 목록 + 최고 점수 + 게임 기록)
├── docs/
│   └── evidence.md  # 실행 증거 텍스트(환경/메뉴/풀기/추가/점수/삭제/git log/push)
├── .gitignore
└── README.md
```

### 클래스 설계
- `Quiz`: 속성 `question`, `choices`(4개), `answer`(1~4 번호), `hint` / 메서드 `display()`, `is_correct()`, `to_dict()`, `from_dict()`
- `QuizGame`: 속성 `quizzes`, `best_score`, `best_correct`, `best_total`, `history` / 메서드 `show_menu()`, `play_quiz()`, `add_quiz()`, `show_quiz_list()`, `show_score()`, `delete_quiz()`, `ask_answer()`, `record_history()`, `load_state()`, `save_state()`, `run()` 등

## 6. 데이터 파일 설명 (`state.json`)
- **경로**: 프로젝트 루트의 `state.json` (UTF-8, `ensure_ascii=False`)
- **역할**: 프로그램을 종료해도 추가한 퀴즈와 최고 점수가 유지되도록 하는 저장소 (데이터 영속성)
- **스키마**

```json
{
    "quizzes": [
        {
            "question": "훈민정음(한글)을 창제한 조선의 왕은?",
            "choices": ["태조", "세종대왕", "정조", "영조"],
            "answer": 2,
            "hint": "한글 반포일을 기념하는 한글날이 있는 왕"
        }
    ],
    "best_score": 83,
    "best_correct": 5,
    "best_total": 6,
    "history": [
        {"played_at": "2026-11-09 13:17:53", "solved": 6, "correct": 5, "score": 83}
    ]
}
```

| 키 | 타입 | 설명 |
|---|---|---|
| `quizzes` | list | 퀴즈 목록. 각 항목은 `question`(문자열), `choices`(문자열 4개), `answer`(정답 번호 1~4), `hint`(문자열, 없으면 `""`, 생략 가능) |
| `best_score` | int | 최고 점수 (100점 만점, 정답 수 ÷ 문제 수 × 100 반올림) |
| `best_correct` | int | 최고 점수를 기록한 판의 정답 수 |
| `best_total` | int | 최고 점수를 기록한 판의 문제 수 (`0` 이면 아직 풀지 않은 상태) |
| `history` | list | 모든 게임 기록. 항목: `played_at`(날짜/시간), `solved`(푼 문제 수), `correct`(정답 수), `score`(점수). 생략 시 빈 목록 |

### JSON 저장 방식의 한계와 대비 전략
`state.json` 한 파일에 모든 데이터를 저장하는 방식은 이 프로젝트 규모(퀴즈 수십 개, 혼자 사용)에서는 단순하고 읽기 쉬워 적합합니다. 하지만 아래 한계가 있어 규모가 커지면 다른 방식이 필요합니다.

| 한계 | 설명 | 대비(안내) |
|---|---|---|
| **대용량 성능** | 저장할 때마다 파일 전체를 다시 씁니다. 퀴즈·기록이 수만 건이 되면 저장 시간이 길어지고, 특히 `history` 는 게임할 때마다 계속 늘어납니다. | 기록과 퀴즈를 파일로 분할(예: `quizzes.json`, `history.json`)하거나 오래된 기록을 보관 파일로 분리, 또는 DB 사용 |
| **메모리** | 실행 시 파일 전체를 읽어 메모리(`list`/`dict`)에 올립니다. 데이터가 커지면 메모리 사용량이 함께 커지고, 일부만 읽는 것이 불가능합니다. | 필요한 부분만 조회할 수 있는 DB(SQLite 등)나 한 줄씩 처리하는 JSON Lines 형식 |
| **동시 접근** | 프로그램을 두 개 동시에 실행해 같은 파일에 저장하면 한쪽의 변경이 덮어써질 수 있고, 잠금(lock) 기능이 없습니다. | 파일 잠금, 또는 트랜잭션을 지원하는 DB(SQLite, PostgreSQL 등) |
| **검색·부분 수정** | 특정 퀴즈만 찾거나 고치려 해도 전체를 읽고 다시 써야 하며 인덱스가 없습니다. | DB의 조건 검색과 인덱스 |

**현재 적용한 안전장치**: 저장 시 임시 파일(`state.json.tmp`)에 먼저 쓴 뒤 `os.replace()` 로 교체해, 저장 도중 종료되어도 기존 파일이 반쯤 쓰인 상태로 깨지는 것을 줄였습니다. 또한 파일이 손상되면 `state.json.corrupt` 로 백업하고 기본 데이터로 복구합니다. (동시 접근 문제까지 해결하는 것은 아닙니다.)

**결론**: 단일 사용자·소규모 데이터인 이번 미션에서는 JSON이 적절하며, 사용자가 늘거나 데이터가 대용량이 되면 DB(예: SQLite)로 전환하는 것이 다음 단계입니다. 이때 저장·불러오기 로직을 `QuizGame.load_state()` / `save_state()` 두 메서드에 모아 두었기 때문에 저장 방식을 바꿔도 다른 코드의 수정 범위가 작습니다.

## 6-1. 클래스를 사용한 이유 (객체지향 vs 함수형)
이 프로그램은 `Quiz`(퀴즈 한 개)와 `QuizGame`(게임 전체)이라는 두 클래스로 역할을 나눴습니다.

**클래스란?** 데이터(속성)와 그 데이터를 다루는 동작(메서드)을 하나로 묶은 설계도입니다. `__init__` 은 객체를 만들 때 속성을 초기화하는 메서드이고, `self` 는 "지금 이 객체 자신"을 가리켜 각 객체가 자기 데이터를 갖게 해 줍니다.

| 구분 | `Quiz` | `QuizGame` |
|---|---|---|
| 맡은 역할 | 문제 1개의 데이터와 동작 | 게임 흐름과 전체 상태 관리 |
| 속성 | `question`, `choices`, `answer`, `hint` | `quizzes`, `best_score`, `history` 등 |
| 메서드 | `display()`, `is_correct()`, `to_dict()`, `from_dict()` | `play_quiz()`, `add_quiz()`, `load_state()`, `save_state()` 등 |

**함수만으로 만들었다면?** 퀴즈를 `dict` 로 들고 다니며 `show_quiz(quiz)`, `check_answer(quiz, n)` 처럼 데이터를 매번 인자로 넘기는 방식이 됩니다. 작은 프로그램에서는 더 짧고 단순하다는 장점이 있습니다. 하지만 다음 문제가 생깁니다.

| 비교 | 함수형(함수 + dict) | 클래스(객체지향) — 이 프로젝트의 선택 |
|---|---|---|
| 데이터 구조 | `dict` 의 키 이름을 코드 곳곳에서 문자열로 직접 사용해 오타·누락이 생기기 쉬움 | `Quiz` 생성 시 선택지 4개·정답 1~4를 검증해 잘못된 퀴즈가 만들어지지 않음 |
| 상태 공유 | 퀴즈 목록, 최고 점수, 기록을 전역 변수나 인자로 계속 전달 | `QuizGame` 의 속성으로 한곳에서 관리하고 메서드가 `self` 로 접근 |
| 기능 추가 | 힌트·기록을 추가하면 여러 함수의 인자와 `dict` 형식을 모두 수정 | `Quiz` 에 `hint` 속성만 추가하고, `QuizGame` 에 메서드를 더하면 됨 |
| 저장/불러오기 | `dict` ↔ JSON 변환 코드가 흩어짐 | `to_dict()` / `from_dict()` 로 변환 책임이 `Quiz` 안에 모임 |
| 테스트·재사용 | 전역 상태에 의존해 일부만 떼어 시험하기 어려움 | `Quiz` 하나만 만들어 `is_correct()` 를 바로 시험할 수 있음 |

결론적으로 "퀴즈 하나"와 "게임 전체"는 책임이 다르므로 클래스로 분리하면 코드를 읽기 쉽고, 보너스 기능(힌트, 삭제, 기록)을 추가할 때 수정 범위가 작았습니다. 반면 입력 검증(`read_int`, `read_text`)처럼 **상태가 필요 없는 일**은 클래스에 넣지 않고 `inputs.py` 의 함수로 두었습니다. 즉 클래스와 함수를 각각 맞는 곳에 사용했습니다.

## 6-2. 핵심 개념 정리
- **변수와 자료형**: 변수는 값을 담는 이름표입니다. `int`(정수: 정답 번호), `str`(문자열: 문제), `bool`(참/거짓: 정답 여부), `list`(순서 있는 모음: 퀴즈·선택지), `dict`(키-값 쌍: JSON 저장 형태)를 목적에 맞게 썼습니다.
- **조건문 `if/elif/else`**: 메뉴 번호에 따라 다른 기능을 실행하고, 정답이면 "정답", 아니면 "오답"으로 갈라집니다.
- **`for` vs `while`**: 횟수·대상이 정해진 반복(퀴즈 목록 순회)은 `for`, 올바른 입력이 올 때까지 반복(입력 재시도, 메뉴 루프)은 `while` 을 썼습니다.
- **함수**: 매개변수로 입력을 받고 반환값으로 결과를 돌려줍니다. 예) `read_int(prompt, low, high)` 는 범위 안의 정수만 반환합니다.
- **파일 입출력과 JSON**: `open()` 으로 파일을 열어 읽고 쓰며(`with` 로 자동 닫기), JSON은 `dict`/`list` 를 텍스트로 표현하는 범용 형식이라 사람이 읽을 수 있고 언어에 상관없이 데이터를 저장·교환하기 좋습니다.
- **`try/except`**: 파일이 없거나 손상되었거나 입력이 숫자가 아닐 때 프로그램이 죽지 않고 안내 후 복구하도록 오류를 처리합니다.
- **Git 명령어**: `init`(저장소 생성), `add`(커밋할 변경 선택), `commit`(변경 이력 저장), `push`(원격에 업로드), `pull`(원격 변경 가져오기), `checkout`(브랜치 이동·생성), `clone`(원격 저장소 복제). 브랜치는 `checkout -b` 로 만들고 `merge` 로 `main` 에 합쳤습니다.

## 7. Git 작업 기록
- 기능 단위 커밋 (`Feat:` / `Refactor:` / `Docs:` 접두어 + 변경 요약), 10개 이상
- `feature/play-quiz` 브랜치에서 퀴즈 풀기를 구현한 뒤 `main` 으로 병합 (`checkout`, `merge`)
- 보너스 기능도 `feature/bonus-*` 브랜치에서 구현한 뒤 `main` 으로 병합
- 사용한 기본 명령어: `init`, `add`, `commit`, `push`, `pull`, `checkout`, `clone`
- 실행 로그: [docs/evidence.md](docs/evidence.md)

> 이 저장소는 `git clone` / `git pull` 실습을 거쳐 검증되었습니다.

## 8. 실행 화면
실제 프로그램 출력과 `git`/`python` 명령 결과를 터미널 스타일 이미지로 렌더링한 캡처입니다.
(전체 텍스트 로그: [docs/evidence.md](docs/evidence.md))

| 화면 | 파일 |
|---|---|
| 개발 환경(Python/Git/원격) | [docs/screenshots/env.png](docs/screenshots/env.png) |
| 메뉴 | [docs/screenshots/menu.png](docs/screenshots/menu.png) |
| 퀴즈 풀기 | [docs/screenshots/play.png](docs/screenshots/play.png) |
| 퀴즈 추가/목록 | [docs/screenshots/add_quiz.png](docs/screenshots/add_quiz.png) |
| 퀴즈 삭제 | [docs/screenshots/delete_quiz.png](docs/screenshots/delete_quiz.png) |
| 점수 확인·게임 기록(재시작 후 유지) | [docs/screenshots/score.png](docs/screenshots/score.png) |
| `git log --oneline --graph` | [docs/screenshots/git_log.png](docs/screenshots/git_log.png) |
