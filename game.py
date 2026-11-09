"""QuizGame: 메뉴 표시와 메뉴별 기능 연결을 담당한다."""

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
        print("🚧 퀴즈 풀기는 준비 중입니다.")

    def add_quiz(self):
        print("🚧 퀴즈 추가는 준비 중입니다.")

    def show_quiz_list(self):
        print("🚧 퀴즈 목록은 준비 중입니다.")

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
