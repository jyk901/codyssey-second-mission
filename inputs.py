"""입력 처리 함수 모음: 공백/변환 실패/범위/빈 입력을 공통으로 처리한다."""


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


def read_text(prompt):
    """빈 문자열이 아닌 텍스트를 입력받는다. 빈 입력이면 안내 후 재입력."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("⚠️ 빈 입력입니다. 내용을 입력하세요.")
            continue
        return text
