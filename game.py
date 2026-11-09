"""QuizGame: 메뉴 표시와 메뉴별 기능 연결을 담당한다."""
import json
import os
from pathlib import Path

from quiz import Quiz
from quiz_data import create_default_quizzes

STATE_FILE = Path(__file__).resolve().parent / "state.json"

LINE = "=" * 40
MENU_MIN = 1
MENU_MAX = 5


def read_int(prompt, low, high):
    """low~high 사이 정수를 입력받는다. 잘못된 입력이면 안내 후 재입력."""
    while True:
        raw = input(prompt).strip()
        if raw == "":
            print("⚠️ 입력이 비어 있습니다. 숫자를 입력하세요.")
            continue
        try:
            number = int(raw)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        if not low <= number <= high:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        return number


class QuizGame:
    def __init__(self, state_path=STATE_FILE):
        self.running = True
        self.state_path = Path(state_path)
        self.quizzes = create_default_quizzes()
        self.best_score = 0      # 최고 점수(100점 만점)
        self.best_correct = 0    # 최고 점수를 낸 판의 정답 수
        self.best_total = 0      # 최고 점수를 낸 판의 문제 수 (0이면 아직 안 푼 상태)
        self.load_state()

    # ---------- 파일 저장/불러오기 ----------
    def load_state(self):
        """state.json에서 퀴즈와 최고 점수를 불러온다.

        파일이 없으면 기본 퀴즈를 쓰고, 손상되었으면 안내 후 기본값으로 복구한다.
        """
        if not self.state_path.exists():
            print("🆕 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            self.save_state()
            return

        try:
            with open(self.state_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best_score = int(data.get("best_score", 0))
            best_correct = int(data.get("best_correct", 0))
            best_total = int(data.get("best_total", 0))
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            print("⚠️ 데이터 파일을 읽을 수 없거나 손상되어 기본 퀴즈로 복구합니다.")
            self.backup_broken_file()
            self.save_state()
            return

        self.quizzes = quizzes
        self.best_score = best_score
        self.best_correct = best_correct
        self.best_total = best_total
        print(f"📂 저장된 데이터를 불러왔습니다. "
              f"(퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")

    def backup_broken_file(self):
        """손상된 파일은 지우지 않고 .corrupt 로 옮겨 둔다."""
        try:
            os.replace(self.state_path, str(self.state_path) + ".corrupt")
        except OSError:
            pass

    def save_state(self):
        """현재 퀴즈와 최고 점수를 state.json에 UTF-8로 저장한다. 성공 여부 반환."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }
        temp_path = str(self.state_path) + ".tmp"
        try:
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            os.replace(temp_path, self.state_path)
            return True
        except OSError:
            print("⚠️ 데이터 파일을 저장하지 못했습니다.")
            return False

    # ---------- 메뉴 ----------

    def show_menu(self):
        print(LINE)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print(LINE)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print(LINE)

    def handle_choice(self, choice):
        if choice == 1:
            self.play_quiz()
        elif choice == 2:
            self.add_quiz()
        elif choice == 3:
            self.show_quiz_list()
        elif choice == 4:
            self.show_score()
        elif choice == 5:
            self.quit()

    # 아래 기능들은 이후 커밋에서 하나씩 구현한다.
    def play_quiz(self):
        """저장된 퀴즈를 차례로 출제하고 정답/오답을 알려준 뒤 결과를 표시한다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        correct = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            print("\n" + "-" * 40)
            quiz.display(number)
            print()
            user_answer = read_int("정답 입력: ", 1, len(quiz.choices))
            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        self.show_result(correct, total)

    def show_result(self, correct, total):
        score = round(correct / total * 100)
        print("\n" + LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        print(LINE)

    def add_quiz(self):
        print("🚧 퀴즈 추가는 준비 중입니다.")

    def show_quiz_list(self):
        """저장된 퀴즈의 문제 목록을 보여준다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    def show_score(self):
        print("🚧 점수 확인은 준비 중입니다.")

    def quit(self):
        self.save_state()
        print("👋 퀴즈 게임을 종료합니다.")
        self.running = False

    def run(self):
        try:
            while self.running:
                self.show_menu()
                choice = read_int("선택: ", MENU_MIN, MENU_MAX)
                self.handle_choice(choice)
                print()
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ 입력이 중단되었습니다. 저장 후 안전하게 종료합니다.")
            self.save_state()
