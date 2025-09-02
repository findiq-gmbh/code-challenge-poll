from sqlmodel import Field, SQLModel


class Answer(SQLModel, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
        description="The unique identifier for an answer",
    )
    question_id: int = Field(
        foreign_key="question.id",
        description="The ID of the question this answer belongs to",
    )
    text: str = Field(index=True, description="The text of the answer", max_length=1000)
