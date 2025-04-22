def test_add_participant(client, db_setup):
    response = client.post("/participants", json={"name": "Alice"})
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"



