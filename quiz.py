"""Quiz: 개별 퀴즈 하나를 표현하는 클래스."""

CHOICE_COUNT = 4


class Quiz:
    def __init__(self, question, choices, answer, hint=""):
        """
        question: 문제 문자열
        choices : 선택지 문자열 4개짜리 list
        answer  : 정답 번호 (1~4)
        hint    : 힌트 문자열 (선택, 없으면 빈 문자열)
        """
        if len(choices) != CHOICE_COUNT:
            raise ValueError(f"선택지는 {CHOICE_COUNT}개여야 합니다.")
        if not 1 <= answer <= CHOICE_COUNT:
            raise ValueError(f"정답은 1~{CHOICE_COUNT} 사이여야 합니다.")
        self.question = question
        self.choices = list(choices)
        self.answer = answer
        self.hint = hint

    def display(self, number=None):
        """문제와 선택지를 화면에 출력한다."""
        if number is not None:
            print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer):
        """사용자가 입력한 번호가 정답인지 확인한다."""
        return user_answer == self.answer

    def has_hint(self):
        return bool(self.hint)

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        """dict(JSON)에서 Quiz를 만든다. 형식이 틀리면 ValueError/KeyError/TypeError."""
        return cls(data["question"], data["choices"], data["answer"],
                   data.get("hint", ""))
