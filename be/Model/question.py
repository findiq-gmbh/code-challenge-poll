from sqlmodel import Field, SQLModel


class Question(SQLModel, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
        description="The unique identifier for a question",
    )
    title: str = Field(
        index=True, description="The title of the question", max_length=1000
    )
    visitor_count: int = Field(
        default=0, description="The number of visitors who have seen the question"
    )
