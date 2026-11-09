"""QuizGame: 메뉴 표시와 메뉴별 기능 연결을 담당한다."""
from quiz_data import create_default_quizzes

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
    def __init__(self):
        self.running = True
        self.quizzes = create_default_quizzes()

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
            print("\n⚠️ 입력이 중단되었습니다. 안전하게 종료합니다.")
