from typing import List

from pydantic import BaseModel


class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool
    # response를 분리한 이유 = 컬럼을 분리하여 반환하거나 그런 의미에서

    class Config:
        orm_mode = True # orm 객체 해석




class ToDoListSchema(BaseModel):
    todos: List[ToDoSchema]

