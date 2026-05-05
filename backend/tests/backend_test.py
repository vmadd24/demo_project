import os
import uuid
import requests
import pytest

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://a236fb6e-4c30-43ff-a5e2-59430fa4f995.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"
ADMIN_EMAIL = "admin@bakery.com"
ADMIN_PASSWORD = "admin123"


@pytest.fixture(scope="session")
def s():
    return requests.Session()


@pytest.fixture(scope="session")
def admin_token(s):
    r = s.post(f"{API}/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert r.status_code == 200, r.text
    data = r.json()
    assert "token" in data and data["role"] == "admin"
    return data["token"]


@pytest.fixture(scope="session")
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


# ---------- Products (public) ----------
class TestProductsPublic:
    def test_list_products_seeded(self, s):
        r = s.get(f"{API}/products")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) >= 9, f"expected >=9, got {len(data)}"
        for p in data:
            assert "id" in p and "name" in p and "category" in p and "price" in p

    def test_filter_by_bread(self, s):
        r = s.get(f"{API}/products", params={"category": "Bread"})
        assert r.status_code == 200
        data = r.json()
        assert len(data) > 0
        assert all(p["category"] == "Bread" for p in data)

    def test_get_product_by_id(self, s):
        pid = s.get(f"{API}/products").json()[0]["id"]
        r = s.get(f"{API}/products/{pid}")
        assert r.status_code == 200
        assert r.json()["id"] == pid

    def test_get_product_404(self, s):
        r = s.get(f"{API}/products/{uuid.uuid4()}")
        assert r.status_code == 404


# ---------- Auth ----------
class TestAuth:
    def test_login_wrong_password(self, s):
        r = s.post(f"{API}/auth/login", json={"email": ADMIN_EMAIL, "password": "wrong"})
        assert r.status_code == 401

    def test_login_sets_cookie(self, s):
        sess = requests.Session()
        r = sess.post(f"{API}/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
        assert r.status_code == 200
        # Check cookie in response headers (Set-Cookie)
        set_cookie = r.headers.get("set-cookie", "")
        assert "access_token" in set_cookie.lower()
        assert "httponly" in set_cookie.lower()

    def test_me_with_bearer(self, s, auth_headers):
        r = s.get(f"{API}/auth/me", headers=auth_headers)
        assert r.status_code == 200
        assert r.json()["email"] == ADMIN_EMAIL
        assert r.json()["role"] == "admin"

    def test_me_without_auth(self, s):
        r = requests.get(f"{API}/auth/me")
        assert r.status_code == 401


# ---------- Products Admin CRUD ----------
class TestProductsAdmin:
    def test_create_without_auth(self, s):
        r = requests.post(f"{API}/products", json={"name": "X", "category": "Bread", "price": 1})
        assert r.status_code == 401

    def test_create_update_delete(self, s, auth_headers):
        # create
        payload = {"name": "TEST_Cinnamon Roll", "category": "Pastry", "price": 3.5, "description": "t", "image_url": "", "available": True}
        r = s.post(f"{API}/products", headers=auth_headers, json=payload)
        assert r.status_code == 200, r.text
        pid = r.json()["id"]
        assert r.json()["name"] == payload["name"]
        # GET verify
        r2 = s.get(f"{API}/products/{pid}")
        assert r2.status_code == 200 and r2.json()["price"] == 3.5
        # update
        upd = {**payload, "price": 4.25, "name": "TEST_Cinnamon Roll v2"}
        r3 = s.put(f"{API}/products/{pid}", headers=auth_headers, json=upd)
        assert r3.status_code == 200 and r3.json()["price"] == 4.25
        r4 = s.get(f"{API}/products/{pid}")
        assert r4.json()["name"] == "TEST_Cinnamon Roll v2"
        # delete
        r5 = s.delete(f"{API}/products/{pid}", headers=auth_headers)
        assert r5.status_code == 200
        r6 = s.get(f"{API}/products/{pid}")
        assert r6.status_code == 404


# ---------- Orders ----------
class TestOrders:
    def test_create_order_no_auth_and_admin_list(self, s, auth_headers):
        products = s.get(f"{API}/products").json()
        p = products[0]
        order_payload = {
            "customer_name": "TEST Jane",
            "phone": "555-1234",
            "address": "1 Bakery Ln",
            "notes": "no onions",
            "items": [{"product_id": p["id"], "product_name": p["name"], "quantity": 2, "price": p["price"]}],
        }
        r = requests.post(f"{API}/orders", json=order_payload)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["total"] == round(p["price"] * 2, 2)
        assert body["status"] == "pending"
        oid = body["id"]

        # list without auth -> 401
        r2 = requests.get(f"{API}/orders")
        assert r2.status_code == 401

        # list with admin
        r3 = s.get(f"{API}/orders", headers=auth_headers)
        assert r3.status_code == 200
        ids = [o["id"] for o in r3.json()]
        assert oid in ids

        # patch status
        r4 = s.patch(f"{API}/orders/{oid}/status", headers=auth_headers, json={"status": "confirmed"})
        assert r4.status_code == 200 and r4.json()["status"] == "confirmed"

        # invalid status
        r5 = s.patch(f"{API}/orders/{oid}/status", headers=auth_headers, json={"status": "bogus"})
        assert r5.status_code == 400

    def test_create_order_empty_items(self, s):
        r = requests.post(f"{API}/orders", json={"customer_name": "a", "phone": "1", "address": "a", "items": []})
        # Pydantic may reject or endpoint returns 400
        assert r.status_code in (400, 422)
