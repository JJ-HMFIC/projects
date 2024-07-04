from database.orm import ToDo
from database.repository import ToDoRepository


#client = TestClient(app=app) -> conftest



# 전체 조회 정렬/역정렬 테스트
def test_get_todos(client, mocker):
    #order = ASC
    mocker.patch.object(ToDoRepository,"get_todos",return_value =[
        ToDo(id=1, contents="FastAPI Section 0", is_done=True),
        ToDo(id=2, contents="FastAPI Section 1", is_done=False),
    ])
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {
        "todos":[
            {"id": 1, "contents" : "FastAPI Section 0", "is_done" : True},
            {"id": 2, "contents" : "FastAPI Section 1", "is_done" : False},
            #{"id": 3, "contents" : "FastAPI Section 2", "is_done" : True},
        ]
    }
    #order = DESC
    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "todos":[
            #{"id": 3, "contents" : "FastAPI Section 2", "is_done" : True},
            {"id": 2, "contents" : "FastAPI Section 1", "is_done" : False},
            {"id": 1, "contents" : "FastAPI Section 0", "is_done" : True},
        ]
    }
    # 위 함수의 구조 = api 두 번 호출 및 db 두번 접근
    # mocking => 속이는 기술

def test_get_todo(client, mocker):
    #200
    mocker.patch.object(
        ToDoRepository,"get_todo_by_todo_id",
        return_value= ToDo(id=1, contents="todo", is_done=True),
    )
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "todo", "is_done": True}
    #404
    mocker.patch.object(
        ToDoRepository,"get_todo_by_todo_id",
        return_value=None
    )
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {'detail': "Todo Not Found"}


def test_create_todo(client, mocker):
    create_spy = mocker.spy(ToDo, "create")
    mocker.patch.object(
        ToDoRepository,"create_todo",
        return_value=ToDo(id=1, contents="todo", is_done=True)
    )

    body = {
        "contents": "test",
        "is_done": False,
    }
    response = client.post("/todos", json=body)

    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done is False

    assert response.status_code == 201
    assert response.json() == {"id": 1, "contents": "todo", "is_done": True}
    #섹션 4 학습 후 바꾸기

def test_update_todo(client, mocker):
    # 200
    mocker.patch.object(
        ToDoRepository,"get_todo_by_todo_id",
        return_value=ToDo(id=1, contents="todo", is_done=True),
    )
    undone = mocker.patch.object(ToDo, "undone")
    mocker.patch.object(
        ToDoRepository,"update_todo",
        return_value=ToDo(id=1, contents="todo", is_done=False),
    )
    response = client.patch("/todos/1", json={"is_done": False})

    undone.assert_called_once_with()

    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "todo", "is_done": False}
    # 404
    mocker.patch.object(ToDoRepository,"get_todo_by_todo_id",return_value=None)

    response = client.patch("/todos/1",json={"is_done": True})
    assert response.status_code == 404
    assert response.json() == {'detail': "Todo Not Found"}

def test_delete_todo(client, mocker):
    # 204
    mocker.patch.object(
        ToDoRepository,"get_todo_by_todo_id",
        return_value=ToDo(id=1, contents="todo", is_done=True),
    )
    mocker.patch.object(
        ToDoRepository,"delete_todo",
        return_value=None
    )
    response = client.get("/todos/1")
    assert response.status_code == 200

    # 404
    mocker.patch.object(
        ToDoRepository,"get_todo_by_todo_id",
        return_value=None
    )
    response = client.delete("/todos/1")
    assert response.status_code == 404
    assert response.json() == {'detail': "Todo Not Found"}
