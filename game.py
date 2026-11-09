"""QuizGame: 메뉴 표시와 메뉴별 기능 연결을 담당한다."""
import json
import os
import random
from pathlib import Path

from inputs import read_answer, read_int, read_optional, read_text
from quiz import CHOICE_COUNT, Quiz
from quiz_data import create_default_quizzes

STATE_FILE = Path(__file__).resolve().parent / "state.json"

LINE = "=" * 40
MENU_MIN = 1
MENU_MAX = 6
HINT_PENALTY = 0.5   # 힌트 1회당 차감되는 정답 수 (문제 배점의 절반)


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
        print("5. 퀴즈 삭제")
        print("6. 종료")
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
            self.delete_quiz()
        elif choice == 6:
            self.quit()

    # 아래 기능들은 이후 커밋에서 하나씩 구현한다.
    def play_quiz(self):
        """저장된 퀴즈를 차례로 출제하고 정답/오답을 알려준 뒤 결과를 표시한다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        # 풀 문제 수 선택 (보너스) + 랜덤 출제 (보너스)
        count = read_int(f"풀 문제 수 (1-{len(self.quizzes)}): ", 1, len(self.quizzes))
        selected = random.sample(self.quizzes, count)  # 무작위로 섞어서 count개 선택

        total = len(selected)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        correct = 0
        hints_used = 0
        for number, quiz in enumerate(selected, start=1):
            print("\n" + "-" * 40)
            quiz.display(number)
            print()
            user_answer, used = self.ask_answer(quiz)
            hints_used += used
            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        self.show_result(correct, total, hints_used)

    def ask_answer(self, quiz):
        """정답을 입력받는다. 'h' 를 입력하면 힌트를 보여준다(점수 차감).

        (정답 번호, 이번 문제에서 새로 사용한 힌트 수)를 반환한다.
        """
        used = 0
        while True:
            answer = read_answer("정답 입력 (힌트: h): ", 1, len(quiz.choices))
            if answer != "h":
                return answer, used
            if not quiz.has_hint():
                print("💡 이 문제에는 힌트가 없습니다.")
            elif used:
                print(f"💡 힌트: {quiz.hint} (이미 사용한 힌트입니다)")
            else:
                used = 1
                print(f"💡 힌트: {quiz.hint}  (문제 배점의 절반이 차감됩니다)")

    def calc_score(self, correct, total, hints_used):
        """점수 = (정답 수 - 힌트 사용 수 x 0.5) / 문제 수 x 100, 최소 0점."""
        effective = max(0, correct - hints_used * HINT_PENALTY)
        return round(effective / total * 100)

    def show_result(self, correct, total, hints_used=0):
        score = self.calc_score(correct, total, hints_used)
        print("\n" + LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if hints_used:
            print(f"💡 힌트 {hints_used}회 사용으로 점수가 차감되었습니다.")
        if self.update_best_score(score, correct, total):
            print("🎉 새로운 최고 점수입니다!")
        print(LINE)

    def update_best_score(self, score, correct, total):
        """이번 점수가 최고 점수보다 높으면 갱신하고 파일에 저장한다."""
        if self.best_total == 0 or score > self.best_score:
            self.best_score = score
            self.best_correct = correct
            self.best_total = total
            self.save_state()
            return True
        return False

    def add_quiz(self):
        """새 퀴즈를 입력받아 등록하고 파일에 저장한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = read_text("문제를 입력하세요: ")
        choices = [read_text(f"선택지 {i}: ") for i in range(1, CHOICE_COUNT + 1)]
        answer = read_int(f"정답 번호 (1-{CHOICE_COUNT}): ", 1, CHOICE_COUNT)
        hint = read_optional("힌트 (없으면 Enter): ")

        self.quizzes.append(Quiz(question, choices, answer, hint))
        if self.save_state():
            print("\n✅ 퀴즈가 추가되었습니다!")

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

    def delete_quiz(self):
        """번호로 퀴즈를 골라 삭제하고 파일에 반영한다."""
        if not self.quizzes:
            print("⚠️ 삭제할 퀴즈가 없습니다.")
            return

        self.show_quiz_list()
        number = read_int(f"삭제할 퀴즈 번호 (1-{len(self.quizzes)}): ", 1, len(self.quizzes))
        removed = self.quizzes.pop(number - 1)
        if self.save_state():
            print(f"\n🗑️ 퀴즈가 삭제되었습니다: {removed.question}")

    def show_score(self):
        """최고 점수를 보여준다. 아직 풀지 않았다면 안내한다."""
        if self.best_total == 0:
            print("⚠️ 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어보세요!")
            return
        print(f"\n🏆 최고 점수: {self.best_score}점 "
              f"({self.best_total}문제 중 {self.best_correct}문제 정답)")

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
