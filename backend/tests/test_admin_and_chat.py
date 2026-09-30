import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_chat_medical_exact_questions():
    # 1. Anemia query
    res_anemia = client.post("/api/chat/", json={"message": "What causes anemia?"})
    assert res_anemia.status_code == 200
    assert "anemia" in res_anemia.json()["reply"].lower()
    assert "red blood cell" in res_anemia.json()["reply"].lower() or "iron" in res_anemia.json()["reply"].lower()

    # 2. Diabetes query
    res_diabetes = client.post("/api/chat/", json={"message": "What are the symptoms of diabetes?"})
    assert res_diabetes.status_code == 200
    assert "diabetes" in res_diabetes.json()["reply"].lower()
    assert "polyuria" in res_diabetes.json()["reply"].lower() or "thirst" in res_diabetes.json()["reply"].lower() or "glucose" in res_diabetes.json()["reply"].lower()

    # 3. Biopsy query
    res_biopsy = client.post("/api/chat/", json={"message": "What is a biopsy?"})
    assert res_biopsy.status_code == 200
    assert "biopsy" in res_biopsy.json()["reply"].lower()
    assert "tissue" in res_biopsy.json()["reply"].lower()

    # 4. Model accuracy query
    res_acc = client.post("/api/chat/", json={"message": "What is the model accuracy?"})
    assert res_acc.status_code == 200
    assert "100.0%" in res_acc.json()["reply"] or "100%" in res_acc.json()["reply"]
    assert "15,000" in res_acc.json()["reply"] or "15000" in res_acc.json()["reply"]

def test_admin_users_unauthorized():
    # Without token
    response = client.get("/api/auth/users")
    assert response.status_code in [401, 403]

def test_admin_users_lifecycle():
    # Login as admin
    login_res = client.post("/api/auth/login", json={"email": "admin@lymphoma.ai", "password": "Admin@123"})
    assert login_res.status_code == 200
    admin_token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {admin_token}"}

    # List users
    users_res = client.get("/api/auth/users", headers=headers)
    assert users_res.status_code == 200
    users_data = users_res.json()
    assert "total" in users_data
    assert "users" in users_data
    assert users_data["total"] >= 1

    # Register temporary user
    temp_email = "test_temp_user_mgmt@lymphoma.ai"
    # Clean up first if exists
    clean_del = client.delete("/api/auth/users/9999", headers=headers)
    
    reg_res = client.post("/api/auth/register", json={
        "full_name": "Temporary Test User",
        "email": temp_email,
        "password": "Password@123"
    })
    if reg_res.status_code == 400: # Already exists, delete first
        for u in users_data["users"]:
            if u["email"] == temp_email:
                client.delete(f"/api/auth/users/{u['id']}", headers=headers)
        reg_res = client.post("/api/auth/register", json={
            "full_name": "Temporary Test User",
            "email": temp_email,
            "password": "Password@123"
        })
    assert reg_res.status_code == 200
    created_user_id = reg_res.json()["user"]["id"]

    # Toggle status to DISABLED
    patch_res = client.patch(f"/api/auth/users/{created_user_id}/status", json={"status": "DISABLED"}, headers=headers)
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "DISABLED"
    assert patch_res.json()["is_active"] is False

    # Attempt login with disabled user (should fail with 403)
    disabled_login = client.post("/api/auth/login", json={"email": temp_email, "password": "Password@123"})
    assert disabled_login.status_code == 403

    # Toggle status back to ACTIVE
    patch_res2 = client.patch(f"/api/auth/users/{created_user_id}/status", json={"status": "ACTIVE"}, headers=headers)
    assert patch_res2.status_code == 200
    assert patch_res2.json()["status"] == "ACTIVE"
    assert patch_res2.json()["is_active"] is True

    # Delete user
    del_res = client.delete(f"/api/auth/users/{created_user_id}", headers=headers)
    assert del_res.status_code == 200
    assert del_res.json()["status"] == "success"

    # Attempt to delete admin itself (should fail with 400)
    admin_id = login_res.json()["user"]["id"]
    self_del_res = client.delete(f"/api/auth/users/{admin_id}", headers=headers)
    assert self_del_res.status_code == 400
