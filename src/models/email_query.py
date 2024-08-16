from pydantic import BaseModel


class EmailQueryInput(BaseModel):
    text: str


class EmailQueryOutput(BaseModel):
    input: str
    output: str
    intermediate_steps: list[str]
