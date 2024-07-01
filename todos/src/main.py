from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from database.orm import ToDo
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
from schema.request import CreateToDoRequest
from schema.response import ToDoListSchema, ToDoSchema

app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"ping": "pong"}

todo_data = {
    1: {
        "id": 1,
        "contents" : "실전! FastAPI 섹션 0 수강",
        "is_done" : True,
    },
    2: {
        "id": 2,
        "contents" : "실전! FastAPI 섹션 1 수강",
        "is_done" : False,
    },
    3: {
        "id": 3,
        "contents" : "실전! FastAPI 섹션 2 수강",
        "is_done" : False,
    }
}

@app.get("/todos",status_code = 200) # 전체 조회
def get_todos_handler(order : str| None = None,
                      session : Session = Depends(get_db)
                      ) -> ToDoListSchema:
    todos: List[ToDo] = get_todos(session=session)
    # ret = list(todo_data.values())

    if order and order == "DESC":
        #return ret[::-1]
        return ToDoListSchema(
        todos=[ ToDoSchema.from_orm(todo) for todo in todos[::-1]]
        )
    #return ret
    return ToDoListSchema(
        todos=[ ToDoSchema.from_orm(todo) for todo in todos ]
    )

#단일조회
@app.get("/todos/{todo_id}",status_code = 200) # 단일 조회
def get_todo_handler(
        todo_id : int,
        session : Session = Depends(get_db)
) -> ToDoSchema:
    # todo = todo_data.get(todo_id)
    todo: ToDo | None =  get_todo_by_todo_id(session= session, todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code = 404, detail="Todo Not Found")


@app.post("/todos", status_code=201) # 생성
def create_todo_handler(
        request : CreateToDoRequest,
        session : Session = Depends(get_db),
)-> ToDoSchema:
    # pydantic으로 받은 데이터를 orm으로 생성
    todo : ToDo = ToDo.create(request=request) # id=None
    todo : ToDo = create_todo(session=session, todo=todo) #id=int

    #todo_data[request.id] = request.dict()
    #return todo_data[request.id]
    return ToDoSchema.from_orm(todo)


@app.patch("/todos/{todo_id}",status_code=200) # 수정
def update_todo_handler(
        todo_id : int,
        is_done : bool = Body(..., embed=True),
        session : Session = Depends(get_db)
):
    #todo = todo_data.get(todo_id)
    #if todo:
    #    todo['is_done'] = is_done
    #    return todo
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        # update
        todo.done() if is_done else todo.undone()
       # if is_done is True:
       #     todo.done()
       # else:
       #     todo.undone()
        todo : ToDo = update_todo(session=session, todo=todo)
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo Not Found")

@app.delete("/todos/{todo_id}",status_code=204)
def delete_todo_handler(
        todo_id : int,
        session: Session = Depends(get_db)
):
    #todo = todo_data.pop(todo_id, None)

    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    delete_todo(session=session,todo_id=todo_id)

    # return todo_data
