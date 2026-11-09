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
| 1 | 퀴즈 풀기 | 저장된 퀴즈를 차례로 출제 → 정답 번호 입력 → 정답/오답 안내 → 모두 풀면 결과 표시 (퀴즈가 없으면 안내) |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호(1~4)를 입력받아 등록하고 즉시 `state.json`에 저장 |
| 3 | 퀴즈 목록 | 등록된 퀴즈의 문제 목록 출력 (퀴즈가 없으면 안내) |
| 4 | 점수 확인 | 최고 점수 출력 (아직 풀지 않았다면 안내). 퀴즈를 풀 때마다 비교·갱신·저장 |
| 5 | 종료 | 저장 후 종료 |

**공통 입력/예외 처리**: 앞뒤 공백 제거 · 숫자 변환 실패(`abc`) · 허용 범위 밖(메뉴 `9`, 정답 `0`) · 빈 입력(Enter)은 모두 안내 메시지 후 재입력합니다. `KeyboardInterrupt`/`EOFError` 는 비정상 종료 없이 저장 후 종료합니다.

**데이터 파일 복구**: `state.json` 이 없으면 기본 퀴즈로 시작하고, 손상되었거나 구조가 틀리면 안내 후 `state.json.corrupt` 로 백업하고 기본 퀴즈로 복구합니다.

## 5. 파일 구조
```
second-mission/
├── main.py        # 진입점 (UTF-8 출력 설정, QuizGame 실행)
├── game.py        # QuizGame 클래스: 메뉴, 풀기/추가/목록/점수, state.json 저장/불러오기
├── quiz.py        # Quiz 클래스: 문제/선택지/정답, 출력·정답 확인·dict 변환
├── quiz_data.py   # 기본 퀴즈 데이터 6개 (Quiz 인스턴스 생성)
├── inputs.py      # 입력 처리 함수 (read_int, read_text)
├── state.json     # 저장 데이터 (퀴즈 목록 + 최고 점수)
├── docs/
│   └── run_logs.md  # 실행 화면 로그 (메뉴/풀기/추가/목록/점수/오류 입력/재시작)
├── .gitignore
└── README.md
```

### 클래스 설계
- `Quiz`: 속성 `question`, `choices`(4개), `answer`(1~4 번호) / 메서드 `display()`, `is_correct()`, `to_dict()`, `from_dict()`
- `QuizGame`: 속성 `quizzes`, `best_score`, `best_correct`, `best_total` / 메서드 `show_menu()`, `play_quiz()`, `add_quiz()`, `show_quiz_list()`, `show_score()`, `load_state()`, `save_state()`, `run()` 등

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
            "answer": 2
        }
    ],
    "best_score": 83,
    "best_correct": 5,
    "best_total": 6
}
```

| 키 | 타입 | 설명 |
|---|---|---|
| `quizzes` | list | 퀴즈 목록. 각 항목은 `question`(문자열), `choices`(문자열 4개), `answer`(정답 번호 1~4) |
| `best_score` | int | 최고 점수 (100점 만점, 정답 수 ÷ 문제 수 × 100 반올림) |
| `best_correct` | int | 최고 점수를 기록한 판의 정답 수 |
| `best_total` | int | 최고 점수를 기록한 판의 문제 수 (`0` 이면 아직 풀지 않은 상태) |

## 7. Git 작업 기록
- 기능 단위 커밋 (`Feat:` / `Refactor:` / `Docs:` 접두어 + 변경 요약), 10개 이상
- `feature/play-quiz` 브랜치에서 퀴즈 풀기를 구현한 뒤 `main` 으로 병합 (`checkout`, `merge`)
- 사용한 기본 명령어: `init`, `add`, `commit`, `push`, `pull`, `checkout`, `clone`
- 실행 로그: [docs/run_logs.md](docs/run_logs.md)
