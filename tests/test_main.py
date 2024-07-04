def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping":"pong"}
# 맨 처음 화면에 나오는 기능 테스트