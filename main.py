"""나만의 퀴즈 게임 - 프로그램 진입점."""
import sys

from game import QuizGame


def main():
    # 윈도우 콘솔에서도 이모지/한글이 깨지지 않도록 UTF-8 출력을 시도한다.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
