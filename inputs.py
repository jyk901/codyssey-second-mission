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


def read_answer(prompt, low, high, hint_key="h"):
    """정답 번호(low~high) 또는 힌트 키를 입력받는다. 힌트 키면 문자열 그대로 반환."""
    while True:
        raw = input(prompt).strip()
        if raw.lower() == hint_key:
            return hint_key
        if raw == "":
            print(f"⚠️ 입력이 비어 있습니다. 숫자 또는 힌트({hint_key})를 입력하세요.")
            continue
        try:
            number = int(raw)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자(힌트: {hint_key})를 입력하세요.")
            continue
        if not low <= number <= high:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자(힌트: {hint_key})를 입력하세요.")
            continue
        return number


def read_optional(prompt):
    """비어 있어도 되는 텍스트를 입력받는다."""
    return input(prompt).strip()


def read_text(prompt):
    """빈 문자열이 아닌 텍스트를 입력받는다. 빈 입력이면 안내 후 재입력."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("⚠️ 빈 입력입니다. 내용을 입력하세요.")
            continue
        return text
