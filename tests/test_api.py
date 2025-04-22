def test_add_participant(client, db_setup):
    response = client.post("/participants", json={"name": "Alice"})
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"

def test_add_second_participant(client, db_setup):
    response = client.post("/participants", json={"name": "Bob"})
    assert response.status_code == 200
    assert response.json()["name"] == "Bob"

def test_add_to_blacklist(client, db_setup):
    response = client.post("/participants/1/blacklist/2")
    assert response.status_code == 200
    assert response.json()["message"] == "Added to blacklist"

def test_add_third_participant(client, db_setup):
    response = client.post("/participants", json={"name": "Charlie"})
    assert response.status_code == 200
    assert response.json()["name"] == "Charlie"

def test_add_fourth_participant(client, db_setup):
    response = client.post("/participants", json={"name": "Diana"})
    assert response.status_code == 200
    assert response.json()["name"] == "Diana"

def test_valid_draw(client, db_setup):
    response = client.get("/draw")
    assert response.status_code == 200
    draw_result = response.json()
    assert len(draw_result) == 4
    givers = set()
    receivers = set()
    for pair in draw_result:
        giver = pair["giver"]
        receiver = pair["receiver"]
        assert giver != receiver
        givers.add(giver)
        receivers.add(receiver)
    assert len(givers) == len(receivers)

def test_get_last_5_draws(client, db_setup):
    response = client.get("/draws")
    assert response.status_code == 200
    draws = response.json()
    assert len(draws) <= 5
    assert all("giver" in draw and "receiver" in draw for draw in draws)
