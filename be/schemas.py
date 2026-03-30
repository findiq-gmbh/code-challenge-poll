from pydantic import BaseModel, field_validator

MAX_TEXT_LENGTH = 500


def validate_text(v: str) -> str:
    v = v.strip()
    if not v:
        raise ValueError("must not be blank")
    if len(v) > MAX_TEXT_LENGTH:
        raise ValueError(f"must be {MAX_TEXT_LENGTH} characters or fewer")
    return v


class QuestionCreate(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, v: str) -> str:
        return validate_text(v)


class AnswerCreate(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, v: str) -> str:
        return validate_text(v)
